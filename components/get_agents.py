import subprocess
import time

import feffery_antd_components as fac
import get_config
import pandas as pd
from dash import dash_table, html


def process():
    config = get_config.get_variable()
    sudo_password = config['sudoPassword']
    cmd = '/var/ossec/bin/agent_control -l'

    sudo_password_with_newline = sudo_password + '\n'

    result = subprocess.run(['sudo', '-S', *cmd.split()], input=sudo_password_with_newline, text=True, check=True, capture_output=True)
    result_str = result.stdout.split('\n')
    

    df = pd.DataFrame(columns=['ID','Name'])

    for line in result_str:
        line_split = line.strip().split(',')
        if len(line_split) == 4:
            id = line_split[0].strip().split(':')[1]
            name = line_split[1].strip().split(':')[1]
            row = pd.Series([id, name],index=['ID','Name'])
            df = df.append(row, ignore_index = True)
    
    table = dash_table.DataTable(
        id = 'agent_table',
        virtualization=True,
        data=df.to_dict('records'),
        columns=[
            {"id": i, "name": i, "selectable": True} for i in df.columns
        ],
        row_selectable="multi",
        selected_rows=[],
        style_header={
            'backgroundColor': '#99ABBD',
            'color': 'black',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'border':'1px black solid',
            'height': '20px',
        },
        style_table={'height': None, "width": "400px", 'overflow': 'auto', "display": "flex","flex-flow": "column"},
        style_cell={'height': None, 'textAlign': 'center'},
    )
    button = fac.AntdRow(
                fac.AntdButton(
                    children='Save',
                    size='large',
                    type='primary',
                    id='savebutton',
                ),
            ),
    return table, button


