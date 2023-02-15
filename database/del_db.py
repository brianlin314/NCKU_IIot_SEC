from pymongo import MongoClient

def delete():
    client = MongoClient()
    suricatadb = client['suricatadb']
    db = client['pythondb']
    posts = db.posts
    posts2 = suricatadb.posts
    client.drop_database('pythondb') # delete db
    client.drop_database('suricatadb')
