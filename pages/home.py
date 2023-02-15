import dash_html_components as html

STYLE = {
    "transition": "margin-left .5s",
    "margin-top": "2rem", # 離上面多遠
    "margin-left": "15.5rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem", # 往內縮多少
    "position":"relative", # 設定位置是相對的還是絕對的
    "left":'0.2rem',
    "width":"73rem",
    "background-color": "#f8f9fa",
    'fontSize': 18,
    'zIndex':1,
}
def serve_layout():
    layout = html.Div(
        [
            html.H3('NCKU_IIoT_SEC 使用手冊:'),
            html.H4('本系統含有:'),
            html.Ul(
                [
                    html.Ul(
                        [
                            html.Li('對本機的監控 - Host IDS'),
                            html.Li('對網路流的監控 - Network IDS'),
                            html.Li('AI預測異常網路流量 - AI Prediction'),
                            html.Li('USB黑白名單辨識 - USB Logs'),
                        ],
                        style={'fontSize':15}
                    ),
                ]
            ),
            html.Hr(), # 底線
            html.H4('Host Based IDS:'),
            html.Ul(
                [
                    html.Li('Discover Page:'),
                    html.Ul(
                        [
                            html.Li('1. 此頁面呈現詳細的log檔內容'),
                            html.Ul(
                                [
                                    html.Li('注意: update僅是選取時間區段，必須再選擇監控端點才會顯示資料'),
                                    html.Img(src='./assets/img/date.png')
                                ]
                            ),
                            html.Li('2. 當 selected fields 為空時, 預設顯示所有的 fields; 可透過 Available fields 選取特徵'),
                            html.Li('3. Table 欄位旁的箭頭可以點選, 選擇資料要升/降冪排序'),
                            html.Li('4. 滑鼠移到 Table 中, 可以顯示詳細資訊'),
                            html.Img(src='./assets/img/hover.png'),
                        ],
                        style={'fontSize': 15}
                    ),
                    html.Li('Security Events'),
                    html.Ul(
                        [
                            html.Li('1. 此頁面呈現不同的可視化資訊和圖表'),
                            html.Ul(
                                [
                                    html.Li('注意: update僅是選取時間區段，必須再選擇監控端點才會顯示資料')
                                ]
                            ),
                        ],
                        style={'fontSize': 15}
                    ),
                    html.Li('Event Logs'),
                    html.Ul(
                        [
                            html.Li('1. 此頁面呈現當天的log檔'),
                            html.Ul(
                                [
                                    html.Li('注意: 必須選擇監控端點才會顯示資料')
                                ]
                            ),
                        ],
                        style={'fontSize': 15}
                    ),
                ]
            ),
            html.Hr(), # 底線
            html.H4('Network Based IDS:'),
            html.Ul(
                [   
                    html.Li('History'),
                    html.Ul(
                        [
                            html.Li('1. 此頁面呈現詳細的log檔內容'),
                            html.Ul(
                                [
                                    html.Li('注意: update僅是選取時間區段，必須再選擇監控端點才會顯示資料'),
                                    html.Img(src='./assets/img/date.png')
                                ]
                            ),
                            html.Li('2. 每個欄位底下可透過filter篩選想要的關鍵字'),
                            html.Img(src='./assets/img/filter.png'),
                        ],
                        style={'fontSize': 15}
                    ),
                    html.Li('Statistics'),
                    html.Ul(
                        [
                            html.Li('1. 此頁面呈現不同的可視化資訊和圖表'),
                            html.Ul(
                                [
                                    html.Li('注意: update僅是選取時間區段，必須再選擇監控端點才會顯示資料')
                                ]
                            ),
                        ],
                        style={'fontSize': 15}
                    ),
                    html.Li('Event Logs'),
                    html.Ul(
                        [
                            html.Li('1. 此頁面呈現當天的log檔'),
                            html.Ul(
                                [
                                    html.Li('注意: 必須選擇監控端點才會顯示資料')
                                ]
                            ),
                        ],
                        style={'fontSize': 15}
                    ),

                ]
            ),
            html.Hr(), # 底線
            html.H4('AI prediction:'),
            html.Ul(
                [
                    html.Li('說明:'),
                    html.Ul(
                        [
                            html.Li('1. 以AI模型對封包進行分析，若疑似異常封包，則 pred_label = 1，並且會以紅色標記'),
                            html.Li('2. 呈現封包詳細內容'),
                            html.Ul(
                                [
                                    html.Li('注意: 必須選擇監控端點才會顯示資料')
                                ]
                            ),
                        ],
                        style={'fontSize': 15}
                    ),
                ]
            ),
            html.Hr(), # 底線
            html.H4('USB logs:'),
            html.Ul(
                [
                    html.Li('說明:'),
                    html.Ul(
                        [
                            html.Li('1. 顯示當前有連接的usb與連接在哪個端口，且判定是否為授權'),
                            html.Img(src='./assets/img/usb_detail2.png')
                        ],
                        style={'fontSize': 15}
                    ),
                ]
            ),
            html.Hr(), # 底線
            html.H4('Setting:'),
            html.Ul(
                [
                    html.Li('Add/Delete USB:'),
                    html.Ul(
                        [
                            html.Li('1. 此頁面可新增USB白名單'),
                            html.Li('2. 需先輸入正確的使用者帳號密碼，方可新增'),
                            html.Img(src='./assets/img/usb.png')
                        ],
                        style={'fontSize': 15}
                    ),
                ]
            )
        ],
        style=STYLE,
    )
    return layout