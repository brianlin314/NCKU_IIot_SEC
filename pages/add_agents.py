import dash
import dash_bootstrap_components as dbc
import feffery_antd_components as fac
import get_config
import globals_variable
from components import get_agents
from dash import callback, html
from dash.dependencies import Input, Output, State

STYLE = { # 設定背景風格
    "position": "relative",
    "top": "1rem",
    "left": "15rem",
    'zIndex':"auto",
}

def serve_layout():
    layout = html.Div(
        [
            fac.AntdRow(
                [
                    html.Div(
                        html.H2('Add Agent Option'),
                    ),
                ]
            ),
            fac.AntdRow(
                [
                    html.Div(
                        html.P('This page can setting your own HIDS agent to show statistics on dashboard'),
                        style = {
                            'color':'#4F4F4F',
                        },
                    ),
                ]
            ),
            fac.AntdRow(
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
                    size = 200,
                ),
            ),
            fac.AntdRow(
                fac.AntdSpace(
                    [
                        
                        fac.AntdInput(
                            size='middle',
                            id='input-mngid',
                            placeholder='',
                            style={
                                'width': '200px',
                                'marginBottom': '5px'
                            }
                        ),
                        fac.AntdInput(
                            id='input-psw',
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
            fac.AntdRow(
                fac.AntdButton(
                    children='Submit',
                    size='large',
                    type='primary',
                    id='input-button',
                ),
            ),
            html.Br(),
            fac.AntdRow(
                fac.AntdSpace(
                    [
                        fac.AntdCol(
                            html.Div(
                                id='agenttable',
                            ),
                        ),
                        fac.AntdCol(
                            html.Div(
                                id='savebutton',
                            ),
                        ),

                    ],
                    size = 50,
                ),
            ),
            dbc.Row(
                html.Div(
                    id='savesuccesstext'
                ),
            ),
        ],
        style=STYLE,
    )
    return layout

@callback(
    Output('agenttable','children'),
    Output('savebutton','children'),
    [
        Input('input-button','nClicks'),
    ],
    [
        State('input-mngid','value'),
        State('input-psw','value'),
    ],
    prevent_initial_call=True # 防止每次都讀到None
)

def update(input_button_clicks, account, password): #第一個參數是Input的參數，第二個是State的參數,參數必須照順序填入
    config = get_config.get_variable()
    if (account == config['dash_user_name']) and (password == config['dash_user_password']):
        return get_agents.process() # Call from /components/get_agent.py, for read existing agent as json format
    return html.P("Login Error!"), dash.no_update
            
@callback(
    Output('savesuccesstext','children'),
    Input('savebutton','nClicks'),
    State('agent_table','data'),
    State('agent_table','selected_rows'),
    prevent_initial_call=True # 防止每次都讀到None
)
def update2(input_button_clicks, df,  selected_rows):
    hids_opt = []
    usb_opt = []
    agentid = {}
    if len(selected_rows)>0:
        for row in selected_rows:
            hids_opt.append({'label':df[row]['Name'], 'value': df[row]['Name']})
            usb_opt.append({'label':df[row]['Name'],'value':df[row]['ID'].strip()})
            agentid[df[row]['Name']] = df[row]['ID'].strip()
        globals_variable.hids_agent_options = hids_opt
        globals_variable.usb_add_options = usb_opt
        globals_variable.agent_id = agentid
        return html.P("Save Successful")
    else:
        return dash.no_update
