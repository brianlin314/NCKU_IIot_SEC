# import pandas as pd
# import plotly.express as px

# from plot import donut
# from database import get_ndb
# from process_time import process_time

# def update(startDate, endDate, freqs, selected_fields, ip):
#     # connect to database
#     posts = get_ndb.connect_db()
#     # 根據 interval 切割 startDate ~ endDate
#     intervals = list(pd.date_range(startDate, endDate, freq=freqs))

#     # 將 selected_fields 做標記, 等等會送入 database 做查詢(若 fields 為空, table 顯示所有 fields)
#     # => 因為 display_cols = {'_id':0}, 會 query 除了 '_id' 以外的所有 cols
#     display_cols = {'_id':0}
#     for key in selected_fields:
#         display_cols[key] = 1

#     # 轉成 timestamp 格式
#     intervals = process_time.timestamp_format(intervals, endDate)

#     # 計算 interval 中的 data 個數
#     cnt = []
#     for i in range(1, len(intervals[:-1])):
#         result = posts.count_documents({'$and':[{'timestamp':{"$gte":intervals[i-1]}},
#                                                 {'timestamp':{"$lt":intervals[i]}}]})
#         cnt.append(result)

#     # 特殊處理無法被完美切割的最後一個 interval
#     result = posts.count_documents({'$and':[{'timestamp':{"$gt":intervals[-2]}},
#                                             {'timestamp':{"$lte":intervals[-1]}}]})
#     cnt.append(result)

#     # 找到 startDate ~ endDate 之間的所有 data, 並轉成 data table 的形式
#     data = posts.find({'$and':[{'timestamp':{"$gte":startDate}},
#                                {'timestamp':{"$lte":endDate}},
#                                {'$or':[{"Src ip":{"$eq":ip}},{"Dst ip":{"$eq":ip}}]}]}, display_cols)
#     df = pd.json_normalize(data)

#     # 若 selected_fields 有 field 沒出現在 df 中 (代表該 field 在 query 後全為空值, 所以沒出現在 df 中)
#     df_columns = list(df.columns)
#     empty_col = ['-' for i in range(len(df))]
#     for i in range(len(selected_fields)):
#         if selected_fields[i] not in df_columns:
#             df.insert(loc=len(df_columns), column=selected_fields[i], value=empty_col)

#     # 用 - 取代 df 中的空值
#     df.fillna('-', inplace=True)

#     interval_title = process_time.interval_title
#     data = {'time':intervals[:-1]}
#     data['Count'] = cnt
#     df2 = pd.DataFrame(data)

#     fig = px.bar(df2, x='time', y='Count', hover_data={"time":False},
#                 labels={'time': f'<b>timestamp per {interval_title[freqs]}</b>', 'Count':'<b>Count</b>'})
#     fig.update_layout(hovermode="x unified")

#     return fig, df