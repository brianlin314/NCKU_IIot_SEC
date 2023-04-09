import os
from pymongo import MongoClient

from database import create_db, update_db, del_db

def get_current_db(dir_path, sudoPassword):
    # 當 last_date.pkl 不存在時(更新版本), 刪除 DB 
    if not os.path.isfile('./last_date.pkl'):
        del_db.delete()

    # 建立和mongoDB連線，取用collection中的posts
    client = MongoClient()
    db = client['pythondb']
    current_db = db.list_collection_names()
    posts = db.posts
    # current_db = []
    if current_db == []:
        num = create_db.createDB(posts, dir_path, sudoPassword)
    else:
        num = update_db.update_db(posts, dir_path, sudoPassword)
    return client, posts, num, current_db

def get_current_nidsdb(dir_path, sudoPassword):
    # 當 last_date.pkl 不存在時(更新版本), 刪除 DB 
    # if not os.path.isfile('./last_nids_num.pkl'):
    #     del_db.delete()

    # 建立和mongoDB連線，取用collection中的posts
    client = MongoClient()
    db = client['pythondb']
    current_db = db.list_collection_names()
    # current_db = 'empty'
    nidsjson = db.nidsjson
    
    if db.nidsjson.count_documents({}) == 0:
        num = create_db.createnidsDB(nidsjson, dir_path, sudoPassword)
        print("add",num,'DATA')
    else:
        print("updating.....................")
        num = update_db.update_nidsdb(nidsjson, dir_path, sudoPassword)
        print("update",num,'DATA')
    return client, nidsjson, num, current_db

def connect_db():
    client = MongoClient()
    db = client['pythondb']
    posts = db.posts
    return posts

def connect_nidsdb():
    client = MongoClient()
    db = client['pythondb']
    nidsjson = db.nidsjson
    return nidsjson