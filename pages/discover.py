import dash_bootstrap_components as dbc # 引入外部套件
import dash
import feffery_antd_components as fac
from dash import dcc, callback
from dash.dependencies import Input, Output, State, ALL
from process_time import process_time
import dash_html_components as html

import globals_variable # 引用內部函式
from components import fields, datePicker, discover_display, collapse_item, alert

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
hitNum = html.H1( # 載入完即消失
    [
        '載入資料中',
        dbc.Spinner(size="lg", spinner_style={'margin-left': '15px', 'width': '40px', 'height': '40px'}),
    ],
    style={'textAlign': 'center'}, id='dataNum'
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

def serve_layout(first):
    first, notification = alert.update_notification(first) # 會跳出更新幾筆資料

    layout = html.Div(
        [
            dbc.Row(
                [
                    fields.serve_fields(), # 左側選取field欄位

                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    datePicker.discover_date_picker(),   # live update, 調整時間
                                    notification
                                ],
                            ),

                            fac.AntdSelect( # 下拉式選取監控端點
                                id = 'dagentselect',
                                placeholder = 'Agent:',
                                options = globals_variable.hids_agent_options,
                                style=dropdown_style
                            ),
                            
                            dcc.Loading(
                                html.Div(
                                    [
                                        hitNum,
                                        dbc.Col(id = 'graph-and-table'),
                                    ],
                                ),
                            ),
                        ],
                        style=DISPLAY_STYLE,
                    ),
                ],
            ),
        ],
    )
    return first, layout

# 初始化 display or 按下 Update 按鈕的觸發事件 or 利用 fields_btn 來動態 update display
@callback(
    [
        Output('datetime-output', 'children'),
        Output('dataNum', 'children'),
        Output("graph-and-table", "children"),
    ],
    [
        Input('submit_date', 'n_clicks'), # update按鈕
        Input({'type': 'add_btn', 'index': ALL}, 'n_clicks'), # selected field 新增或刪除，選擇後會立刻更改
        Input({'type': 'del_btn', 'index': ALL}, 'n_clicks'),  # selected field 新增或刪除，選擇後會立刻更改
        Input('dagentselect', 'value'),
    ],
    [
        State('datetime-picker', 'value'), # 時間算在state，當input value出去後會跟著改變
    ]
)
def update(n_clicks, add_btn, del_btns, value, time): # dagentselect, 參數必須照input順序填入
    # 將 time 轉成 timestamp format, 並得到 interval
    startDate, endDate, freqs = process_time.get_time_info(time)
    try:
        return discover_display.update(startDate, endDate, freqs, globals_variable.agent_id[value])
    except:
        return dash.no_update, dash.no_update, dash.no_update # 若還沒選擇監控端點，是不會顯示任何值