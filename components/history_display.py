import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, callback, dash_table
from dash import html
import pandas as pd
import globals_variable
from components.se_display import CONFIG
import datetime
import time
import re
from database import get_db
global CONFIG

BAR_STYLE = {'zIndex':1} #'border':'1px black solid', 

def update(startDate, endDate, freqs, ip):
    global CONFIG
    dateFormat = "%Y-%m-%dT%H:%M:%S.%f%z"
    starttime = datetime.datetime.strptime(startDate, dateFormat).strftime("%H:%M:%S")
    endtime = datetime.datetime.strptime(endDate, dateFormat).strftime("%H:%M:%S")
    startDate = datetime.datetime.strptime(startDate, dateFormat).strftime("%m/%d/%Y")
    endDate = datetime.datetime.strptime(endDate, dateFormat) .strftime("%m/%d/%Y")

    nidsjson = get_db.connect_db('nids')
    escaped_ip = re.escape(ip)
    print(startDate, endDate)
    query = {
        '$or': [
            {'$and': [
                {'Date': startDate},
                {'Time': {'$gte': starttime}},
                {'$or':[{'Source': {'$regex': f'^{escaped_ip}(:\\d{{1,5}})?$'}},
                        {'Destination': {'$regex': f'^{escaped_ip}(:\\d{{1,5}})?$'}}]}
            ]},
            {'$and': [
                {'Date': endDate},
                {'Time': {'$lte': endtime}},
                {'$or':[{'Source': {'$regex': f'^{escaped_ip}(:\\d{{1,5}})?$'}},
                        {'Destination': {'$regex': f'^{escaped_ip}(:\\d{{1,5}})?$'}}]}
            ]},
            {'$and': [
                {'Date': {'$gt': startDate, '$lt': endDate}},
                {'$or':[{'Source': {'$regex': f'^{escaped_ip}(:\\d{{1,5}})?$'}},
                        {'Destination': {'$regex': f'^{escaped_ip}(:\\d{{1,5}})?$'}}]}
            ]},
        ]
    }
    data = list(nidsjson.find(query))
    df = pd.DataFrame(data)
    df = df.drop(columns = '_id')
    all_cols = list(df.columns)

    table = dash_table.DataTable(
        virtualization = True,
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        filter_action="native",
        page_action="native",
        page_current= 0,
        page_size= 50,
        data = df.to_dict('records'),
        columns = [{'name': column, 'id': column, "deletable": True, "selectable": True} for column in all_cols],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'color': 'black',
            'fontWeight': 'bold',
            'textAlign': 'left',
            'border':'1px black solid',
            'minWidth': '100%',
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
        fixed_rows={
            'headers': True,
            'data': 0,
        },
    )
    
    display = [
        html.Br(),
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
