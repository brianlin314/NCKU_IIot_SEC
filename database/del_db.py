from pymongo import MongoClient
import get_config

def delete():
    config = get_config.get_variable()
    client = MongoClient(config["mongoUrl"])
    client.drop_database('pythondb') # delete db
