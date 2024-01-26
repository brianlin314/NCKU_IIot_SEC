import cicflowmeter
import os
import pandas as pd
import keras
from keras.models import load_model
import xgboost as xgb
from xgboost import XGBClassifier
import pickle
import numpy as np
import tensorflow as tf
import get_config

def new_report(test_report):
    lists = os.listdir(test_report)     #列出目錄的下所有文件和文件夾保存到lists
    lists.sort(key=lambda fn:os.path.getmtime(test_report + fn))        #按時間排序
    file_new = os.path.join(test_report,lists[-1])      #獲取最新的文件保存到file_new
    return file_new

def airesult(ip):
    config = get_config.get_variable()
    pcappath = new_report(config.pcapdirpath)
    file = os.path.split(pcappath)[-1]
    cmd = f"cicflowmeter -f {pcappath} -c {config.csvdirpath}{file}.csv" # 將pcap通過cic-flowmeter轉成csv
    os.system(cmd) # 將指令給os執行
    with tf.device('/cpu:0'): # cpu運行
        model = xgb.Booster()
        model.load_model(config.model_path) # 載入model

    csvpath = new_report(config.csvdirpath)
    file = pd.read_csv(csvpath)
    mask1 = (file["src_ip"] == ip)
    mask2 = (file["dst_ip"] == ip)
    file = file[(mask1|mask2)]
    
    df_list = []
    df_list.append(file)

    df = pd.concat(df_list, axis=0, ignore_index=True)
    if len(df) == 0: # 若df沒資料，回傳0
        return 0
    del df_list
    cleaned_data = df.dropna()
    X_test = cleaned_data.drop(columns = ["src_ip","dst_ip","src_port","timestamp", "protocol","psh_flag_cnt","init_fwd_win_byts","flow_byts_s","flow_pkts_s"], axis=1)
    del df
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
    
    #p.s釋放空間
    del X_test
    del result
    del pred_label

    return cleaned_data
