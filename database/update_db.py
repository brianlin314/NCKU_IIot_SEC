import json
import pickle as pkl
from datetime import datetime, timedelta

from database import create_db

# generator
def gen_dates(start, days):
    day = timedelta(days=1)
    for offset in range(days):
        yield start + (day * offset)

def get_date_list(start, end):
    dateFormat = "%Y-%m-%d"
    start = datetime.strptime(start, dateFormat).date()
    end = datetime.strptime(end, dateFormat).date()
    dates = []
    for date in gen_dates(start, (end-start).days+1): # +1 是把 endDate 加進去 lst 中
        dates.append(str(date))
    return dates

def get_time_info(time):
    year, month, day = time.split('-')
    return year, month, day

def update_db(posts, dir_path, sudoPassword):
    create_db.change_permission(dir_path, sudoPassword)
    create_db.unzip(dir_path, sudoPassword)

    file = open('last_date.pkl', 'rb')
    last_time, last_cnt = pkl.load(file)
    # print(last_time, last_cnt)

    dateFormat = '%Y-%m-%d'
    now = datetime.now().date()
    now_time = datetime.strftime(now, dateFormat)

    months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
    ]

    convert_month = {}
    for i in range(len(months)):
        convert_month[str(i+1).zfill(2)] = months[i]
    last_time =  last_time.split('/')[-1]
    dates_lst = get_date_list(last_time, now_time)

    # 特殊處理上次更新的最後一天
    data = []
    last_y, last_m, last_d = get_time_info(dates_lst[0])
    f = open(f'{dir_path}/{last_y}/{convert_month[last_m]}/ossec-alerts-{last_d}.json', 'r')
    lines = f.readlines()
    update_lines = lines[last_cnt:]
    try:
        json_lines = [json.loads(line) for line in update_lines]
        data += json_lines
    except:
        pass
    # print(f'{dates_lst[0]} 新增{len(json_lines)}筆')

    # 更新 last date info
    last_date_info = [last_time, len(lines)]
    create_db.record_last(last_date_info)

    # 更新其他天的資料
    for date in dates_lst[1:]:
        year, month, day = get_time_info(date)
        try:
            f = open(f'{dir_path}/{year}/{convert_month[month]}/ossec-alerts-{day}.json', 'r')
            lines = f.readlines()

            # 更新 last date info
            last_date_info = [f'{year}-{month}-{day}', len(lines)]
            create_db.record_last(last_date_info)

            json_lines = [json.loads(line) for line in lines]
            data += json_lines
        except:
            pass
            # print(f'{date} 沒有資料')

    # print('-' * 25)
    num = 0
    if data == []:
        pass
        # print('沒有要新增的資料')
    else:
        num = len(data)
        posts.insert_many(data) # insert data into mongoDB
        print(f'新增{len(data)}筆資料')
    return num