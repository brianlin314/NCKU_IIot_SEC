import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, callback, dash_table
import dash_html_components as html
import pandas as pd
import globals_variable
from datetime import date
import dash
from database import get_db
import re
table_style = {
    "margin-left": "1rem",
    "margin-right": "1rem",
    "position":"relative",
    "left":"0.5rem",
    "top":"2rem",
    'fontsize':12,
}

def update(ip):
    ai_result = get_db.connect_aidb()
    global df
    today = date.today()
    today = today.strftime("%Y-%m-%d")

    escaped_ip = re.escape(ip)
    query = {
        '$and': [
            {'Date': {'$eq': today}},
            {'$or': [
                {'src_ip': {'$regex': f'^{escaped_ip}'}},
                {'dst_ip': {'$regex': f'^{escaped_ip}'}}
            ]}
        ]
    }
    data = list(ai_result.find(query))
    if len(data) == 0:
        return html.H4("目前沒有資料")
    df = pd.DataFrame(data)
    df = df.drop(columns = '_id')
    df = df[['Date', 'Time', 'pred_label', 'src_ip', 'dst_ip', 'src_port', 'dst_port', 'protocol']]

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
            'border':'1px black solid',
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
                'filter_query': '{pred_label} >= 1',
                'column_id': 'pred_label'
            },
            'backgroundColor': '#FD4000',
            'color': 'white'
        },
        ]
    )
    return table
