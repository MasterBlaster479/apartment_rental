from pony.orm import Database, sql_debug

db = Database()
db.bind('postgres', user='postgres', password='postgres', host='127.0.0.1', port=5437, database='apartment_rental')

def register_models(app):
    sql_debug(True)
    db.generate_mapping(create_tables=True, check_tables=True)