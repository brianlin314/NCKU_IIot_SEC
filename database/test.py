import os
from datetime import datetime

import pandas as pd
import torch
from sklearn.preprocessing import MinMaxScaler
from torch import nn
from torch.utils.data import DataLoader, Dataset

import get_config
import json
from pymongo import MongoClient

class AutoEncoder(nn.Module):
    def __init__(self, f_in):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(f_in, 100),
            nn.Tanh(),
            nn.Dropout(0.2),
            nn.Linear(100, 70),
            nn.Tanh(),
            nn.Dropout(0.2),
            nn.Linear(70, 40)
        )
        self.decoder = nn.Sequential(
            nn.ReLU(inplace=True),
            nn.Linear(40, 40),
            nn.Tanh(),
            nn.Dropout(0.2),
            nn.Linear(40, 70),
            nn.Tanh(),
            nn.Dropout(0.2),
            nn.Linear(70, f_in)
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

def filter_and_sort_pcap(directory_path, min_size_mb=9.9):
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
    df = pd.read_csv(file_name)
    df = df.drop(['timestamp', 'src_ip', 'dst_ip'], axis=1)
    cleaned_df = df.dropna()
    cleaned_df.isna().sum().to_numpy()

    cleaned_df = cleaned_df.to_numpy()
    dataset = MinMaxScaler().fit_transform(cleaned_df)
    data = torch.tensor(dataset, dtype=torch.float32)

    data_loader = DataLoader(data, batch_size=batch_size, shuffle=False)
    
    model = AutoEncoder(79)  # 確保 input_size 和 hidden_size 與模型訓練時相同
    model = torch.load(model_path, map_location=torch.device('cpu'))
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
        print("pcap:", pcap, "anomaly:", anomaly_indices)
        df_with_labels = mark_anomalies(config["csvdirpath"] + pcap + '.csv', anomaly_indices)
        data += df_with_labels.to_dict('records')
        try:
            database.insert_many(data) # insert data into mongoDB
        except Exception as e:
            print(e)
            
        
if __name__ == '__main__':
    ##
    with open('config.json', 'r') as f:
        config = json.load(f)
        mongoUrl = config['mongoUrl']

    # 建立和mongoDB連線，取用collection中的posts
    client = MongoClient(mongoUrl)
    db = client['pythondb']
    current_db = db.list_collection_names()
    airesult = db.airesult
    ##
    createaiDB(airesult, "./wirepcap/pcap/")
    