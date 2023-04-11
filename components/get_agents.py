from subprocess import Popen, PIPE
import globals_variable
from dash import dash_table
import pandas as pd
import time
import dash_html_components as html
import feffery_antd_components as fac 

def process():
    sudo_password = "echo "+ globals_variable.sudoPassword+"\n"
    command = 'cd /var/ossec/bin\n'
    cmd2 = './agent_control -l\n'
    p = Popen('sudo -s\n', shell= True, stdin=PIPE,  stdout=PIPE)
    time.sleep(1)
    p.stdin.write(sudo_password .encode())
    p.stdin.write(command.encode())
    p.stdin.write(cmd2.encode())
    p.stdin.close()
    # while True:
    result_str = p.stdout.readlines()

    df = pd.DataFrame(columns=['ID','Name'])

    for line in result_str:
        line = line.decode()
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


