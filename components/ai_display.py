import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, callback, dash_table
import dash_html_components as html
import pandas as pd
import json
from pandas import json_normalize
import globals
from components import ai_result
from datetime import date
import dash

table_style = {
    "margin-left": "1rem",
    "margin-right": "1rem",
    "position":"relative",
    "left":"0.5rem",
    "top":"2rem",
    'fontsize':12,
}

def update(ip):
    # today = date.today()
    # todate = today.strftime("%m/%d/%y")
    # #在server上需要取消註解這行 ： hids_logtojson.log2json(globals.hidsdirpath+'/2022/Aug/ossec-alerts-09.json')
    #讀取json檔, 篩選今天的log內容
    global df
    df = ai_result.airesult(ip)
    if type(df) == int:
        return html.H3("無資料可顯示，請檢查ip位址是否設定正確!")
    df = df.drop(['flow_duration', 'flow_byts_s', 'flow_pkts_s', 'fwd_pkts_s', 'bwd_pkts_s', 'tot_fwd_pkts', 'tot_bwd_pkts', 'totlen_fwd_pkts', 'totlen_bwd_pkts', 'fwd_pkt_len_max', 'fwd_pkt_len_min', 'fwd_pkt_len_mean', 'fwd_pkt_len_std', 'bwd_pkt_len_max', 'bwd_pkt_len_min', 'bwd_pkt_len_mean', 'bwd_pkt_len_std', 'pkt_len_max', 'pkt_len_min', 'pkt_len_mean', 'pkt_len_std', 'pkt_len_var', 'fwd_header_len', 'bwd_header_len', 'fwd_seg_size_min', 'fwd_act_data_pkts', 'flow_iat_mean', 'flow_iat_max', 'flow_iat_min', 'flow_iat_std', 'fwd_iat_tot', 'fwd_iat_max', 'fwd_iat_min', 'fwd_iat_mean', 'fwd_iat_std', 'bwd_iat_tot', 'bwd_iat_max', 'bwd_iat_min', 'bwd_iat_mean', 'bwd_iat_std', 'fwd_psh_flags', 'bwd_psh_flags', 'fwd_urg_flags', 'bwd_urg_flags', 'fin_flag_cnt', 'syn_flag_cnt', 'rst_flag_cnt', 'psh_flag_cnt', 'ack_flag_cnt', 'urg_flag_cnt', 'ece_flag_cnt', 'down_up_ratio', 'pkt_size_avg', 'init_fwd_win_byts', 'init_bwd_win_byts', 'active_max', 'active_min', 'active_mean', 'active_std', 'idle_max', 'idle_min', 'idle_mean', 'idle_std', 'fwd_byts_b_avg', 'fwd_pkts_b_avg', 'bwd_byts_b_avg', 'bwd_pkts_b_avg', 'fwd_blk_rate_avg', 'bwd_blk_rate_avg', 'fwd_seg_size_avg', 'bwd_seg_size_avg', 'cwe_flag_count', 'subflow_fwd_pkts', 'subflow_bwd_pkts', 'subflow_fwd_byts', 'subflow_bwd_byts'],axis = 1)
    df = df[['pred_label', 'timestamp', 'src_ip', 'dst_ip', 'src_port', 'dst_port', 'protocol']] #, 'src_mac', 'dst_mac'
    df= df.sort_values(by='timestamp',ascending=False)
    all_cols = list(df.columns)

    table = dash_table.DataTable(
        virtualization=True,
        data=df.to_dict('records'),
        columns=[{'name': column, 'id': column} for column in all_cols],
        style_header={
            'backgroundColor': '#99ABBD',
            'color': 'black',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'border':'1px black solid',
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell={
            'width': '180px',
            'textAlign': 'center',
            'fontsize':12,
            'height': 'auto',

        },
        style_table={
            'minWidth': '100%',
            'Width': '100%'
        },
        style_data_conditional=[
        {
            'if': {
                'filter_query': '{pred_label} >= 1',
                'column_id': 'pred_label'
            },
            'backgroundColor': '#FD4000',
            'color': 'white'
        },
        

    ]
    )
    return table
