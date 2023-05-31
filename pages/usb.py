import dash_bootstrap_components as dbc
import feffery_antd_components as fac
import dash
from dash_extensions import Lottie
from dash import dcc, callback
from dash.dependencies import Input, Output, State, ALL
from datetime import date
from dash import html

import pandas as pd
import globals_variable
from components import usblog_display

# components
img_path = './assets/img'
hitNum = html.H1(
    [
        '載入資料中',
        dbc.Spinner(size="lg", spinner_style={'margin-left': '15px', 'width': '40px', 'height': '40px'}),
    ],
    style={'textAlign': 'center'}, id='dataNum'
)

COL_STYLE = {
   'width': 3,
   'textAlign': 'center',
}

dropdown_style = {
    "display":"inline-block",
    "fontSize":20,
    'width': '200px',
    "position":"relative",
    "left":"1rem",
    "top":"1rem",
    "bottom":"2rem"
}

STYLE = {
    "transition": "margin-left .5s",
    "margin-top": "2rem",
    "margin-left": "15rem",
    "margin-right": "0.5rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'zIndex':1,
    'height':1000,
    "position":"relative",
    "left":"0.5rem",
    "top":"1rem"

}

table_style = {
    "margin-right": "0.5rem",
    'width':'100%',
    'height':500,
    'minWidth': '100%',
    'minHeight': '100%',
    "position":"relative",
    "left":"4.75rem",
    "top":"2rem",
}

def serve_layout():
    layout = html.Div(
        [
            html.H4("Please Choose the Agent"),
            dbc.Row(
                dbc.Col(
                    fac.AntdSelect( # 下拉式選取監控端點
                        id = 'uagentselect',
                        placeholder = 'Agent:',
                        options = globals_variable.hids_agent_options,
                        style = dropdown_style
                    ),
                ),
            ),
            dcc.Loading(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.Img(src = f'{img_path}/check.png', height = "50px")),
                                        dbc.CardBody(
                                            [
                                                html.H4('Authorized Using USB'),
                                                html.H4('--', style = {'fontSize':30, 'color':'blue'}, id = 'AUSB'),
                                            ],
                                        ),
                                    ],
                                ),
                                style=COL_STYLE,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.Img(src = f'{img_path}/warning.png', height = "50px")),
                                        dbc.CardBody(
                                            [
                                                html.H4('Unauthorized Using USB'),
                                                html.H4('--', style = {'fontSize':30, 'color':'blue'}, id = 'UUSB'),
                                            ],
                                        ),
                                    ],
                                ),
                                style=COL_STYLE,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.Img(src = f'{img_path}/usb-port.png', height = "50px")),
                                        dbc.CardBody(
                                            [
                                                html.H4('Total Using Port'),
                                                html.H4('--', style = {'fontSize':30, 'color':'blue'}, id = 'Total'),
                                            ],
                                        ),
                                    ],
                                ),
                                style = COL_STYLE,
                            ),
                        ],
                        style={'margin-top':30, 'margin-left':'3rem', 'margin-right':'3rem'},
                    ),
                    dbc.Row(
                        html.Div(
                            id='utable'
                        )
                        ,style = table_style,
                    ),
                ],
            ),
        ],
        style=STYLE,
    )
    return layout

@callback(
    Output('AUSB', 'children'),
    Output('UUSB', 'children'),
    Output('Total', 'children'),
    Output('utable', 'children'),
    Input('uagentselect', 'value'),
    prevent_initial_call=True
)

def update(value):
    try:
        return usblog_display.update(globals_variable.agent_id[value])
    except:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update