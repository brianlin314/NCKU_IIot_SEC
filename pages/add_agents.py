import dash_bootstrap_components as dbc
from dash import dcc
import dash_html_components as html

STYLE = {
    "transition": "margin-left .5s",
    "margin-top": "2rem",
    "margin-left": "20rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 30,
    'zIndex':1,
    'border':'1px black solid',
}
dropdown_style = {
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
            html.P("Welcome to add agent"),
            dbc.Row(
                    dbc.Col(
                        html.Div(children=[
                            dcc.Dropdown(                       
                                id="choice_agent",
                                options=[
                                    {'label': 'Agent_A'},
                                    {'label': 'Respberry_pi'}
                                ],
                                placeholder="agent",
                            )
                        ],style=dropdown_style),
                    )
            ),
        ],
        style=STYLE,
    )
    return layout
