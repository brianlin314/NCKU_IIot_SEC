import plotly.graph_objects as go


def calculate_cnt(startDate, endDate, ip):
    nids_logtojson.log2json(globals.nidsdirpath+"/fast.log")

    #讀取json檔, 篩選今天的log內容
    global df
    df = pd.read_json(globals.nidsdirpath+"/fast.json")

    # get the set of col_values
    set_values = posts.distinct(col_name)

    cnt = []
    for value in set_values:
        result = posts.count_documents({'$and':[{col_name:{"$in": [value]}},
                                                {'timestamp':{"$gte":startDate}},
                                                {'timestamp':{"$lte":endDate}},
                                                {'agent.id':{"$eq":id}}]})
        cnt.append(result)
    return cnt, set_values

def get_top_n(non_zero_cnt, non_zero_col, top_num):
    if len(non_zero_col) >= top_num:
        non_zero_cnt, non_zero_col = (list(t) for t in zip(*sorted(zip(non_zero_cnt, non_zero_col), reverse=True)))
        non_zero_cnt = non_zero_cnt[:top_num]
        non_zero_col = non_zero_col[:top_num]
    return non_zero_cnt, non_zero_col

def update(startDate, endDate, col_name, title, top_num, id):
    cnt, set_values = calculate_cnt(startDate, endDate, col_name, id)

    # 去除資料個數為零的
    non_zero_cnt = []
    non_zero_col = []
    for i in range(len(set_values)):
        if cnt[i] != 0:
            non_zero_cnt.append(cnt[i])
            non_zero_col.append(set_values[i])

    # 排序並取前 top_num 個
    non_zero_cnt, non_zero_col = get_top_n(non_zero_cnt, non_zero_col, top_num)

    fig = go.Figure(go.Pie(
        name = col_name,
        values = non_zero_cnt,
        labels = non_zero_col,
        text = non_zero_col,
        hovertemplate = "%{label} <br>出現次數:%{value} <br>佔比: %{percent}",
        hole=0.8,
    ))
    fig.update_layout(title_text=f"<b>{title}</b>")
    return fig