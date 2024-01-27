import json
import re
from datetime import date

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import callback, dash_table, dcc, html

from components import nids_logtojson
from database import get_db


def data_process(ip):
    nidsjson = get_db.connect_db('nids')
    
    today = date.today().strftime("%m/%d/%Y")
    escaped_ip = re.escape(ip)
    
    query = {
        'Date': today,
        '$or': [
            {'Source': {'$regex': f'^{escaped_ip}(:\\d{{1,5}})?$'}},
            {'Destination': {'$regex': f'^{escaped_ip}(:\\d{{1,5}})?$'}}
        ]
    }
    
    data = list(nidsjson.find(query))
    
    df = pd.DataFrame(data).astype(str).drop(columns='_id', errors='ignore')
    all_cols = df.columns.tolist()

    return df, all_cols

def update(ip):
    df, all_cols = data_process(ip)
    table = dash_table.DataTable(
        virtualization = True,
        data = df.to_dict('records'),
        columns = [{'name': column, 'id': column} for column in all_cols],
        style_header={
            'backgroundColor': '#99ABBD',
            'color': 'black',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'border':'1px black solid',
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
        page_size=30
    )
    return table
