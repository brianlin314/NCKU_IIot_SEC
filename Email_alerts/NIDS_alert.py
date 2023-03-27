from datetime import datetime
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import smtplib

# {'Date': '03/13/2023', 'Time': '15:16:21', 'Signature Id': '2210042', 'Rule Discription': 'SURICATA STREAM TIMEWAIT ACK with wrong seq', 
# 'Classification': 'Generic Protocol Command Decode', 'Priority': '3', 'Protocol': 'TCP', 'Source': '20.42.72.131:443', 'Destination': '172.20.10.3:46468'}
def latest_rule_describe(latest_rule):
    rule_info = {}
    last = latest_rule      # fetch latest rule
    line_list = last.split(' [**] ')
    Timestamp = line_list[0].strip().split('-')
    rule_info['Date'] = Timestamp[0]
    rule_info['Time'] = Timestamp[1].split('.')[0]
    sid = line_list[1].split(' ')
    line_list[1] = line_list[1].replace(sid[0], '')
    sid = sid[0].split(':')[1]
    rule_info['Signature Id'] = sid
    rule_info['Rule Discription'] = line_list[1].strip()
    suri_type = line_list[2].split('] ')
    rule_info['Classification'] = suri_type[0].replace('[Classification: ', '')
    rule_info['Priority'] = suri_type[1].replace('[Priority: ', '')
    protocol = suri_type[2].split(' ')
    proto = protocol[0][1:-1]
    rule_info['Protocol'] = proto
    rule_info['Source'] = protocol[1]
    rule_info['Destination'] = protocol[3].strip()
    return rule_info

if __name__ == '__main__':
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["from"] = "P76111262@gs.ncku.edu.tw"  #寄件者
    content["to"] = ",brian0314b@gmail.com,,P76115038@gs.ncku.edu.tw,x0917364931@gmail.com,fico880227@gmail.com,P78111014,P78111014@gs.ncku.edu.tw," #收件者
    content["subject"] = "NCKU_IIoT_SEC-NIDS 已偵測到裝置受到網路危害" #郵件標題
    count = 0
    while True:
        with open("/var/log/suricata/fast.log","r") as logfiles:
            lines = logfiles.readlines()
            rule_latest = lines[-1]
            latest_rule_info = latest_rule_describe(rule_latest) # 抓出最新一筆的log的詳細資料
            check_Time = '' 
            check_rule = ''
            if latest_rule_info["Priority"] == "1" and check_Time != latest_rule_info['Time'] and check_rule != latest_rule_info['Rule Discription']:
                check_Time = latest_rule_info['Time']
                check_rule = latest_rule_info['Rule Discription']
                msg=("日期: " + latest_rule_info['Date'] + "\n" +
                    "時間: " + latest_rule_info['Time'] + "\n" +
                    "規則ID: " + latest_rule_info['Signature Id'] + "\n" + 
                    "事件描述: " +latest_rule_info['Rule Discription'] + "\n" + 
                    "事件分類: " +latest_rule_info['Classification'] + "\n" + 
                    "事件等級: " + latest_rule_info['Priority'] +"\n" + 
                    "事件協定: " + latest_rule_info['Protocol'] + "\n" + 
                    "攻擊來源: " + latest_rule_info['Source'] + "\n" + 
                    "攻擊目標: " + latest_rule_info['Destination'])
                content.attach(MIMEText(msg))  # 郵件內容
                with smtplib.SMTP(host = "smtp.gmail.com", port = "587") as smtp:  # 設定SMTP伺服器
                    try:
                        smtp.ehlo()  # 驗證SMTP伺服器
                        smtp.starttls()  # 建立加密傳輸
                        smtp.login("P76111262@gs.ncku.edu.tw", "")  # 登入寄件者gmail
                        smtp.send_message(content)  # 寄送郵件
                        print("郵件傳送成功!")
                    except Exception as e:
                        print("郵件傳送失敗,錯誤訊息: ", e)
            else:
                sleep(1)
                continue
        

