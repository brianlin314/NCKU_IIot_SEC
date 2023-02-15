# import json
# import pickle as pkl
# from datetime import datetime, timedelta

# from database import create_ndb

# # generator
# def gen_dates(start, days):
#     day = timedelta(days=1)
#     for offset in range(days):
#         yield start + (day * offset)

# def get_date_list(start, end):
#     dateFormat = "%Y-%m-%d"
#     start = datetime.strptime(start, dateFormat).date()
#     end = datetime.strptime(end, dateFormat).date()
#     dates = []
#     for date in gen_dates(start, (end-start).days+1): # +1 是把 endDate 加進去 lst 中
#         dates.append(str(date))
#     return dates

# def get_time_info(time):
#     year, month, day = time.split('-')
#     return year, month, day

# def update_db(posts, dir_path, sudoPassword):
#     create_ndb.change_permission(dir_path, sudoPassword)
#     create_ndb.unzip(dir_path, sudoPassword)

#     file = open('last_date.pkl', 'rb')
#     last_time, last_cnt = pkl.load(file)
#     # print(last_time, last_cnt)

#     # 特殊處理上次更新的最後一天
#     data = []
#     #f = open(f'{dir_path}/{last_y}/{convert_month[last_m]}/ossec-alerts-{last_d}.json', 'r') #suricata路徑
#     f = open(f'{dir_path}/eve.json', 'r')
#     lines = f.readlines()
#     update_lines = lines[last_cnt:]
#     try:
#         json_lines = [json.loads(line) for line in update_lines]
#         data += json_lines
#     except:
#         pass
#     # print(f'{dates_lst[0]} 新增{len(json_lines)}筆')

#     # 更新 last date info
#     last_date_info = [last_time, len(lines)]
#     create_ndb.record_last(last_date_info)

#     # print('-' * 25)
#     num = 0
#     if data == []:
#         pass
#         # print('沒有要新增的資料')
#     else:
#         num = len(data)
#         posts.insert_many(data) # insert data into mongoDB
#         print(f'新增{len(data)}筆資料')
#     return num