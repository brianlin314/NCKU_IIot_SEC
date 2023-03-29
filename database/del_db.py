from pymongo import MongoClient

def delete():
    client = MongoClient()
    db = client['pythondb']
    posts = db.posts
    client.drop_database('pythondb') # delete db
