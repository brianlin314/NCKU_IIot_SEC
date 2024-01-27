import json
from datetime import date

import dash
import dash_bootstrap_components as dbc
import feffery_antd_components as fac
import pandas as pd
from dash import dash_table, html
from pandas import json_normalize

from usb_data import usb


def update(id):
    usb.usbdf()
    #讀取json檔, 篩選今天的log內
    global df
    df = pd.read_json("./usb_data/usb_info.json")
    if len(df)==0:
        return [dash.no_update, dash.no_update, dash.no_update, html.H3("目前無USB連接在偵測裝置上")]

    id = int(id)
    df = df[(df["agent_id"] == id)]
    try:
        df['In_Time'] = df['In_Time'].apply(lambda x: x.strftime("%H:%M:%S"))
        df['Out_Time'] = df['Out_Time'].apply(lambda x: x.strftime("%H:%M:%S"))
    except:
        print(id)
    AUSB = df[((df['authorized'] == 'white')&(df['connected'] == 1))].shape[0]
    UUSB = df[((df['authorized'] == 'black')&(df['connected'] == 1))].shape[0]
    Total=  df[(df['connected'] == 1)].shape[0]
    all_cols = list(df.columns)
    table = dash_table.DataTable(
        virtualization=True,
        data=df.to_dict('records'),
        columns=[{'name': column, 'id': column} for column in all_cols],
        fixed_rows={'headers': True},
        style_header={
            'backgroundColor': '#99ABBD',
            'color': 'black',
            'fontWeight': 'bold',
            'textAlign': 'center',
        },
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{authorized} = "black"',
                    'column_id': 'authorized'
                },
                'backgroundColor': '#FD4000',
                'color': 'white'
            },
        ],
        style_cell={
            'width': '180px',
            'textAlign': 'center',
            'fontsize':12,
            'height': 'auto',
        },
        style_table={"height":2000, "width":"1445px"},
    )
    return [AUSB, UUSB, Total, table]
