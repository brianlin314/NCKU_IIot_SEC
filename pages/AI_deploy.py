import os
import subprocess
import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

import torch
from torch import nn, optim
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
import json
import warnings

warnings.filterwarnings('ignore')

STYLE = {
    "transition": "margin-left .5s",
    "margin-top": "2rem",
    "margin-left": "15rem",
    "margin-right": "0.5rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'zIndex':1,
    "position":"relative",
    "left":"0.5rem",
    "top":"1rem"

}

def update_model_path_in_config(new_path, config_file='config.json'):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        
        new_path = os.path.join('model_weights', new_path)

        config['model_path'] = new_path
        
        with open(config_file, 'w') as file:
            json.dump(config, file, indent=4)
        
        return True

    except Exception as e:
        print(f"Error updating config file: {e}")
        return False

def get_file_options(folder_path):
    files = os.listdir(folder_path)
    options = [{'label': file, 'value': file} for file in files if os.path.isfile(os.path.join(folder_path, file))]
    return options

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

def train_model(input_file, save_name):
    model_save_path = f"./model_weights/{save_name}.pth"
    if not input_file.endswith('.pcap'):
        return "請確保檔案格式為 .pcap", 0
    
    output_csv = input_file.replace('.pcap', '.csv')
    output_csv_path = f"./train_csv/{output_csv}"
    try: 
        print("input_file:", input_file)
        subprocess.run(['cicflowmeter', '-f', input_file, '-c', output_csv_path], check=True)
        print("cicflowmeter success")
    except subprocess.CalledProcessError as e:
        return f"cicflowmeter error: {e}", 0
    
    df = pd.read_csv(output_csv_path)
    df = df.drop(['timestamp', 'src_ip', 'dst_ip'],axis=1)
    cleaned_df = df.dropna()
    X = cleaned_df
    x_train, x_test = train_test_split(X, test_size=0.2, random_state=42)

    x_train = x_train.to_numpy()
    x_test = x_test.to_numpy()
    x_train_scaled = MinMaxScaler().fit_transform(x_train)
    x_test_scaled = MinMaxScaler().fit_transform(x_test)
    train = torch.tensor(x_train_scaled, dtype=torch.float32)
    test = torch.tensor(x_test_scaled, dtype=torch.float32)

    EPOCHS = 100
    BATCH_SIZE = 256

    model = AutoEncoder(79)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    train_loader = DataLoader(train, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test, batch_size=1, shuffle=False)

    device = "cpu"

    training_loss_list = []
    model.to(device)

    for epoch in range(EPOCHS):
        training_loss = 0.0
        for data in train_loader:
            # Move data to device
            data = data.to(device)

            # Zero the parameter gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = model(data)

            # Loss
            loss = criterion(outputs, data)

            # Backward pass and optimize
            loss.backward()
            optimizer.step()
            training_loss += loss.item()

        # Compute average loss for the epoch
        average_training_loss = training_loss / len(train_loader)
        training_loss_list.append(average_training_loss)

        # Print progress
        if (epoch + 1) % 5 == 0:
            print(f"Epoch: {epoch + 1}, train loss: {average_training_loss:.6f}")
            
        # 保存模型的權重和參數
        torch.save(model, model_save_path)

    reconstruction_errors = []
    with torch.no_grad():
        for data in test_loader:
            inputs = data.to(device)
            outputs = model(inputs)
            error = torch.mean(torch.square(outputs - inputs), dim=1)
            reconstruction_errors.extend(error.cpu().numpy())

    # Set a threshold for anomaly detection
    threshold = 0.05

    # Detect anomalies based on the threshold
    anomalies = [idx for idx, error in enumerate(reconstruction_errors) if error > threshold]

    test_acc = (len(test_loader) - len(anomalies)) / len(test_loader)
    print("準確率:", test_acc)

    return f"模型訓練完成，模型權重已儲存至 {model_save_path}", test_acc

def serve_layout():
    # 定義應用的佈局
    folder_path = "./model_weights"
    file_options = get_file_options(folder_path)
    layout = html.Div([
        html.H1("重新訓練模型與部屬模型"),
        html.Div([
            dcc.Upload(
                id = 'choose-file',
                children = dbc.Button('選擇檔案', color="primary"),
                multiple = False,  # 如果你只需要一次選擇一個檔案，將此設為False
                style = {
                    'display': 'inline-block',
                    'alignItems': 'center',
                    'marginRight': '10px' # 右邊距用來隔開按鈕和檔案名稱顯示
                }  # 設定為內聯顯示以與文本對齊
            ),
            html.Div(
                id = 'output-file-name', 
                style = {
                    'display': 'inline-block', 
                    'alignItems': 'center',  # 垂直居中對齊文本
                    # 'height': '30px'
                }
            )
        ], style = {
            'display': 'flex',
            'alignItems': 'center'
            }
        ),
        html.Div([  # 新增輸入框和其標籤
            html.Label("請輸入儲存模型的檔名:", style={'marginRight': '10px'}),
            dcc.Input(
                id='model-name-input',
                type='text',
                placeholder='輸入模型名稱',
                style={'marginRight': '10px', 'width': '200px'}
            ),
            dbc.Button('重新訓練模型權重', id='train_btn', color="primary")
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'marginTop': '20px'
        }),
        html.Div(id='training-output', style={'marginTop': '20px'}),
        html.Div([  # 新增加的下拉式選單和確認按鈕
            dcc.Dropdown(
                id='dropdown',
                options=file_options,
                style={'width': '200px', 'marginRight': '20px'},  # 設定下拉選單的寬度和右邊距
                placeholder="Select an option"
            ),
            dbc.Button('確認', id='confirm_btn',color="primary")
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'marginTop': '20px'
        }),
        html.Div(id='output-dropdown', style={'marginTop': '10px'})  # 顯示選擇的下拉選項
    ], style=STYLE  # 將所有元素置中對齊
    )
    return layout

# # 使用回調來顯示上傳檔案的名稱
# @callback(
#     Output('output-file-name', 'children'),
#     Input('choose-file', 'filename')
# )
# def update_output(filename):
#     if filename is not None:
#         return html.Div([
#             html.H5("選擇的檔案為:", style={'marginRight': '10px', 'display': 'inline'}),
#             html.P(filename, style={'display': 'inline'})
#         ], style={'display': 'flex', 'alignItems': 'center'})
#     else:
#         return "尚未選擇檔案，請確保檔案格式為 .pcap"

@callback(
    Output('training-output', 'children'),
    Input('train_btn', 'n_clicks'),
    State('choose-file', 'filename'),
    State('model-name-input', 'value')
)
def train_model_weights(n_clicks, filename, model_name):
    if n_clicks:
        if filename is None or filename.endswith('.pcap') is False:
            return "請選擇要訓練的檔案，並確保檔案格式為 .pcap"
        if model_name is None:
            return "請輸入儲存模型的檔名"
        txt, acc = train_model(filename, model_name)
        return f"{txt}，準確率為: {acc}"
    return ""

# 使用回調來顯示選擇的下拉選項
@callback(
    Output('output-dropdown', 'children'),
    Input('confirm_btn', 'n_clicks'),
    State('dropdown', 'value')
)

def handle_model_selection(n_clicks, selected_model):
    if n_clicks is None:
        return dash.no_update
    
    if selected_model:
        success = update_model_path_in_config(selected_model)
        if success:
            return f"設定檔已更新，目前模型路徑為: {selected_model}"
        else:
            return "配置失敗"
    else:
        return ""

