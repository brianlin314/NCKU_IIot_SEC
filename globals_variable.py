import pandas as pd
from database import get_db
from datetime import date

def initialize():
    global posts, model_path, num, sudoPassword, first, agent_pi_ip1, agent_pc_ip1, current_db, selected_fields, n_selected_fields, add_next_click, all_fields, fields_num, agent_pi_ip , agent_pc_ip, hidsdirpath, nidsdirpath, agent_pi_id , agent_pc_id, pcapdirpath, csvdirpath, modelpath, agent_options
    # 需要 sudo 密碼以存取檔案
    agent_pc_id = "000" # usb 的 agent id設定(pc) 
    agent_pi_id = "003" # usb 的 agent id設定(raspberry pi)
    agent_pc_ip = '192.168.0.150:0' # HIDS NIDS ip 設定(pc)
    agent_pi_ip = "192.168.3.66:80" # HIDS,NIDS ip 設定(raspberry pi)
    agent_pc_ip1 = '192.168.3.7'  # AI prediction 的ip設定(pc)
    agent_pi_ip1 = "192.168.3.66" # AI prediction 的ip設定(raspberry pi)
    sudoPassword = '0314' # 虛擬機密碼
    dir_path = '/var/ossec/logs/alerts'
    hidsdirpath = '/var/ossec/logs/alerts/' # ('放你的wazuhlog存放路徑 不包含年月日'+'/'+today.year+'/'+today.strftime("%b")+'/ossec-alerts-'+today.day+'.json')
    nidsdirpath = '/var/log/suricata/'  # nids存放路徑 不包含檔名
    pcapdirpath = './wirepcap/pcap/' 
    csvdirpath = './wirepcap/csv/' 
    model_path = 'cic_xgboost.bin'
    selected_fields = []
    n_selected_fields = []
    client, posts, num, current_db, = get_db.get_current_db(dir_path, sudoPassword)
    all_fields, fields_num = get_fields(posts)
    add_next_click = [1 for i in range(fields_num)]
    agent_options = [               # pages 底下的 agent 下拉式選單選項               
        {'label': 'Raspberry Pi', 'value': 'Raspberry Pi'},
        {'label': 'PC', 'value': 'PC'},
    ] 

def get_fields(posts):
    data = posts.find({}, {'_id':0})
    df = pd.json_normalize(data)
    all_fields = list(df.columns)
    all_fields.remove('timestamp')
    return all_fields, len(all_fields)

def get_hfields(posts):
    data = posts.find({}, {'_id':0})
    df = pd.json_normalize(data)
    all_hfields = list(df.columns)
    all_hfields.remove('timestamp')
    return all_hfields, len(all_hfields)
