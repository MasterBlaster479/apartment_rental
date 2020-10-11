from icalendar import Calendar as ICalendar, Event
import models
import pandas
from pony.orm import db_session, select
import io
from collections import OrderedDict

@db_session
def register_user(user):
    return models.User(**dict(user))

@db_session
def login(user):
    return models.User.get(login=user.login, password=user.password)

@db_session
def get_user_by_login(login):
    return models.User.get(login=login).to_dict()

@db_session
def process_calendar_file_data(file_datas):
    for file_name, file_read in file_datas:
        file_apartment_name = file_name.replace('.ics', '')
        apartment = models.Apartment.get(name=file_apartment_name)
        if not apartment:
            apartment_id = models.Apartment(name=file_apartment_name)
        else:
            apartment_id = apartment
        calendar = ICalendar.from_ical(file_read)
        for component in calendar.subcomponents:
            note = ''
            guest_uid = str(component.get('UID'))
            if models.Guest.get(uid=guest_uid):
                guest_id = models.Guest.get(uid=guest_uid)
                note = component.get('SUMMARY')
            else:
                guest_name = str(component.get('SUMMARY'))
                guest_id = models.Guest(name=guest_name, uid=guest_uid)
            date_start, date_end = component.get('DTSTART').dt, component.get('DTEND').dt
            reservation_data = dict(guest_id=guest_id, apartment_id=apartment_id,
                                    note=note, date_start=date_start, date_end=date_end)
            models.Reservation(**reservation_data)
    return True

@db_session
def export_calendar_by_apartment_id(id):
    apartment_name, data = '', ''
    if models.Apartment.get(id=id):
        apartment = models.Apartment.get(id=id)
        apartment_name = apartment.name
        calendar = ICalendar(prodid=apartment_name)
        for reservation in apartment.reservations:
            event = Event(dtstart=reservation.date_start, dtend=reservation.date_end, uid=reservation.guest_id.uid,
                          summary=reservation.guest_id.name)
            calendar.add_component(event)
        data = io.BytesIO(calendar.to_ical())
    return apartment_name, data

@db_session
def get_calendar(date_from=None, date_to=None):
    data = OrderedDict()
    reservations = select(r for r in models.Reservation)
    if date_from:
        reservations = reservations.where(lambda r: r.date_start >= date_from)
    if date_to:
        reservations = reservations.where(lambda r: r.date_end <= date_to)
    if not reservations:
        return []
    reservation_date_start = min(r.date_start for r in reservations)
    reservation_date_stop = max(r.date_start for r in reservations)
    reserved_apartments = select(r.apartment_id.name for r in reservations).order_by(1).distinct()
    for reservation_date in pandas.date_range(reservation_date_start, reservation_date_stop):
        reservation_date = reservation_date.to_pydatetime().date()
        data[reservation_date] = {}
        starting_event = reservations.where(lambda r: r.date_start == reservation_date)
        ending_event = reservations.where(lambda r: r.date_end == reservation_date)
        ongoing_event = reservations.where(lambda r: r.date_start < reservation_date and r.date_end > reservation_date)
        apartments_start = select(e.apartment_id.name for e in starting_event).distinct()[:]
        apartments_end = select(e.apartment_id.name for e in ending_event).distinct()[:]
        apartments_ongoing = select(e.apartment_id.name for e in ongoing_event).distinct()[:]
        if apartments_ongoing:
            data[reservation_date]['cleaning_index'] = -1
        else:
            # The lesser the better
            data[reservation_date]['cleaning_index'] = len(apartments_end) * 10 + len(apartments_start) * 1
        line_repr = {}.fromkeys(reserved_apartments, '')
        line_repr.update({a: 'Occupied' for a in apartments_ongoing})
        line_repr.update({a: 'Leaving' for a in apartments_end})
        for a in apartments_start:
            if line_repr.get(a):
                line_repr[a] += '/Entering'
            else:
                line_repr[a] = 'Entering'
        data[reservation_date]['line_repr'] = line_repr
    min_cleaning_index = min(map(lambda x: x['cleaning_index'],
                                 filter(lambda x: x['cleaning_index'] != -1, data.values())))
    calendar = OrderedDict()
    calendars = []
    for key in data:
        if data[key]['cleaning_index'] == min_cleaning_index:
            data[key]['cleaning_day'] = True
            line_repr = data[key]['line_repr']
            for apartment_name in line_repr:
                if line_repr[apartment_name] != 'Occupied':
                    if line_repr[apartment_name] == 'Entering':
                        line_repr[apartment_name] = 'Cleaning/Entering'
                    elif line_repr[apartment_name] == 'Leaving':
                        line_repr[apartment_name] = 'Leaving/Cleaning'
                    elif line_repr[apartment_name] == 'Leaving/Entering':
                        line_repr[apartment_name] = 'Leaving/Cleaning/Entering'
                    else:
                        line_repr[apartment_name] = 'Cleaning'
            calendar[key] = line_repr
            new_line_repr = dict(date=key)
            new_line_repr.update(line_repr)
        else:
            line_repr = data[key]['line_repr']
            new_line_repr = dict(date=key)
            new_line_repr.update(line_repr)
            calendar[key] = line_repr
        calendars.append(new_line_repr)
    return calendars

