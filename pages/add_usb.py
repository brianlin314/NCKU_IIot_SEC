import dash_bootstrap_components as dbc
from dash import callback
import feffery_antd_components as fac  
from dash.dependencies import Input, Output, State
import dash_html_components as html

import ast
from usb_data import cdbtxt2json

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
                    fac.AntdRow(
                        [
                            html.Div(
                                fac.AntdText('輸入使用者帳號', code=True),
                                style={
                                    'width': '170px',
                                    "font-size": '24px',
                                    'color':'#0E79E1',
                                }
                            ),
                            fac.AntdInput(
                                id='input-root', #input id
                                size='large', #調整輸入框大小
                                placeholder='輸入使用者名稱', #輸入框裡的文字
                                #addonAfter='輸入USB Serial Number', #輸入框前的文字
                                style={ #css style
                                    'width': '300px',
                                    'marginBottom': '5px',
                                }
                            )
                        ]
                    ),

                    html.Br(),
                    fac.AntdRow(
                        [   
                            html.Div(
                                fac.AntdText('輸入使用者密碼', code=True),
                                style={
                                    'width': '170px',
                                    "font-size": '24px',
                                    'color':'#0E79E1',
                                }
                            ),
                            fac.AntdInput(
                                id='input-password', #input id
                                mode='password', #隱藏所打的字
                                size='large', #調整輸入框大小
                                placeholder='輸入使用者密碼', #輸入框裡的文字
                                #addonAfter='輸入USB Serial Number', #輸入框前的文字
                                style={ #css style
                                    'width': '300px',
                                    'marginBottom': '5px'
                                }
                            )
                        ]
                    ),

                    html.Br(),
                    fac.AntdRow(
                        [
                            html.Div(
                                fac.AntdText('輸入USB序列號', code=True),
                                style={
                                    'width': '170px',
                                    "font-size": '24px',
                                    'color':'#0E79E1',
                                }
                            ),

                            fac.AntdInput(
                                id='input-usbSN', #input id
                                mode='password', #隱藏所打的字
                                size='large', #調整輸入框大小
                                placeholder='輸入USB Serial Number', #輸入框裡的文字
                                style={ #css style
                                    'width': '300px',
                                    'marginBottom': '5px'
                                }
                            )
                        ]
                    ),

                    html.Br(),
                    fac.AntdRow(
                        [
                            html.Div(
                                fac.AntdText('重新輸入序列號', code=True),
                                style={
                                    'width': '170px',
                                    "font-size": '24px',
                                    'color':'#0E79E1',
                                }
                            ),

                            fac.AntdInput(
                                id='input-usbSN-again', #input id
                                mode='password', #隱藏所打的字
                                size='large', #調整輸入框大小
                                placeholder='再次確認USB Serial Number', #輸入框裡的文字
                                style={ #css style
                                    'width': '300px',
                                    'marginBottom': '5px'
                                }
                            )
                        ]
                    ),

                    html.Br(),
                    fac.AntdRow(
                        [
                            html.Div(
                                fac.AntdText('請選擇Agent', code=True),
                                style={
                                    'width': '170px',
                                    "font-size": '24px',
                                    'color':'#0E79E1',
                                }
                            ),
                            fac.AntdSelect(
                                id='usb-select',
                                placeholder='請選擇Agent',
                                size='large',
                                options=[
                                    {'label':'PC','value':'004'},
                                    {'label':'Raspberry pi','value':'003'},
                                    {'label':'Laptop','value':'009','disabled': True},
                                    {'label':'CNC','value':'008','disabled': True}
                                ],
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

def callback_usb(input_button_clicks, account, password, clickedKey, input_value, input_value_again): #第一個參數是Input的參數，第二個是State的參數,參數必須照順序填入
    check=0
    auth=open('./usb_data/manager.json','r')
    lines=auth.readlines()
    for line in lines:
        line = ast.literal_eval(line)
        if line['manager'] == account:
            if line['password']==password:
                if input_value == input_value_again:
                    cdb_list=input_value+" "+clickedKey
                    with open('./usb_data/cdb.txt', 'a') as f: #a代表append
                        f.write(cdb_list)
                        f.write('\n')
                    f.close()
                    cdbtxt2json.c2j()
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
            elif line['password'] != password:
                print("密碼輸錯!")
                return [
                        f'USB Serial Number = {input_value}',
                        f'Agent = {clickedKey}',
                        fac.AntdNotification(
                        message='密碼輸入錯誤',
                        description='提示:帳號密碼輸入錯誤',
                        type='error',
                        placement = 'bottomRight')
                    ]
        elif  line['manager'] != account:
            check+=1
    if check==len(lines):
        print("check",check)
        return [
                f'USB Serial Number = {input_value}',
                f'Agent = {clickedKey}',
                fac.AntdNotification(
                message='查無此帳號',
                description='提示:帳號密碼輸入錯誤',
                type='error',
                placement = 'bottomRight')
            ]
