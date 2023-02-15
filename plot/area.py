import pandas as pd
import plotly.express as px

from database import get_db
from process_time import process_time

def update(startDate, endDate, col_name, freqs, title, id):
    interval_title = process_time.interval_title
    drop_null = {col_name:{"$exists": True}}
    display_cols = {'_id':0, col_name:1}

    # connect to database
    posts = get_db.connect_db()

    # get the set of col_values
    set_values = posts.distinct('rule.level')

    # 根據 interval 切割 startDate ~ endDate
    intervals = list(pd.date_range(startDate, endDate, freq=freqs))
    intervals = process_time.timestamp_format(intervals, endDate) # 轉成 timestamp 格式

    cnt = [[] for i in range(len(set_values))]
    dic = {set_values[i]:i for i in range(len(set_values))}

    for i in range(1, len(intervals[:-1])):
        for value in set_values:
            result = posts.count_documents({'$and':[{'timestamp':{"$gte":intervals[i-1]}},
                                                    {'timestamp':{"$lt":intervals[i]}},
                                                    {col_name:value},
                                                    {'agent.id':{"$eq":id}}]})
            cnt[dic[value]].append(result)

    for value in set_values:
        result = posts.count_documents({'$and':[{'timestamp':{"$gt":intervals[-2]}},
                                                {'timestamp':{"$lte":intervals[-1]}},
                                                {col_name:value},
                                                {'agent.id':{"$eq":id}}]})
        cnt[dic[value]].append(result)

    # 去除資料個數為零的
    non_zero_cnt = []
    non_zero_col = []
    for i in range(len(set_values)):
        if sum(cnt[i]) != 0:
            non_zero_cnt.append(cnt[i])
            non_zero_col.append(set_values[i])

    data = {'time':intervals[:-1]}
    for i in range(len(non_zero_col)):
        data[non_zero_col[i]] = non_zero_cnt[i]
    df = pd.DataFrame(data)

    fig=px.area(df, x="time", y=non_zero_col, title=f"<b>{title}</b>", hover_data={"time":False},
              labels={"time":f"<b>timestamp per {interval_title[freqs]}</b>", "value": "<b>Count</b>", "variable": col_name}
        )
    fig.update_layout(hovermode="x unified")
    return fig