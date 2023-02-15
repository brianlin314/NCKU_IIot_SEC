import os
import json
import glob
import pickle as pkl

def record_last(last_date_info):
    file = open('last_date.pkl', 'wb')
    pkl.dump(last_date_info, file)
    file.close()

def change_permission(dir_path, sudoPassword):
    paths = dir_path.split('/')
    for i in range(2, len(paths)+1):
        path = '/'.join(paths[:i])

        # 若 path permission 已經為 777, 則不用改變他的 permission
        if oct(os.stat(path).st_mode)[-3:] == '777':
            continue

        if i != len(paths):
            changePermission_cmd = f"echo {sudoPassword} | sudo -S chmod 777 {path}"
            os.system(changePermission_cmd)
        else:
            changePermission_cmd = f"echo {sudoPassword} | sudo -S chmod 777 -R {path}"
            os.system(changePermission_cmd)

def unzip(dir_path, sudoPassword):
    gz_files = glob.glob(f'{dir_path}/**/*.json.gz', recursive=True)

    # unzip all .json.gz files => 用 "find {dir_path} -name '*.json.gz' -exec gunzip {} +" 指令
    # f sting 中用兩個{}, 來顯示{}
    if len(gz_files) != 0:
        changePermission_cmd = f"echo {sudoPassword} | sudo -S chmod 777 -R {dir_path}"
        os.system(changePermission_cmd)
        unzip_cmd = f"find {dir_path} -name '*.json.gz' -exec gunzip {{}} +"
        os.system(unzip_cmd)

def createDB(database, dir_path, sudoPassword):

    # 更改目錄存取權限
    change_permission(dir_path, sudoPassword)

    # unzip json.gz files
    unzip(dir_path, sudoPassword)

    # 找出年份(2000~2099)的資料夾, 並由小到大排序
    targetPattern = "20[0-9][0-9]"
    years = sorted(glob.glob(f'{dir_path}/{targetPattern}'))

    months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
    ]

    month_dict = {}
    for i in range(len(months)):
        month_dict[months[i]] = i + 1

    num = 0
    data = []
    error_file = ''
    json_files = []
    for year_ in years:
        # 按照月份存取
        for month in months:
            json_files = sorted(glob.glob(f'{year_}/{month}/*.json'))  # 找出所有日期的 .json files, 並由小到大排序
            for i in range(len(json_files)):
                f = open(json_files[i], 'r')
                lines = f.readlines()

                # 紀錄每月最後有資料的日期, data數目 => 紀錄 last date info
                if i == len(json_files)-1:
                    day = json_files[i].split('.')[-2].split('-')[-1]
                    last_date_info = [f'{year_}-{month_dict[month]}-{day}', len(lines)]
                    record_last(last_date_info)
                try:
                    json_lines = [json.loads(line) for line in lines]
                    num += len(lines)
                except:
                    error_file = json_files[i]
                data += json_lines
                # print(f'{json_files[i]} 有 {len(lines)} 筆資料')
    try:
        database.insert_many(data) # insert data into mongoDB
    except:
        print(f'重新 insert {error_file}')
        f = open(error_file, 'r')
        lines = f.readlines()
        json_lines = [json.loads(line) for line in lines]
        num += len(lines)
        database.insert_many(json_lines)
    return num