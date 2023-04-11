import pymongo as pym

def connect_to_DB():
    client = pym.MongoClient()
    db = client['pythondb']
    return db

def use_table_from_DB(table):
    db = connect_to_DB()
    return db[table]