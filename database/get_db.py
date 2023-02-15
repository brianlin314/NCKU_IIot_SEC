import os
from pymongo import MongoClient

from database import create_db, update_db, del_db

def get_current_db(dir_path, sudoPassword):
    # 當 last_date.pkl 不存在時(更新版本), 刪除 DB 
    if not os.path.isfile('./last_date.pkl'):
        del_db.delete()

    client = MongoClient()
    db = client['pythondb']
    current_db = db.list_collection_names(include_system_collections=False)
    posts = db.posts

    if current_db == []:
        num = create_db.createDB(posts, dir_path, sudoPassword)
    else:
        num = update_db.update_db(posts, dir_path, sudoPassword)
    return client, posts, num, current_db

def connect_db():
    client = MongoClient()
    db = client['pythondb']
    posts = db.posts
    return posts