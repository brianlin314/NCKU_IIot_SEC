import dash_bootstrap_components as dbc
from dash import dcc, callback
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import dash
import dash_html_components as html

import globals
from process_time import process_time
from components import datePicker, history_display

dropdown_style = {
    "display":"inline-block",
    "fontSize":20,
    'width': '200px',
    "position":"relative",
    "left":"1rem",
    "top":"1rem",
    "bottom":"2rem"
}
# components
hitNum = html.H1(
    [
        '載入資料中',
        dbc.Spinner(size="lg", spinner_style={'margin-left': '15px', 'width': '40px', 'height': '40px'}),
    ],
    style={'textAlign': 'center'}, id='hdataNum'
)

DISPLAY_STYLE = {
    "transition": "margin-left .5s",
    "margin-top": 20,
    "margin-right": 30,
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 12,
    'width': '1px',
    'zIndex':1,
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
                                    datePicker.his_date_picker(),   # live update
                                ],
                            ),
                            fac.AntdSelect(
                                id = 'hisagentselect',
                                placeholder='Agent:',
                                options = globals.agent_options,
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
        Output('hdatetime-output', 'children'),
        Output("hgraph-and-table", "children"),
    ],
    [
        Input('hsubmit_date', 'n_clicks'),
        Input('hisagentselect', 'value'),
    ],
    [
        State('hdatetime-picker', 'value'),
    ]
)
def update(n_clicks, value, time): 
    # 將 time 轉成 timestamp format, 並得到 interval
    startDate, endDate, freqs = process_time.get_time_info(time)
    if(value=='Raspberry Pi'):
        return history_display.update(startDate, endDate, freqs, globals.agent_pi_ip)
    elif(value=='PC'):
        return history_display.update(startDate, endDate, freqs, globals.agent_pc_ip)
    return dash.no_update, dash.no_update