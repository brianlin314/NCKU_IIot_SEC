# NCKU_IIot_SEC Dashboard
## 詳細安裝說明請參考 https://hackmd.io/@Brianlin314/Skjj7Cfnq
## 路徑、密碼更改
請先到 globals_variable.py 中更改 sudoPassword, dir_path, ip ...

sudoPassword 是指使用者密碼，或虛擬機密碼

設定agent_pc_id流程,查看pc對應id,Ex:000,001,002...:
```
sudo -s
cd /var/ossec/bin
./agent_control -l
```

設定ip流程，若不知道port number，可以輸入以指令尋找::
```
sudo tail -f /var/log/suricata/fast.log
```

## 環境安裝
```
git clone https://github.com/brianlin314/NCKU_IIot_SEC.git
sudo apt-get install -y mongodb
conda create -y -n dashboard python=3.7
pip install -r requirements.txt
```

## 開啟dashboard及emai_alert流程
```
conda activate dashboard 
cd NCKU_IIot_SEC
python NIDS_alert.py &  // 將python程式在後台執行，當關閉終端機，該程式也會被shut down
python app.py  // ctrl+左鍵 點選http://127.0.0.1:8050/ 開啟
```

## 可能遇到的問題
* oserror: [errno 98] address already in use

  使用以下指令
  ```
  sudo lsof -t -i tcp:8050 | xargs kill -9
  ```
