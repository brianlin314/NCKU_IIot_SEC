# dashboard
## 路徑、密碼更改
請先到 globals.py 中更改 sudoPassword, dir_path

sudoPassword 是指使用者密碼

dir_path 是 filebeat 收集 alert json files 的路徑, 預設為 /var/ossec/logs/alerts

## 環境安裝
```
git clone https://github.com/cliff0917/dashboard.git
sudo apt-get install -y mongodb
conda create -y -n dashboard python=3.7
conda activate dashboard
cd dashboard
pip install -r requirements.txt
python app.py
```

## 可能遇到的問題
* oserror: [errno 98] address already in use

  使用以下指令
  ```
  sudo lsof -t -i tcp:8050 | xargs kill -9
  ```
