##########################
##       引用外部套件    ##
##########################
import os
import warnings
import webbrowser

import dash
import globals_variable
##########################
##       引用內部函式    ##
##########################
from components import hide_sidebar, navbar
from components.autoencoder_model import AutoEncoder
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State
from flask import Flask, send_from_directory, session
from pages import (AI_prediction, add_agents, add_usb, discover, hids_logs,
                   history, home, login, nids_logs, non_exist, security_events,
                   statistics, usb)

warnings.filterwarnings("ignore", category=Warning) # 忽略匹配的警告
server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

globals_variable.default() # 初始化全域變數，只在重啟Dash的時候會呼叫

###########################
##  SECRET_KEY Setting   ##
###########################
server.config.update(SECRET_KEY='mijijidasdoksmer') #可以隨便設定

##########################
##      Components      ##
##########################
global first # used by /page/security_events.py & /components/alert.py, 用來更新alert的筆數
first = 1

# login_modal = login.modal
navbar1 = navbar.navbar
sidebar = hide_sidebar.sidebar 
url = dcc.Location(id="url", refresh=True)
content = html.Div(id='content')

##########################
##      Layout          ##
##########################
def serve_layout():
    globals_variable.initialize()
    layout = html.Div(
        [
            url,
            navbar1, # 呼叫 navbar 裡的 navbar
            sidebar, # 呼叫 hide_sidebar 裡的 sidebar
            content,
        ],
    )
    return layout

# live update, 請注意這裡是要用 serve_layout 而非 serve_layout()
app.layout = serve_layout


# 透過 url 來決定顯示哪個 page
@app.callback(
    Output('content', 'children'),
    [
        Input('url', 'pathname'), # 第一個值為id，第二個值為屬性名
    ]
)

def display_page(pathname): # 根據callack,返回所選頁面
    global first

    view = None

    if ('user' not in session): # 檢查 user 是否在 session 中，其中 'user' 不是字串，而是 login.py 中的 session['user']，他可以直接呼叫
        view = login.serve_layout()

    elif (pathname in ['/', '/Home']) and ('user' in session): 
        view = home.serve_layout()

    elif (pathname == '/Host_based/Discover') and ('user' in session):
        view = discover.serve_layout(first)

    elif (pathname == '/Host_based/Security_events') and ('user' in session):
        view = security_events.serve_layout(first)

    elif (pathname == '/Host_based/logs') and ('user' in session):
        view = hids_logs.serve_layout()

    elif (pathname == '/Network_based/History') and ('user' in session):
        view = history.serve_layout()

    elif (pathname == '/Network_based/Statistics') and ('user' in session):
        view = statistics.serve_layout()

    elif (pathname == '/Network_based/logs') and ('user' in session):
        view = nids_logs.serve_layout()

    elif (pathname == '/AI_Prediction') and ('user' in session):
        view = AI_prediction.serve_layout()

    elif (pathname == '/USB') and ('user' in session):
        view = usb.serve_layout()
    
    elif (pathname == '/Setting/add_USB') and ('user' in session):
        view = add_usb.serve_layout()
    
    elif (pathname == '/Setting/add_agents') and ('user' in session):
        view = add_agents.serve_layout()

    else:
        view = non_exist.serve_layout()

    return view

@server.route("/total", methods=['GET'])
def serving_lottie_total():
    directory = os.path.join(os.getcwd(), "assets/lottie")
    return send_from_directory(directory, "total.json")

@server.route("/alert", methods=['GET'])
def serving_lottie_alert():
    directory = os.path.join(os.getcwd(), "assets/lottie")
    return send_from_directory(directory, "alert.json")

@server.route("/failure", methods=['GET'])
def serving_lottie_failure():
    directory = os.path.join(os.getcwd(), "assets/lottie")
    return send_from_directory(directory, "failure.json")

@server.route("/success", methods=['GET'])
def serving_lottie_success():
    directory = os.path.join(os.getcwd(), "assets/lottie")
    return send_from_directory(directory, "success.json")

if __name__ == '__main__':
    app.run_server(debug=True) # 每次更新時都可以直接查看網頁，而不用重新執行py
