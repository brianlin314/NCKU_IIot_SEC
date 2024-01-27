import dash
import dash_bootstrap_components as dbc
import feffery_antd_components as fac
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State

import globals_variable
from components import datePicker, history_display
from process_time import process_time

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

def serve_layout():
    layout = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    datePicker.date_picker("history"),   # live update
                                ],
                            ),
                            fac.AntdSelect(
                                id = 'hisagentselect',
                                placeholder='Agent:',
                                options = globals_variable.nids_agent_options,
                                style=dropdown_style
                            ),
                            dcc.Loading(
                                html.Div(
                                    [
                                        dbc.Col(id='hgraph-and-table'),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ],style = STYLE,
    )
    return layout

# 初始化 display or 按下 Update 按鈕的觸發事件 or 利用 fields_btn 來動態 update display
@callback(
    [
        Output('history-datetime-output', 'children'),
        Output("hgraph-and-table", "children"),
    ],
    [
        Input('history-submit-date', 'n_clicks'),
        Input('hisagentselect', 'value'),
    ],
    [
        State('history-datetime-picker', 'value'),
    ]
)
def update(n_clicks, value, time): 
    # 將 time 轉成 timestamp format, 並得到 interval
    startDate, endDate, _ = process_time.get_time_info(time)
    try:
        return history_display.update(startDate, endDate, globals_variable.agent_ip[value])
    except:
        return "", ""