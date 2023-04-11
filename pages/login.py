import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import callback
from flask import session
import dash_core_components as dcc

def serve_layout(): # login 彈出式介面
    layout = html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader("NCKU-IIOT-SEC"), 
                    dbc.ModalBody(
                        [
                            dbc.Input(
                                type="text",
                                placeholder="請輸入用戶名",
                                id="username-input",
                                className="mb-3",
                            ),
                            dbc.Input(
                                type="password",
                                placeholder="請輸入密碼",
                                id="password-input",
                                className="mb-3",
                            ),
                            dbc.Button("登入", id="login-button", color="primary", block=True),
                        ]
                    ),
                    dbc.ModalFooter(
                        [
                            html.Div(children='', id='output-state'),
                        ]
                    )
                ],
                id="login-modal",
                is_open = True,
            ),
            html.Div(id="hidden_div_for_redirect_callback")
        ],
    )
    return layout

@callback(
    Output("hidden_div_for_redirect_callback", "children"),
    Output('output-state', 'children'),
    Output('login-modal', 'is_open'),
    [
        Input('login-button', 'n_clicks'),
    ],
    [
        State('username-input', 'value'),
        State('password-input', 'value')
    ],
    prevent_initial_call = True
)

def login_button_click(login_button, username, password):
    if login_button > 0:
        if username == 'test' and password == 'test':
            session['user'] = username
            return dcc.Location(pathname="/Home", id="someid_doesnt_matter"), '', False
        else:
            return '/Login', 'Incorrect username or password', True