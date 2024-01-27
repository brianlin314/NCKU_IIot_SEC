import dash_bootstrap_components as dbc
import feffery_antd_components as fac
from dash import callback, html
from dash.dependencies import Input, Output, State

import globals_variable
from usb_data import cdbtxt2json
import get_config
import json
import pandas as pd

STYLE = { # 設定背景風格
    "transition": "margin-left .5s",
    "margin-top": "2rem",
    "margin-left": "20rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 30,
    'zIndex':1,
}

dropdown_style = { # 設定背景風格
    "display":"inline-block",
    "fontSize":30,
    "width":'300px',
    "height":"100px",
    "position":"relative",
    "left":"1rem",
    "top":"2rem"
}

def serve_layout():
    layout = html.Div(
        [
            html.P("Welcome to add Authorized USB"),
            html.Div(
                [   
                    ##############################
                    ##    User ID & Passwrd     ##
                    ##############################
                    
                    fac.AntdSpace(
                        [
                            fac.AntdCol(
                                html.Div(
                                    html.H5('Manager ID'),
                                    style = {
                                            'color':'#8EA0A5',
                                    },
                                ),
                            ),
                            fac.AntdCol(
                                html.Div(
                                    html.H5('Manager Password'),
                                    style = {
                                            'color':'#8EA0A5',
                                    },
                                ),
                            ),

                        ],
                        size = 195,
                    ),
                    fac.AntdRow(
                        fac.AntdSpace(
                            [
                                
                                fac.AntdInput(
                                    size='middle',
                                    id='input-root',
                                    placeholder='',
                                    style={
                                        'width': '200px',
                                        'marginBottom': '5px'
                                    }
                                ),
                                fac.AntdInput(
                                    id='input-password',
                                    mode='password',
                                    passwordUseMd5=True,
                                    maxLength=100,
                                    style={
                                        'width': '200px'
                                    }
                                ),
                            ],
                            size = 100,
                        ),
                    ),

                    ##############################
                    ##    USB Serial number     ##
                    ##############################
                    html.Br(),
                    fac.AntdSpace(
                        [
                            fac.AntdCol(
                                html.Div(
                                    html.H5('USB Serial Number'),
                                    style = {
                                        'color':'#8EA0A5',
                                    },
                                ),
                            ),
                            fac.AntdCol(
                                html.Div(
                                    html.H5('USB Serial Number Again'),
                                    style = {
                                        'color':'#8EA0A5',
                                    },
                                ),
                            ),
                        ],
                        size = 130,
                    ),
                    html.Br(),
                    fac.AntdSpace(
                        [
                            fac.AntdInput(
                                id='input-usbSN', #input id
                                mode='password', #隱藏所打的字
                                size='large', #調整輸入框大小
                                placeholder='輸入USB Serial Number', #輸入框裡的文字
                                style={ #css style
                                    'width': '200px',
                                    'marginBottom': '5px'
                                }
                            ),
                            fac.AntdInput(
                                id='input-usbSN-again', #input id
                                mode='password', #隱藏所打的字
                                size='large', #調整輸入框大小
                                placeholder='再次輸入USB Serial Number', #輸入框裡的文字
                                style={ #css style
                                    'width': '200px',
                                    'marginBottom': '5px'
                                }
                            ),
                        ],
                        size = 100,
                    ),
                    html.Br(),
                    html.Br(),
                    fac.AntdRow(
                        [
                            html.Div(
                                html.H5('Choose Agent'),
                                style = {
                                        'color':'#8EA0A5',
                                },
                            ),
                        ]
                    ),
                    fac.AntdRow(
                        [
                            fac.AntdSelect(
                                id='usb-select',
                                placeholder='請選擇Agent',
                                size='large',
                                options = globals_variable.usb_add_options,
                                style={
                                'width': '200px' #固定寬度
                                }
                            ),
                            fac.AntdButton(
                                children='Submit',
                                size='large',
                                type='primary',
                                id='input-button',
                            ),
                        ]
                    ),

                    html.Br(),
                    fac.AntdSpace(
                        [
                            fac.AntdText(id='output-usb-SN'), #output id
                            fac.AntdText(id='output-usb-agent')
                        ],
                        size=20
                    ),

                    html.Div(id="main-page") #為了湊齊Output
                ]
            )
        ],
        style=STYLE,
    )
    return layout

@callback(
    Output('output-usb-SN','children'),
    Output('output-usb-agent','children'),
    Output('main-page','children'),
    Input('input-button','nClicks'),
    [State('input-root','value'),
    State('input-password','value'),
    State('usb-select','value'),
    State('input-usbSN','value'),
    State('input-usbSN-again','value')],
    prevent_initial_call=True # 防止每次都讀到None
)

def callback_usb(input_button_clicks, account, password, clickedKey, input_value, input_value_again):
    check=0
    config = get_config.get_variable()
    if config['dash_user_name'] == account and config['dash_user_password'] == password:
        if input_value == input_value_again:
            #read json file and write new one
            f = open('./usb_data/usb_cdb.json', 'a+') #a代表append
            try:
                cdb_df = pd.DataFrame(json.loads(f.read()))
            except:
                cdb_df = pd.DataFrame(columns=['cdb_SN', 'Aid'])
            new_info = {"cdb_SN": input_value, "Aid": clickedKey}
            cdb_df = cdb_df.append(new_info, ignore_index=True)
            f.write(cdb_df.to_json(orient='records', lines=True))
            f.close()

            return [
                f'USB Serial Number = {input_value}',
                f'Agent = {clickedKey}',
                fac.AntdNotification(
                message='新增USB白名單通知',
                description='新增USB序列號: '+input_value+'  至Agent ID: '+clickedKey,
                type='success',
                placement = 'bottomRight')
            ]
        elif input_value != input_value_again:
            return [
                f'USB Serial Number = {input_value}',
                f'Agent = {clickedKey}',
                fac.AntdNotification(
                message='USB白名單新增失敗',
                description='2次輸入之USB序列號不同',
                type='warning',
                placement = 'bottomRight')
            ]
    else:
        return [
                f'USB Serial Number = {input_value}',
                f'Agent = {clickedKey}',
                fac.AntdNotification(
                message='帳號密碼輸入錯誤',
                description='提示:帳號密碼輸入錯誤',
                type='error',
                placement = 'bottomRight')
            ]