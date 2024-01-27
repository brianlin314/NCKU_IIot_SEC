import datetime
from datetime import date

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, html

from database import get_db


def data_process(id):
    posts = get_db.connect_db("hids")

    today = date.today()
    today_str = today.strftime("%Y-%m-%d")

    query = {
        'agent.id': id,
        'timestamp': {'$gte': f'{today_str}T00:00:00', '$lt': f'{today_str}T23:59:59'}
    }
    projection = {"_id": 0, "timestamp": 1, "rule.description": 1, "rule.level": 1, "agent.id": 1, "agent.name": 1} 

    data = posts.find(query, projection)
    df = pd.json_normalize(data)

    df = df.rename(columns={"timestamp": "Date_Time", "rule.description": "Rule_Description", "rule.level": "Rule_Level", "agent.id": "Agent_ID", "agent.name": "Agent_Name"})
    df[['Date', 'Time']] = pd.to_datetime(df['Date_Time']).dt.strftime('%Y-%m-%d %H:%M:%S').str.split(expand=True)
    df = df[['Date', 'Time', 'Rule_Description', 'Rule_Level', 'Agent_ID', 'Agent_Name']]

    all_cols = df.columns.tolist()

    return df, all_cols

def update(id):
    df, all_cols = data_process(id)
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
        style_cell={
            'width': '180px',
            'textAlign': 'center',
            'fontsize':12,
            'height': '30px',

        },
        style_table={
            'minWidth': '100%',
            'Width': '100%'
        },
        style_data_conditional=[
        {
            'if': {
                'filter_query': '{Rule_Level} >= 8',
                'column_id': 'Rule_Level'
            },
            'backgroundColor': '#FD4000',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{Rule_Level} >4 && {Rule_Level} < 8',
                'column_id': 'Rule_Level'
            },
            'backgroundColor': '#F7E277',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{Rule_Level} <=4',
                'column_id': 'Rule_Level'
            },
            'backgroundColor': '#90BD3C',
            'color': 'white'
        },
        ],
        page_size=30,
    )
    return table
