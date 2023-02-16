import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, callback, dash_table
import dash_html_components as html
import pandas as pd
import globals_variable
from components.se_display import CONFIG
from components import nids_logtojson
from datetime import date
import datetime
import time
global CONFIG

BAR_STYLE = {'zIndex':1} #'border':'1px black solid', 

def update(startDate, endDate, freqs, ip):
    global CONFIG
    
    dateFormat = "%Y-%m-%dT%H:%M:%S.%f%z"
    starttime = datetime.datetime.strptime(startDate, dateFormat).strftime("%H:%M:%S")
    endtime = datetime.datetime.strptime(endDate, dateFormat).strftime("%H:%M:%S")
    startDate = datetime.datetime.strptime(startDate, dateFormat).strftime("%m/%d/%Y")
    endDate = datetime.datetime.strptime(endDate, dateFormat) .strftime("%m/%d/%Y")

    nids_logtojson.log2json(globals_variable.nidsdirpath+"/fast.log")

    #讀取json檔, 篩選今天的log內容
    global df
    df = pd.read_json(globals_variable.nidsdirpath+"/fast.json")
    mask = df['Destination'] == ip
    df1 = df.loc[mask]
    mask1 = df['Source'] == ip
    df2 = df.loc[mask1]
    df = pd.concat([df1,df2])
    # 若有資料
    df.insert(0, '#', [i for i in range(1, len(df)+1)])
    df['Date'] = pd.to_datetime(df['Date'])
    
    mask = (df['Date'] >=startDate) &(df['Date'] <= endDate)
    # mask1 = (df['Time'] >=starttime) &(df['Time'] <= endtime)
    df = df.loc[mask]
    # df = df.loc[mask1]
    all_cols = list(df.columns)

    # # 解決 data table 中 list 的顯示問題, 將 df 中的 list 轉成 string 用逗號隔開, 並串接在一起
    # for column in all_cols:
    #     df[column] = [', '.join(map(str, l)) if isinstance (l, list) else l for l in df[column]]

    # 根據 column 名稱長度, 自動調整 data table 的 header 寬度
    long_column_names = [{"if": {"column_id": column}, "min-width": "300px"} for column in all_cols if len(column) >= 30]
    med_column_names = [{"if": {"column_id": column}, "min-width": "225px"} for column in all_cols if (len(column) > 15 and len(column)) < 30]
    small_column_names = [{"if": {"column_id": column}, "min-width": "120px"} for column in all_cols if len(column) <= 15]

    adjusted_columns = long_column_names + med_column_names + small_column_names

    table = dash_table.DataTable(
        id = 'hdash-table',
        data=df.to_dict('records'),
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in all_cols
        ],
        virtualization=True,
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
        # 要 minWidth, maxWidth 同時設一樣, 再搭配 fixed_rows, 才能 fixed header
        style_cell={
            'textAlign': 'left',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'minWidth': 240,
            'maxWidth': 240,
            # 'whiteSpace': 'pre-line',   # 超過自動換行
        },
        fixed_rows={
            'headers': True,
            'data': 0,
        },
        style_cell_conditional=adjusted_columns,
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 248, 248)',
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'color': 'black',
            'fontWeight': 'bold',
            'textAlign': 'left',
            'border':'1px black solid',
            'minWidth': '100%',
        },
    )

    display = [
        html.Br(),
        # dbc.Row(
        #     [
        #         html.H3(f'每頁{default_page_size}筆', style={'margin-left': '15px'}, id='hpage-size'),
        #         dcc.Dropdown(value=default_page_size, clearable=False, style={'width': '35%', 'margin-left': '15px'},
        #                      options=[10, 25, 50, 100], id='hrow_drop')
        #     ]
        # ),
        table,
    ]

    return [f'從 {startDate} 到 {endDate}', display]

@callback(
    Output('hdash-table', 'style_data_conditional'),
    Input('hdash-table', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]
