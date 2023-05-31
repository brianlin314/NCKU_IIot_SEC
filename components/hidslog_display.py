import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
from datetime import date
from dash import html
from database import get_db
import globals_variable
from components import hids_logtojson
import dash
import datetime

table_style = {
    "margin-left": "1rem",
    "margin-right": "1rem",
    "position":"relative",
    "left":"0.5rem",
    "top":"2rem",
    'fontsize':12,
}
# global CONFIG

def try_lambda(dic, key):
    try:
        return dic[key]
    except:
        pass

def update(id):
    posts = get_db.connect_db()
    today = date.today()
    today = today.strftime("%Y-%m-%d")

    query = {
        '$and': [
            {'agent.id': {'$eq': id}}
        ]
    }
    projection = {"_id":0, "timestamp":1, "rule.description":1, "rule.level":1, "agent.id":1, "agent.name":1} 
    data = list(posts.find(query, projection))
    df = pd.json_normalize(data)
    df = df.loc[:, ["timestamp", "rule.description", "rule.level", "agent.id", "agent.name"]]
    df[['Date', 'Time']] = df.timestamp.str.split("T", expand = True)
    df = df.drop(columns=['timestamp'])
    df = df[['Date', 'Time', 'rule.description', 'rule.level', 'agent.id', 'agent.name']]
    mask = df['Date'] == today
    df = df[mask]
    all_cols = list(df.columns)
    print(all_cols)

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
                'filter_query': '{rule.level} >= 8',
                'column_id': 'rule.level'
            },
            'backgroundColor': '#FD4000',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{rule.level} >4 && {rule.level} < 8',
                'column_id': 'rule.level'
            },
            'backgroundColor': '#F7E277',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{rule.level} <=4',
                'column_id': 'rule.level'
            },
            'backgroundColor': '#90BD3C',
            'color': 'white'
        },
        ],
        # page_action='auto',   # 後端分頁
        # page_current=0,
        page_size=30,
    )
    return table
