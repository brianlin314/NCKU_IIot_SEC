import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
import json
from pandas import json_normalize
from datetime import date
import dash_html_components as html
import os

import globals_variable
from components import hids_logtojson

table_style = {
    "margin-left": "1rem",
    "margin-right": "1rem",
    "position":"relative",
    "left":"0.5rem",
    "top":"2rem",
    'fontsize':12,
}
# global CONFIG

def update(id):
    cmd = 'sudo chmod  777 -R /var/ossec/logs/alerts/' # 更改wazuh 底下資料夾權限
    password = globals_variable.sudoPassword
    os.system('echo %s | sudo -S %s' % (password, cmd))
    today = date.today()
    todate = today.strftime("%Y/%m/%d")
    #在server上需要取消註解這行 ：
    # 使用strftime將日期格式轉成我們想要的格式
    hids_logtojson.log2json(globals_variable.hidsdirpath+str(today.year)+'/'+today.strftime("%b")+'/ossec-alerts-'+str(today.day).zfill(2)+'.json')
    #讀取json檔, 篩選今天的log內容
    global df, df_
    df = pd.read_json(open(globals_variable.hidsdirpath+str(today.year)+'/'+today.strftime("%b")+'/ossec-alerts-'+str(today.day).zfill(2)+'_1.json', "r", encoding="utf8"))
    if len(df) == 0:
        return html.H3("該時段無資料可顯示，請檢查ip位址是否設定正確!")
    #在server上需要改 ： open(globals.hidsdirpath+'/'+today.year+'/'+today.strftime("%b")+'/ossec-alerts-'+today.day+'.json'
    df = df.loc[:, ["timestamp", "rule", "agent"]]
    df_=pd.DataFrame()
    df_['Date'] = df['timestamp'].apply(lambda x: x.strftime("%Y/%m/%d"))
    df_['Time'] = df['timestamp'].apply(lambda x: x.strftime("%H:%M:%S"))
    df_['Agent_ID'] = df['agent'].apply(lambda x: x['id'])
    df_['Agent'] = df['agent'].apply(lambda x: x['name'])
    df_['Event'] = df['rule'].apply(lambda x: x['description'])
    df_['Level'] = df['rule'].apply(lambda x: x['level'])
    df_= df_.sort_values(by='Time',ascending=False)
    del df
    df = df_
    df = df[((df['Date'] == todate) & (df['Agent_ID'] == id))]
    all_cols = list(df.columns)

    table = dash_table.DataTable(
        virtualization=True,
        data=df.to_dict('records'),
        columns=[{'name': column, 'id': column} for column in all_cols],
        style_header={
            'backgroundColor': '#99ABBD',
            'color': 'black',
            'fontWeight': 'bold',
            'textAlign': 'center',
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell={
            'width': '180px',
            'textAlign': 'center',
            'fontsize':12,
            'height': 'auto',

        },
        style_table={
            'minWidth': '100%',
            'Width': '100%'
        },
        style_data_conditional=[
        {
            'if': {
                'filter_query': '{Level} >= 8',
                'column_id': 'Level'
            },
            'backgroundColor': '#FD4000',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{Level} >4 && {Level} < 8',
                'column_id': 'Level'
            },
            'backgroundColor': '#F7E277',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{Level} <=4',
                'column_id': 'Level'
            },
            'backgroundColor': '#90BD3C',
            'color': 'white'
        },
        ],
    )
    return table
