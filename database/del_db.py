import get_config
from pymongo import MongoClient


def delete():
    config = get_config.get_variable()
    client = MongoClient(config["mongoUrl"])
    client.drop_database('pythondb') # delete db
