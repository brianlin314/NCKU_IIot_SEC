import pandas as pd
import plotly.express as px

from plot import donut
from database import get_suricatadb
from process_time import process_time

def update(currentDate, freqs):
    posts = get_suricatadb.connect_db()

    intervals = list(pd.date_range(currentDate, freq=freqs))

    # 轉成 timestamp 格式s
    intervals = process_time.timestamp_format(intervals, currentDate)

    #Suricata log
    display_cols = {'_id':0}
    selected_fields = {'Time', 'Signature Id', 'Classification', 'Protocol', 'Priority', 'Source', 'Destination'}
    for key in selected_fields:
        display_cols[key] = 1
    
    # 計算 interval 中的 data 個數
    cnt = []
    for i in range(1, len(intervals[:-1])):
        result = posts.count_documents({'$and':[{'timestamp':{"$gte":intervals[i-1]}},
                                                {'timestamp':{"$lt":intervals[i]}}]})
        cnt.append(result)


    # 找到 startDate ~ endDate 之間的所有 data, 並轉成 data table 的形式
    data = posts.find({'timestamp':{"$eq":currentDate}}, display_cols)
    df = pd.json_normalize(data)

    # 若 selected_fields 有 field 沒出現在 df 中 (代表該 field 在 query 後全為空值, 所以沒出現在 df 中)
    df_columns = list(df.columns)
    empty_col = ['-' for i in range(len(df))]
    for i in range(len(selected_fields)):
        if selected_fields[i] not in df_columns:
            df.insert(loc=len(df_columns), column=selected_fields[i], value=empty_col)

    # 用 - 取代 df 中的空值
    df.fillna('-', inplace=True)

    # interval_title = process_time.interval_title
    # data = {'time':intervals[:-1]}
    # data['Count'] = cnt
    # df2 = pd.DataFrame(data)
    return df