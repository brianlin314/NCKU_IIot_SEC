from pymongo import MongoClient

def delete():
    client = MongoClient()
    client.drop_database('pythondb') # delete db
