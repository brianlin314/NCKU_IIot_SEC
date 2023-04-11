import json
from time import sleep
import ast
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import smtplib
import socket

# 去讀wazuh log檔，找出目前有多少usb插在端點上，且列出詳細資訊

if __name__ == "__main__":

    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["from"] = "ne6111071@gs.ncku.edu.tw"  #寄件者
    content["to"] = ",brian0314b@gmail.com,,P76115038@gs.ncku.edu.tw,,x0917364931@gmail.com,,fico880227@gmail.com,,P78111014@gs.ncku.edu.tw," #收件者
    content["subject"] = "NCKU_IIoT_SEC 已偵測到非法 USB 插入 " #郵件標題

    timestamp_check = "1990-01-01T00:00:00.000"
    while True:
        with open("/var/ossec/logs/alerts/alerts.json","r") as jsonfiles:
            lines = jsonfiles.readlines()
            for i in range(len(lines)-1, -1, -1):
                usb_detail = {}
                cdb = open("./usb_data/usb_cdb.json","r") # 開啟白名單檔案
                cdb_line = cdb.readlines()
                info = json.loads(lines[i])
                timestamp1 = info["timestamp"].split("+")[0]
                if timestamp1 == timestamp_check:
                    break
                else:
                    if info["rule"]["id"] == '81104' and info["location"] == '/var/log/kern.log':
                        usb_detail["Timestamp"] = info["timestamp"].split("+")[0]
                        usb_detail["agent_id"] = info["agent"]["id"]
                        usb_detail["agent_name"] = info["agent"]["name"]
                        usb_detail["authorized"] = "black"
                        full_log=info["full_log"].split(" ")
                        usb_detail["SerialNum"] = full_log[-1]

                        if "SerialNumber" not in usb_detail["SerialNum"]:
                            for cline in cdb_line:
                                cline = ast.literal_eval(cline)
                                if usb_detail["SerialNum"] == cline["cdb_SN"] and cline["Aid"] == usb_detail["agent_id"]:
                                    usb_detail["authorized"] = "white"
                            usb_port=full_log[-3].strip(":")
                            usb_detail["UsbPort"] = full_log[-3].strip(":")

                            if usb_detail["authorized"] == "black":
                                print("detect USB black!")
                                msg=("時間戳記 : " + usb_detail["Timestamp"] + "\n" +
                                    "裝置 ID : " + usb_detail["agent_id"] + "\n" +
                                    "裝置名稱 : " + usb_detail["agent_name"] + "\n" + 
                                    "USB 序列號 : " + usb_detail["SerialNum"])
                                content.attach(MIMEText(msg))  # 郵件內容
                                with smtplib.SMTP(host = "smtp.gmail.com", port = "587") as smtp:  # 設定SMTP伺服器
                                    print("SMTP finished")
                                    try:
                                        smtp.ehlo()  # 驗證SMTP伺服器
                                        smtp.starttls()  # 建立加密傳輸
                                        smtp.login("ne6111071@gs.ncku.edu.tw", "awstljcoltsfkuas")  # 登入寄件者gmail
                                        smtp.send_message(content)  # 寄送郵件
                                        print("郵件傳送成功!", "傳送資訊為:", usb_detail)
                                    except Exception as e:
                                        print("郵件傳送失敗,錯誤訊息: ", e)
                                #給agent警告訊息，三色燈與蜂鳴器警報
                                HOST = '192.168.65.7'
                                PORT = 9453

                                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                s.connect((HOST, PORT))
                                while True:
                                    s.send("red".encode())
                                    print("wait for message")
                                    data = s.recv(1024)
                                    print ("server send : ", data.decode())
                                    if data.decode() == "Done":
                                        cmd = "ACK!"
                                        cmd = cmd.encode()
                                        s.send(cmd)
                                        s.shutdown(2)
                                        s.close()
                                        break
                                
                        

            info = json.loads(lines[-1])
            timestamp_check = info["timestamp"].split("+")[0]