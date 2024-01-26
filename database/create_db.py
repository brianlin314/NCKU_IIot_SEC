import os
import json
import glob
import pickle as pkl
from components import nids_logtojson, ai_result
from itertools import islice
import get_config
import tensorflow as tf
import xgboost as xgb
import pandas as pd
import numpy as np
from datetime import datetime
import subprocess

def record_last(last_date_info):
    file = open('last_date.pkl', 'wb')
    pkl.dump(last_date_info, file)
    file.close()

def change_permission(dir_path, sudoPassword):
    paths = dir_path.split('/')
    path = '/'.join(paths[:3])
    try:
        if oct(os.stat(path).st_mode)[-3:] == '777':
            print(path, 'is already 777')
            return
        else:
            cmd = f"sudo chmod 777 -R {path}"
            subprocess.run(['sudo', '-S', *cmd.split()], input=sudoPassword.encode(), check=True)
            return
    except:
        print(path, 'Permission denied')
        return

def unzip(dir_path, sudoPassword):
    gz_files = glob.glob(f'{dir_path}/**/*.json.gz', recursive=True)

    # unzip all .json.gz files => 用 "find {dir_path} -name '*.json.gz' -exec gunzip {} +" 指令
    # f sting 中用兩個{}, 來顯示{}
    if len(gz_files) != 0:
        changePermission_cmd = f"echo {sudoPassword} | sudo -S chmod 777 -R {dir_path}"
        os.system(changePermission_cmd)
        unzip_cmd = f"find {dir_path} -name '*.json.gz' -exec gunzip {{}} +"
        os.system(unzip_cmd)

def createDB(database, dir_path, sudoPassword):

    # 更改目錄存取權限
    change_permission(dir_path, sudoPassword)

    # unzip json.gz files
    unzip(dir_path, sudoPassword)

    # 找出年份(2000~2099)的資料夾, 並由小到大排序
    targetPattern = "20[0-9][0-9]"
    years = sorted(glob.glob(f'{dir_path}/{targetPattern}'))

    months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
    ]

    month_dict = {}
    for i in range(len(months)):
        month_dict[months[i]] = i + 1

    num = 0
    data = []
    error_file = ''
    json_files = []
    for year_ in years:
        # 按照月份存取
        for month in months:
            json_files = sorted(glob.glob(f'{year_}/{month}/*.json'))  # 找出所有日期的 .json files, 並由小到大排序
            for i in range(len(json_files)):
                f = open(json_files[i], 'r', errors='replace')
                lines = f.readlines()

                # 紀錄每月最後有資料的日期, data數目 => 紀錄 last date info
                if i == len(json_files)-1:
                    day = json_files[i].split('.')[-2].split('-')[-1]
                    last_date_info = [f'{year_}-{month_dict[month]}-{day}', len(lines)]
                    record_last(last_date_info)
                try:
                    json_lines = [json.loads(line) for line in lines]
                    num += len(lines)
                except:
                    error_file = json_files[i]
                data += json_lines
    try:
        print("createDB:", data)
        database.insert_many(data) # insert data into mongoDB
    except:
        print(f'重新 insert {error_file}')
        f = open(error_file, 'r', errors='replace')
        lines = f.readlines()
        json_lines = [json.loads(line) for line in lines]
        num += len(lines)
        database.insert_many(json_lines)
    return num

def record_nids_last(last_num_info):
    file = open('last_nids_num.pkl', 'wb')
    pkl.dump(last_num_info, file)
    file.close()

def createnidsDB(database, dir_path, sudoPassword):

    # 更改目錄存取權限
    change_permission(dir_path, sudoPassword)
    
    #Ollie:這樣每次更新的時候log一樣不會被轉成json
    targetPattern = "20[0-9][0-9]"

    years = sorted(glob.glob(f'{dir_path}/{targetPattern}'))

    months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
    ]

    num = 0
    data = []
    error_file = ''
    log_files = []
    log_lines = []

    for year_ in years:
        log_files = sorted(glob.glob(f'{year_}/*.log'))  # 找出所有日期的 .log files, 並由小到大排序

        for i in range(len(log_files)):
            f = open(log_files[i], 'r', errors='replace')
            lines = f.readlines()

            # 紀錄每月最後有資料的日期, data數目 => 紀錄 last date info
            if i == len(log_files)-1:
                day = log_files[i].split('.')[-2].split('-')[-1]
                month = log_files[i].split('.')[-2].split('-')[-2]
                last_date_info = [f'{year_}-{month}-{day}', len(lines)]
                record_nids_last(last_date_info)
            try:
                log_lines = [nids_logtojson.log2dic(line) for line in lines]
                num += len(lines)
            except:
                error_file = log_files[i]
            data += log_lines
            print(f'{log_files[i]} 有 {len(lines)} 筆資料')
    try:
        database.insert_many(data) # insert data into mongoDB
    except:
        print(f'重新 insert {error_file}')
        f = open(error_file, 'r')
        lines = f.readlines()
        log_lines = [nids_logtojson.log2dic(line) for line in lines]
        num += len(lines)
        database.insert_many(log_lines)
    return num

def createaiDB(database, dir_path, sudoPassword):
    config = get_config.get_variable()
    # 更改目錄存取權限
    change_permission(dir_path, sudoPassword)
    lists = os.listdir(dir_path)     #列出目錄的下所有文件和文件夾保存到lists

    q_list = []
    for pcap in lists:
        if os.path.getsize(dir_path+pcap) >= 50000000:
            q_list.append(pcap)
    q_list.sort(key=lambda fn:os.path.getmtime(dir_path + fn)) #按時間排序

    num = 0
    error_file = ''
    # log_files = []

    for i, pcap in enumerate(q_list):
        data = []
        if not os.path.isfile(config["csvdirpath"]+pcap+'.csv'):
            cmd = f"cicflowmeter -f {dir_path+pcap} -c {config['csvdirpath']}{pcap}.csv" # 將pcap通過cic-flowmeter轉成csv
            os.system(cmd) # 將指令給os執行
        with tf.device('/cpu:0'): # cpu運行
            model = xgb.Booster()
            model.load_model(config["model_path"])
        file = pd.read_csv(config["csvdirpath"]+pcap+'.csv')
        df_list = []
        df_list.append(file)

        df = pd.concat(df_list, axis=0, ignore_index=True)
        if len(df) == 0: # 若df沒資料，回傳0
            return 0
        del df_list

        cleaned_data = df.dropna()
        del df

        X_test = cleaned_data.drop(columns = ["src_ip","dst_ip","src_port","timestamp", "protocol","psh_flag_cnt","init_fwd_win_byts","flow_byts_s","flow_pkts_s"], axis=1)
        X_test = X_test.iloc[:, :].values
        X_test = X_test.tolist()
        print('model is analyzing...')
        result = model.predict(xgb.DMatrix(X_test))
        result = np.array(result)
        pred_label=[[] for i in range(len(result))]
        result=result.tolist()
        for i in range(len(result)):
            pred_label[i]=result[i].index(max(result[i]))
        result=np.array(result)

        cleaned_data['pred_label'] = pred_label
        cleaned_data[['Date','Time']] = cleaned_data['timestamp'].str.split(' ', expand = True)
        cleaned_data = cleaned_data.drop(columns= ["timestamp", 'flow_duration', 'flow_byts_s', 'flow_pkts_s', 'fwd_pkts_s', 'bwd_pkts_s', 'tot_fwd_pkts', 'tot_bwd_pkts', 'totlen_fwd_pkts', 'totlen_bwd_pkts', 'fwd_pkt_len_max', 'fwd_pkt_len_min', 'fwd_pkt_len_mean', 'fwd_pkt_len_std', 'bwd_pkt_len_max', 'bwd_pkt_len_min', 'bwd_pkt_len_mean', 'bwd_pkt_len_std', 'pkt_len_max', 'pkt_len_min', 'pkt_len_mean', 'pkt_len_std', 'pkt_len_var', 'fwd_header_len', 'bwd_header_len', 'fwd_seg_size_min', 'fwd_act_data_pkts', 'flow_iat_mean', 'flow_iat_max', 'flow_iat_min', 'flow_iat_std', 'fwd_iat_tot', 'fwd_iat_max', 'fwd_iat_min', 'fwd_iat_mean', 'fwd_iat_std', 'bwd_iat_tot', 'bwd_iat_max', 'bwd_iat_min', 'bwd_iat_mean', 'bwd_iat_std', 'fwd_psh_flags', 'bwd_psh_flags', 'fwd_urg_flags', 'bwd_urg_flags', 'fin_flag_cnt', 'syn_flag_cnt', 'rst_flag_cnt', 'psh_flag_cnt', 'ack_flag_cnt', 'urg_flag_cnt', 'ece_flag_cnt', 'down_up_ratio', 'pkt_size_avg', 'init_fwd_win_byts', 'init_bwd_win_byts', 'active_max', 'active_min', 'active_mean', 'active_std', 'idle_max', 'idle_min', 'idle_mean', 'idle_std', 'fwd_byts_b_avg', 'fwd_pkts_b_avg', 'bwd_byts_b_avg', 'bwd_pkts_b_avg', 'fwd_blk_rate_avg', 'bwd_blk_rate_avg', 'fwd_seg_size_avg', 'bwd_seg_size_avg', 'cwe_flag_count', 'subflow_fwd_pkts', 'subflow_bwd_pkts', 'subflow_fwd_byts', 'subflow_bwd_byts'])

        #p.s釋放空間
        del X_test
        del result
        del pred_label

        try:
            airesultline = cleaned_data.to_dict('records')
        except:
            print('轉dictionary失敗')

        data += airesultline
        print(f'{pcap} 有 {len(airesultline)} 筆資料')
        try:
            database.insert_many(data) # insert data into mongoDB
        except:
            print(f'insert failed')

        try:
            cmd2 = f"rm {dir_path+pcap}"
            cmd3 = f"rm {config['csvdirpath']}{pcap}.csv"
            os.system(cmd2)
            os.system(cmd3)
            num += 1
        except:
            print("刪除檔案失敗")
    return num