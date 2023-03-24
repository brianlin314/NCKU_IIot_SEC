import dash_bootstrap_components as dbc
from dash import callback
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import pandas as pd
from datetime import date
import dash_html_components as html

import globals_variable
from components import ai_display

# components
hitNum = html.H1(
    [
        '載入資料中',
        dbc.Spinner(size="lg", spinner_style={'margin-left': '15px', 'width': '40px', 'height': '40px'}),
    ],
    style={'textAlign': 'center'}, id='dataNum'
)

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
    "position":"relative",
    "left":"0.5rem",
    "top":"1rem"

}

table_style = {
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
                    id = 'aagentselect',
                    placeholder='Agent:',
                    options = globals_variable.nids_agent_options,
                    style=dropdown_style
                ),
            ),
            dbc.Row(
                html.Div(
                        id='atable'
                ),style = table_style,
            )
        ],
        style=STYLE,
    )
    return layout

@callback(
    Output('atable', 'children'),
    Input('aagentselect', 'value'), # 當選擇完agent後，即callback
    prevent_initial_call=True # to prevent callbacks from firing when their inputs initially appear in the layout of your Dash application.
)

def update(value):
    ip = globals_variable.agent_ip[value]
    return ai_display.update(ip)