import json
import os

from pymongo import MongoClient

from database import create_db, del_db, update_db


def get_current_db(dir_path, sudoPassword):
    # 當 last_date.pkl 不存在時(更新版本), 刪除 DB 
    if not os.path.isfile('./last_date.pkl'):
        del_db.delete()
    
    with open('config.json', 'r') as f:
        config = json.load(f)
        mongoUrl = config['mongoUrl']

    # 建立和mongoDB連線，取用collection中的posts
    client = MongoClient(mongoUrl)

    # 選擇 MongoDB 中的 pythondb 資料庫，如果這個資料庫不存在，pymongo 會在首次存取時自動創建。
    db = client['pythondb']

    # 列出所有的資料庫名稱
    current_db = db.list_collection_names()

    posts = db.posts

    if db.posts.count_documents({}) == 0:
        num = create_db.createDB(posts, dir_path, sudoPassword)
        print("HIDS add ", num, ' DATA') 
    else:
        num = update_db.update_db(posts, dir_path, sudoPassword)
        print("HIDS update ", num, ' DATA') 
    return client, posts, num, current_db

def get_current_nidsdb(dir_path, sudoPassword):
    # 當 last_date.pkl 不存在時(更新版本), 刪除 DB 
    if not os.path.isfile('./last_nids_num.pkl'):
        del_db.delete()

    with open('config.json', 'r') as f:
        config = json.load(f)
        mongoUrl = config['mongoUrl']

    # 建立和mongoDB連線，取用collection中的posts
    client = MongoClient(mongoUrl)
    db = client['pythondb']
    current_db = db.list_collection_names()
    nidsjson = db.nidsjson
    
    if db.nidsjson.count_documents({}) == 0:
        num = create_db.createnidsDB(nidsjson, dir_path, sudoPassword)
        print("NIDS add ", num, ' DATA')
    else:
        num = update_db.update_nidsdb(nidsjson, dir_path, sudoPassword)
        print("NIDS update ", num, ' DATA')
    return client, nidsjson, num, current_db


def get_current_aidb(dir_path, sudoPassword):
    with open('config.json', 'r') as f:
        config = json.load(f)
        mongoUrl = config['mongoUrl']

    # 建立和mongoDB連線，取用collection中的posts
    client = MongoClient(mongoUrl)
    db = client['pythondb']
    current_db = db.list_collection_names()
    airesult = db.airesult

    if db.airesult.count_documents({}) == 0:
        num = create_db.createaiDB(airesult, dir_path)
        print("AIIDS add ", num, ' DATA')
    else:
        num = create_db.createaiDB(airesult, dir_path)
        print("AIIDS update ", num, ' DATA')
    return client, airesult, num, current_db

def connect_db(collection_name):
    with open('config.json', 'r') as f:
        config = json.load(f)
        mongoUrl = config['mongoUrl']

    client = MongoClient(mongoUrl)
    db = client['pythondb']

    if collection_name == 'hids':
        return db.posts
    elif collection_name == 'nids':
        return db.nidsjson
    elif collection_name == 'ai':
        return db.airesult
    else:
        raise ValueError("Invalid collection_name")