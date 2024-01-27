from datetime import date

import dash
import dash_bootstrap_components as dbc
import feffery_antd_components as fac
import pandas as pd
from dash import callback, dcc, html
from dash.dependencies import ALL, Input, Output, State

import globals_variable
from components import nids_logtojson, nidslog_display

# components

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
    "top":"10rem",
}

def serve_layout():
    layout = html.Div(
        [
            html.H4("Please Choose the Agent"),
            dbc.Row(
                fac.AntdSelect(
                    id = 'agentselect',
                    placeholder='Agent:',
                    options = globals_variable.nids_agent_options,
                    style=dropdown_style
                ),
            ),
            html.Br(),
            dcc.Loading(
                html.Div(
                    [
                        dbc.Col(id='nids_log_table'),
                    ],
                ),style = table_style,
            )
        ],
        style=STYLE,
    )
    return layout

@callback(
    Output('nids_log_table', 'children'),
    Input('agentselect', 'value'),
    prevent_initial_call=True
)

def update(value):
    try:
        return nidslog_display.update(globals_variable.agent_ip[value])
    except:
        return ""