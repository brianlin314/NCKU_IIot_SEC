import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, MATCH
from dash import callback
import dash_html_components as html

import globals

field_style = {'margin-top':'7px', 'margin-left':'50px',"width": 150}
add_btn_style = {'color':'green', 'fontSize':12,'margin-top':'4.98px', 'margin-bottom':'3px', 'align':'center', "width": 50}
del_btn_style = {'color':'red', 'fontSize':12,'margin-top':'4.98px', 'margin-bottom':'3px', 'align':'center', "width": 50}

def serve_btns():
    add_collapse_fields = []
    del_collapse_fields = []

    for i in range(globals.fields_num):
        # 新增 add collapsed fields, btns
        field = globals.all_fields[i]

        add_collapse_text = dbc.Collapse(
            html.P(field, style=field_style),
            id={'type': 'add_collapse_text', 'index': i},
            is_open=True,
        )
        add_collapse_btn = dbc.Collapse(
            html.Button('+ add', id = {'type': 'add_btn', 'index': i}, n_clicks=0, style=add_btn_style),
            id={'type': 'add_collapse_btn', 'index': i},
            is_open=True,
        )
        add_collapse_field = dbc.Row(
            [
                add_collapse_text,
                dbc.Col(style={"width": 70}),
                add_collapse_btn,
            ]
        )
        add_collapse_fields.append(add_collapse_field)

        # 新增 del collapsed fields, btns
        del_collapse_text = dbc.Collapse(
            html.P(field, style=field_style),
            id={'type': 'del_collapse_text', 'index': i},
            is_open=False,
        )
        del_collapse_btn = dbc.Collapse(
            html.Button('- del', id = {'type': 'del_btn', 'index': i}, n_clicks=0, style=del_btn_style),
            id={'type': 'del_collapse_btn', 'index': i},
            is_open=False,
        )
        del_collapse_field = dbc.Row(
            [
                del_collapse_text,
                dbc.Col(style={"width": 70}),
                del_collapse_btn,
            ]
        )
        del_collapse_fields.append(del_collapse_field)

    return add_collapse_fields, del_collapse_fields

@callback(
    [
        Output({'type': 'add_collapse_text', 'index': MATCH}, 'is_open'),
        Output({'type': 'add_collapse_btn', 'index': MATCH}, 'is_open'),
        Output({'type': 'del_collapse_text', 'index': MATCH}, 'is_open'),
        Output({'type': 'del_collapse_btn', 'index': MATCH}, 'is_open'),
    ],
    [
        Input({'type': 'add_btn', 'index': MATCH}, 'n_clicks'),
        Input({'type': 'del_btn', 'index': MATCH}, 'n_clicks'),
        Input({'type': 'add_btn', 'index': MATCH}, 'id'),
    ],
    prevent_initial_call=True
)
def update(add_clicks, del_clicks, id):
    # 監聽 add_btn 是否被按, 若有則新增該 field
    field_idx = int(id['index'])
    if add_clicks == globals.add_next_click[field_idx]:
        globals.add_next_click[field_idx] += 1
        field_name = globals.all_fields[field_idx]
        globals.selected_fields.append(field_name)
        # print(selected_fields)
        return [False, False, True, True]

    # add_btn 沒被按 => 則為 del_btn 被按, 或者add_btn, del_btn都沒被按(網頁初始狀態)
    else:
        try:
            globals.selected_fields.remove(globals.all_fields[field_idx])
            # print(selected_fields)
        except:
            pass
        return [True, True, False, False]