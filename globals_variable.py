import pandas as pd
from database import get_db
from datetime import date
from components import nids_logtojson
def default():
    global user_psw , posts, model_path, usb_add_options, sudoPassword, dir_path, agent_ip, agent_id, nids_agent_options, hids_agent_options, current_db, selected_fields, n_selected_fields, add_next_click, all_fields, fields_num, hidsdirpath, nidsdirpath, pcapdirpath, csvdirpath
    sudoPassword = 'uscc^%^07SEC' # 虛擬機密碼
    dir_path = '/var/ossec/logs/alerts'
    hidsdirpath = '/var/ossec/logs/alerts/' # ('放你的wazuhlog存放路徑 不包含年月日'+'/'+today.year+'/'+today.strftime("%b")+'/ossec-alerts-'+today.day+'.json')
    nidsdirpath = '/var/log/suricata/'  # nids存放路徑 不包含檔名
    pcapdirpath = './wirepcap/pcap/' 
    csvdirpath = './wirepcap/csv/' 
    model_path = 'cic_xgboost.bin'
    nids_agent_options = [               # pages 底下的 agent 下拉式選單選項               
        {'label': 'Server', 'value': 'Server'},
        {'label': 'PCs', 'value': 'PCs'},
    ] 
    hids_agent_options = [            # pages 底下的 agent 下拉式選單選項               
        {'label': 'Server', 'value': 'Server'},
        {'label': 'PC_1', 'value': 'PC_1'},
        {'label': 'PC_2', 'value': 'PC_2'},
        {'label': 'PC_3', 'value': 'PC_3'},
    ] 
    usb_add_options = [
    	{'label':'Server','value':'000'},
	    {'label':'PC_1','value':'001'},
        {'label':'PC_2','value':'002'},
        {'label':'PC_3','value':'003'},
    ]
    agent_ip = {'Server' : '140.116.82.33', 'PCs' : '210.61.41.223'}
    agent_id = {'Server' : '000', 'PC_1' : '001', 'PC_2' : '002', 'PC_3' : '003'}
    user_psw = {'hello': 'world'}
    
def initialize():
    global posts, current_db, first, selected_fields, current_nids_db, n_selected_fields, add_next_click, all_fields, fields_num
    first = 1
    sudoPassword = 'uscc^%^07SEC' # 虛擬機密碼
    dir_path = '/var/ossec/logs/alerts'
    nidsdirpath = '/var/log/suricata/'
    selected_fields = []
    n_selected_fields = []
    _, posts, num, current_db, = get_db.get_current_db(dir_path, sudoPassword)
    # nids_logtojson.log2json('/var/log/suricata/fast.log') # brian new add
    _, nidsjson, n_num, current_nids_db, = get_db.get_current_nidsdb(nidsdirpath , sudoPassword)
    all_fields, fields_num = get_fields(posts)
    add_next_click = [1 for i in range(fields_num)]

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
