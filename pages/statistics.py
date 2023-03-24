import dash_bootstrap_components as dbc
import dash
from dash import dcc, callback
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import dash_html_components as html

from process_time import process_time
from components import datePicker, statistics_display
import globals_variable

img_path = '../assets/img'
dropdown_style = {
    "display":"inline-block",
    "fontSize":20,
    'width': '200px',
    "position":"relative",
    "left":"1rem",
    "top":"1rem",
    "bottom":"2rem"
}

DISPLAY_STYLE = {
    "transition": "margin-left .5s",
    "margin-top": 20,
    "margin-left": "15rem",
    "margin-right": "4rem",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    "height":'10rem',
    'fontSize': 10,
    'zIndex': 1,
    'zIndex': 2,
}

COL_STYLE = {
   'width': 3,
   'textAlign': 'center',
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
                                    datePicker.st_date_picker(), # live update
                                ],
                            ),
                            fac.AntdSelect(
                                    id = 'stagentselect',
                                    placeholder='Agent:',
                                    options = globals_variable.nids_agent_options,
                                    style=dropdown_style
                            ),
                        ],
                        style=DISPLAY_STYLE,
                    ),
                ],
            ),
            dcc.Loading(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.Img(src=f'{img_path}/all.png', height="50px")),
                                        dbc.CardBody(
                                            [
                                                html.H4('Total'),
                                                html.H4('--', style={'fontSize':30, 'color':'blue'}, id='sttotal'),
                                            ],
                                        ),
                                    ],
                                ),
                                style=COL_STYLE,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.Img(src=f'{img_path}/warning.png', height="50px")),
                                        dbc.CardBody(
                                            [
                                                html.H4('High Priority Packets'),
                                                html.H4('--', style={'fontSize':30, 'color':'red'}, id='high-priority'),
                                            ],
                                        ),
                                    ],
                                ),
                                style=COL_STYLE,
                            ),
                        ],
                        style={'margin-top':20,'margin-left':'13rem','margin-right':'2rem'},
                    ),
                    dbc.Row(
                        id='stgraph-frist-row',style={'margin-left':'13rem','margin-right':'3rem'},
                    ),
                    dbc.Row(
                        id='stgraph-second-row',style={'margin-left':'13rem','margin-right':'3rem'},
                    ),
                ],
            ),
        ],
    )
    return layout

# 初始化 display or 按下 Update 按鈕的觸發事件
@callback(
    [
        Output('st-datetime-output', 'children'),
        Output('sttotal', 'children'),
        Output('high-priority', 'children'),
        Output('stgraph-frist-row', 'children'),
        Output('stgraph-second-row', 'children')
    ],
    [
        Input('st-submit_date', 'n_clicks'),
        Input('stagentselect','value')
    ],
    [
        State('st-datetime-picker', 'value')
    ]
)
def update(n_clicks, value, time):
    # 將 time 轉成 timestamp format, 並得到 interval
    startDate, endDate, freqs = process_time.get_time_info(time)
    try:
        return statistics_display.update(startDate, endDate, freqs, globals_variable.agent_ip[value])
    except:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update