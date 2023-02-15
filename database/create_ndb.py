# import os
# import json
# import glob
# import pickle as pkl

# def record_last(last_date_info):
#     file = open('last_date.pkl', 'wb')
#     pkl.dump(last_date_info, file)
#     file.close()

# def change_permission(dir_path, sudoPassword):
#     paths = dir_path.split('/')
#     for i in range(2, len(paths)+1):
#         path = '/'.join(paths[:i])

#         # 若 path permission 已經為 777, 則不用改變他的 permission
#         if oct(os.stat(path).st_mode)[-3:] == '777':
#             continue

#         if i != len(paths):
#             changePermission_cmd = f"echo {sudoPassword} | sudo -S chmod 777 {path}"
#             os.system(changePermission_cmd)
#         else:
#             changePermission_cmd = f"echo {sudoPassword} | sudo -S chmod 777 -R {path}"
#             os.system(changePermission_cmd)

# def unzip(dir_path, sudoPassword):
#     gz_files = glob.glob(f'{dir_path}/**/*.json.gz', recursive=True)

#     # unzip all .json.gz files => 用 "find {dir_path} -name '*.json.gz' -exec gunzip {} +" 指令
#     # f sting 中用兩個{}, 來顯示{}
#     if len(gz_files) != 0:
#         changePermission_cmd = f"echo {sudoPassword} | sudo -S chmod 777 -R {dir_path}"
#         os.system(changePermission_cmd)
#         unzip_cmd = f"find {dir_path} -name '*.json.gz' -exec gunzip {{}} +"
#         os.system(unzip_cmd)

# def createDB(database, dir_path, sudoPassword):

#     # 更改目錄存取權限
#     change_permission(dir_path, sudoPassword)

#     # unzip json.gz files
#     unzip(dir_path, sudoPassword)

#     num = 0
#     data = []

#     f = open(dir_path+'/eve.json', 'r')
#     lines = f.readlines()
#     json_lines = [json.loads(line) for line in lines]
#     num += len(lines)

#     data += json_lines

#     database.insert_many(data)
    
#     return num