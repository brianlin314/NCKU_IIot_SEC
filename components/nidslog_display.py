import dash_bootstrap_components as dbc
from dash import dcc, callback, dash_table
import pandas as pd
import json
from pandas import json_normalize
from datetime import date
import dash_html_components as html
import os
import dash
import globals_variable
from components import nids_logtojson
from database import get_db
import pprint
import re

table_style = {
    "margi n-left": "1rem",
    "margin-right": "1rem",
    "position":"relative",
    "left":"0.5rem",
    "top":"5rem",
    'fontsize':12,
}


# global CONFIG

def update(ip):
    nidsjson = get_db.connect_nidsdb()
    today = date.today()
    today = today.strftime("%m/%d/%Y")

    escaped_ip = re.escape(ip)
    query = {
        '$and': [
            {'Date': {'$eq': today}},
            {'$or': [
                {'Source': {'$regex': f'^{escaped_ip}(:\\d{{1,5}})?$'}},
                {'Destination': {'$regex': f'^{escaped_ip}(:\\d{{1,5}})?$'}}
            ]}
        ]
    }
    data = list(nidsjson.find(query))
    df = pd.DataFrame(data)
    df = df.drop(columns = '_id')
    all_cols = list(df.columns)
    table = dash_table.DataTable(
        virtualization = True,
        data = df.to_dict('records'),
        columns = [{'name': column, 'id': column} for column in all_cols],
        page_size = 8,
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
        }
    )
    return table
