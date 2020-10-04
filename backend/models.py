from pony.orm import *
from datetime import date, datetime, time
import uuid
from db import db

class User(db.Entity):
    first_name = Required(str)
    last_name = Required(str)
    email = Optional(str)
    login = Required(str, unique=True)
    password = Required(str)
    active = Optional(bool, default=True)

class Guest(db.Entity):
    name = Required(str)
    uid = Required(uuid.UUID, default=uuid.uuid4)
    email = Optional(str)
    mobile = Optional(str)
    calendars = Set("Reservation", lazy=True)

class Apartment(db.Entity):
    name = Required(str)
    reservations = Set("Reservation")

class Reservation(db.Entity):
    guest_id = Required(Guest, index=True)
    apartment_id = Required(Apartment, index=True)
    date_start = Required(date)
    time_start = Required(time, default=lambda: time(15,0))
    date_end = Required(date)
    time_end = Required(time, default=lambda: time(11,0))
    note = Optional(str)



