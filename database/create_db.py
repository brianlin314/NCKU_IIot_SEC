import glob
import json
import os
import pickle as pkl
import subprocess
from datetime import datetime

import get_config
import numpy as np
import pandas as pd
import torch
from components import nids_logtojson
from components.autoencoder_model import AutoEncoder
from pymongo import MongoClient
from sklearn.preprocessing import MinMaxScaler
from torch import nn
from torch.utils.data import DataLoader, Dataset


def record_last(last_date_info):
    file = open('last_date.pkl', 'wb')
    pkl.dump(last_date_info, file)
    file.close()

def change_permission(dir_path, sudoPassword):
    paths = dir_path.split('/')
    path = '/'.join(paths[:3])
    try:
        cmd = f"sudo chmod 777 -R {path}"
        subprocess.run(['sudo', '-S', *cmd.split()], input=sudoPassword.encode(), check=True)
    except:
        pass

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
                    # json_lines = [json.loads(line) for line in lines]
                    json_lines = []
                    for line in lines:
                        # 檢查 line 是否為空
                        if line.strip():
                            try:
                                json_data = json.loads(line)
                                json_lines.append(json_data)
                            except json.decoder.JSONDecodeError as e:
                                print(f"Error decoding JSON: {e}. Skipping line.")
                    num += len(lines)
                except:
                    error_file = json_files[i]
                data += json_lines
    try:
        database.insert_many(data) # insert data into mongoDB
    except:
        print(f'重新 insert {error_file}')
        f = open(error_file, 'r', errors='replace')
        lines = f.readlines()
        # json_lines = [json.loads(line) for line in lines]
        json_lines = []
        for line in lines:
            # 檢查 line 是否為空
            if line.strip():
                try:
                    json_data = json.loads(line)
                    json_lines.append(json_data)
                except json.decoder.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}. Skipping line.")
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

def filter_and_sort_pcap(directory_path, min_size_mb=9.5):
    # 取得目錄中所有檔案
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    # 過濾並排序檔案
    filtered_files = [f for f in files if os.path.getsize(os.path.join(directory_path, f)) > min_size_mb * 1024 * 1024]
    sorted_files = sorted(filtered_files)

    return sorted_files

def pcap_to_csv(dir_path, pcap):
    config = get_config.get_variable()
    cmd = f"cicflowmeter -f {dir_path}{pcap} -c {config['csvdirpath']}{pcap}.csv"
    os.system(cmd)

def AEpredict(file_name, model_path, threshold=0.05, batch_size=32):
    config = get_config.get_variable()
    df = pd.read_csv(file_name)
    df = df.drop(['timestamp', 'src_ip', 'dst_ip'], axis=1)
    cleaned_df = df.dropna()
    cleaned_df.isna().sum().to_numpy()

    cleaned_df = cleaned_df.to_numpy()
    dataset = MinMaxScaler().fit_transform(cleaned_df)
    data = torch.tensor(dataset, dtype=torch.float32)

    data_loader = DataLoader(data, batch_size=batch_size, shuffle=False)
    
    model = AutoEncoder(79)  # 確保 input_size 和 hidden_size 與模型訓練時相同
    model = torch.load(config["model_path"], map_location=torch.device('cpu'))
    model.cpu()
    model.eval()

    reconstruction_errors = []
    with torch.no_grad():
        for data in data_loader:
            inputs = data.cpu()
            outputs = model(inputs)
            error = torch.mean(torch.square(outputs - inputs), dim=1)
            reconstruction_errors.extend(error.cpu().numpy())
    
    anomalies = [idx for idx, error in enumerate(reconstruction_errors) if error > threshold]

    return anomalies

def mark_anomalies(file_name, anomalies):
    df = pd.read_csv(file_name)
    df['predict_label'] = 'normal'  # 假設所有資料默認為正常

    # 將被標記為異常的資料行的 'predict_label' 設為 'anomaly'
    df.loc[anomalies, 'predict_label'] = 'anomaly'

    return df

def createaiDB(database, dir_path):
    config = get_config.get_variable()

    files = filter_and_sort_pcap(dir_path)

    for i, pcap in enumerate(files):
        data = []
        pcap_to_csv(dir_path, pcap)
        
        anomaly_indices = AEpredict(config["csvdirpath"] + pcap + '.csv', config["model_path"])
        df_with_labels = mark_anomalies(config["csvdirpath"] + pcap + '.csv', anomaly_indices)
        data += df_with_labels.to_dict('records')
        try:
            database.insert_many(data) # insert data into mongoDB
            cmd1 = f"rm {dir_path + pcap}"
            cmd2 = f"rm {config['csvdirpath']}{pcap}.csv"
            os.system(cmd1) 
            os.system(cmd2)
        except Exception as e:
            print(e)
    
    return len(files)
            