import dash_bootstrap_components as dbc
from dash import callback
from dash.dependencies import Input, Output, State, ALL
import feffery_antd_components as fac
import pandas as pd
from datetime import date
import dash_html_components as html

import globals_variable
from components import hidslog_display
# components
hitNum = html.H1(
    [
        '載入資料中',
        dbc.Spinner(size="lg", spinner_style={'margin-left': '15px', 'width': '40px', 'height': '40px'}),
    ],
    style={'textAlign': 'center'}, id='dataNum'
)


dropdown_style = { # 設定背景風格
    "display":"inline-block",
    "fontSize":20,
    'width': '200px',
    "position":"relative",
    "left":"1rem",
    "top":"1rem",
    "bottom":"2rem"
}

STYLE = { # 設定背景風格
    "transition": "margin-left .5s",
    "margin-top": "2rem",
    "margin-left": "15rem",
    "margin-right": "0.5rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'zIndex':1,
    "position":"relative",
    "left":"0.5rem",
    "top":"1rem"
}

table_style = { # 設定背景風格
    "margin-right": "0.5rem",
    'width':'100%',
    'height':'500px',
    'minWidth': '100%',
    "position":"relative",
    "left":"0.5rem",
    "top":"2rem",
}

def serve_layout():
    layout = html.Div(
        [
            html.H4("Please Choose the Agent"),
            dbc.Row(
                fac.AntdSelect(
                    id = 'hagentselect',
                    placeholder='Agent:',
                    options = globals_variable.agent_options,
                    style=dropdown_style
                ),
            ),
            dbc.Row(
                html.Div(
                        id='htable'
                ),style = table_style,
            )
        ],
        style=STYLE,
    )
    return layout

@callback(
    Output('htable', 'children'),
    Input('hagentselect', 'value'),
    prevent_initial_call=True
)

def update(value):
    if(value=='Raspberry Pi'):
        id = globals_variable.agent_pi_id
    elif(value=='PC'):
        id = globals_variable.agent_pc_id
    return hidslog_display.update(id)