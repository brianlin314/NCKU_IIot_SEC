import dash_bootstrap_components as dbc
import dash
from dash import dcc, callback
from dash.dependencies import Input, Output, State
from dash_extensions import Lottie
import feffery_antd_components as fac
from process_time import process_time
from components import datePicker, se_display, alert
import globals_variable
from dash import html

options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
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

def serve_layout(first):
    first, notification = alert.update_notification(first)

    layout = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    datePicker.se_date_picker(), # live update
                                    notification,
                                ],
                            ),
                            fac.AntdSelect(
                                    id = 'seagentselect',
                                    placeholder='Agent:',
                                    options=globals_variable.hids_agent_options,
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
                                        dbc.CardHeader(Lottie(options=options, width="23%", height="23%", url="/total", speed=2.01)),
                                        dbc.CardBody(
                                            [
                                                html.H4('Total'),
                                                html.H4('--', style={'fontSize':30, 'color':'blue'}, id='total'),
                                            ],
                                        ),
                                    ],
                                ),
                                style=COL_STYLE,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(Lottie(options=options, width="15%", height="15%", url="/alert", speed=1.01)),
                                        dbc.CardBody(
                                            [
                                                html.H4('Level 12 or above alerts'),
                                                html.H4('--', style={'fontSize':30, 'color':'red'}, id='level12'),
                                            ],
                                        ),
                                    ],
                                ),
                                style=COL_STYLE,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(Lottie(options=options, width="17%", height="17%", url="/failure", speed=0.551)),
                                        dbc.CardBody(
                                            [
                                                html.H4('Authentication failure'),
                                                html.H4('--', style={'fontSize':30, 'color':'red'}, id='fail'),
                                            ],
                                        ),
                                    ],
                                ),
                                style=COL_STYLE,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(Lottie(options=options, width="17%", height="17%", url="/success", speed=0.81)),
                                        dbc.CardBody(
                                            [
                                                html.H4('Authentication success'),
                                                html.H4('--', style={'fontSize':30, 'color':'green'}, id='success'),
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
                        id='graph-frist-row',style={'margin-left':'13rem','margin-right':'3rem'},
                    ),
                    dbc.Row(
                        id='graph-second-row',style={'margin-left':'13rem','margin-right':'3rem'},
                    ),
                ],
            ),
        ],
    )
    return first, layout

# 初始化 display or 按下 Update 按鈕的觸發事件
@callback(
    [
        Output('se-datetime-output', 'children'),
        Output('total', 'children'),
        Output('level12', 'children'),
        Output('fail', 'children'),
        Output('success', 'children'),
        Output('graph-frist-row', 'children'),
        Output('graph-second-row', 'children'),
    ],
    [
        Input('se-submit_date', 'n_clicks'),
        Input('seagentselect','value')
    ],
    [
        State('se-datetime-picker', 'value')
    ]
)

def update(n_clicks, value, time):
    # 將 time 轉成 timestamp format, 並得到 interval
    startDate, endDate, freqs = process_time.get_time_info(time)
    try:
        print("security event已經取得資料",globals_variable.agent_id[value])
        return se_display.update(startDate, endDate, freqs, globals_variable.agent_id[value])
    except:
        print("security event未取得資料")
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
