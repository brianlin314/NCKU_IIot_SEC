from datetime import datetime
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
import datetime
import smtplib

# 08/21/2022-13:51:34.630152  [**] [1:1000001:1] Possible DDoS attack [**] [Classification: (null)] [Priority: 3] {TCP} 11.196.20.74:8368 -> 192.168.65.10:80
def description(rule_num):
    line_list = rule_num.split(' [**] ')        # split to 3 parts
    Timestamp = line_list[0].strip().split('-')     # 08/21/2022-13:51:34.630152
    Date = Timestamp[0]     # Date : 08/21/2022 
    Time = Timestamp[1].split('.')[0]       # Time : 13:51:34
    sid = line_list[1].split(' ')       # sid : [1:1000001:1]
    line_list[1] = line_list[1].replace(sid[0], '')
    rule_discribe = line_list[1].strip()
    return Date,Time,rule_discribe
def latest_rule_detail(rule_num_latest):
    rule_info={}
    last=lines[-1] #取出log檔的最後一行
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
def timeInterval(time1,time2):
    """
    time1-time2
    """
    dt1=datetime.datetime.strptime(time1,'%H:%M:%S')
    dt2=datetime.datetime.strptime(time2,'%H:%M:%S')
    d=dt1-dt2
    snd=d.total_seconds()
    return snd

if __name__ == '__main__':
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["from"] = "P76111262@gs.ncku.edu.tw"  #寄件者
    #content["to"] = "fico880227@gmail.com" #收件者
    content["to"] = "brian0314b@gmail.com" #收件者
    content["subject"] = "NCKU_IIoT_SEC-NIDS 已偵測到裝置受到網路危害" #郵件標題
    while(1):
        #sleep(100)
        with open("/var/log/suricata/fast.log","r") as logfiles:
            email_bool=0 #判斷是否要寄信
            lines=logfiles.readlines() #
            rule_num_latest=lines[-1] #
            latest_rule_info=latest_rule_detail(rule_num_latest) # 抓出最新一筆的log的詳細資料
            if latest_rule_info["Rule Discription"] == 'SURICATA Applayer Detect protocol only one direction': #每次寄完信，都會噴出這條規則，拿這條規則當作已經寄過信的證明
                continue
            #print("latest_rule_info:")
            #print(latest_rule_info)
            check_rule_same=0 #判斷最新的規則跟過去4個規則是否存在相同
            if latest_rule_info["Priority"]=="1": #寄給經理級
                for i in range(-2,-6,-1):
                    Date,Time,rule_discribe=description(lines[i]) #check_list保存fast.log倒數-2~-5筆資料的timestamp和rule description
                    res=timeInterval(latest_rule_info["Time"],Time)
                    if latest_rule_info["Rule Discription"] == rule_discribe and latest_rule_info["Date"] == Date and res > 300.0: #規則相同/日期相同/時間間隔大於10分鐘
                        print("F1 rule")
                        print(res)
                        email_bool=1
                        break
                    elif latest_rule_info["Rule Discription"] == rule_discribe and latest_rule_info["Date"] != Date: #規則相同/日期不同
                        #print("F2")
                        print(res)
                        email_bool=1
                        break
                    elif latest_rule_info["Rule Discription"] != rule_discribe:
                        #print("F3")
                        print(res)
                        check_rule_same+=1
                if check_rule_same==4: #最新的規則跟過去4個規則皆不同
                    email_bool=1
                if email_bool == 1:
                    msg=("日期: "+latest_rule_info['Date']+"\n"+
                        "時間: "+latest_rule_info['Time']+"\n"+
                        "規則ID: "+latest_rule_info['Signature Id']+"\n"+
                        "事件描述: "+latest_rule_info['Rule Discription']+"\n"+
                        "事件分類: "+latest_rule_info['Classification']+"\n"+
                        "事件等級: "+latest_rule_info['Priority']+"\n"+
                        "事件協定: "+latest_rule_info['Protocol']+"\n"+
                        "攻擊來源: "+latest_rule_info['Source']+"\n"+
                        "攻擊目標: "+latest_rule_info['Destination'])
                    content.attach(MIMEText(msg))  #郵件內容
                    #content.attach(MIMEImage(Path("hacker.jpg").read_bytes()))  # 郵件圖片內容
                    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
                        try:
                            smtp.ehlo()  # 驗證SMTP伺服器
                            smtp.starttls()  # 建立加密傳輸
                            smtp.login("P76111262@gs.ncku.edu.tw", "hzooyjrqcnpgomjp")  # 登入寄件者gmail
                            smtp.send_message(content)  # 寄送郵件
                            print("郵件傳送成功!")
                        except Exception as e:
                            print("郵件傳送失敗,錯誤訊息: ", e)
            else:
                continue
        sleep(5)