import get_config
import pandas as pd
from database import get_db


def default():
    global usb_add_options, dir_path, agent_ip, agent_id, nids_agent_options, hids_agent_options
    config = get_config.get_variable()
    nids_agent_options = config["nids_agent_options"] # pages 底下的 agent 下拉式選單選項
    hids_agent_options = config["hids_agent_options"] # pages 底下的 agent 下拉式選單選項
    usb_add_options = config["usb_add_options"] # pages 底下的 agent 下拉式選單選項
    agent_ip = config["agent_ip"] # agent ip
    agent_id = config["agent_id"] # agent id
    
def initialize():
    global posts, first, selected_fields, n_selected_fields, add_next_click, all_fields, fields_num
    config = get_config.get_variable()
    first = 1
    selected_fields = []
    n_selected_fields = []
    _, posts, num, current_db, = get_db.get_current_db(config["hidsdirpath"], config["sudoPassword"])
    _, nidsjson, n_num, current_nids_db, = get_db.get_current_nidsdb(config["nidsdirpath"] , config["sudoPassword"])
    _, airesult, ai_num, current_ai_db, = get_db.get_current_aidb(config["pcapdirpath"] , config["sudoPassword"])
    all_fields, fields_num = get_fields(posts)
    add_next_click = [1 for i in range(fields_num)]
    print("初始化完成，歡迎使用 Dashboard!")

def get_fields(posts):
    data = posts.find({}, {'_id':0})
    df = pd.json_normalize(data)
    all_fields = list(df.columns)
    if 'timestamp' in all_fields:
        all_fields.remove('timestamp')
    else:
        print("'timestamp' not found in all_fields")
    return all_fields, len(all_fields)
