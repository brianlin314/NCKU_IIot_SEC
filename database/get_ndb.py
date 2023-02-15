# import os
# from pymongo import MongoClient
# import glob
# import json
# from database import create_ndb, del_db, update_ndb

# def get_current_db(dir_path, sudoPassword):
#     # 當 last_date.pkl 不存在時(更新版本), 刪除 DB 
#     if not os.path.isfile('./last_date.pkl'):
#         del_db.delete()

#     client = MongoClient()
#     ndb = client['ndb']
#     current_db = ndb.list_collection_names(include_system_collections=False)
#     posts = ndb.posts

#     if current_db == []:
#         num = create_ndb.createDB(posts, dir_path, sudoPassword)
#     else:
#         num = update_ndb.update_db(posts, dir_path, sudoPassword)
#     return client, posts, num, current_db

# def connect_db():
#     client = MongoClient()
#     ndb = client['ndb']
#     posts = ndb.posts
#     return posts