import json
import re
# 把 NIDS 的 log 轉成 json
def log2json(filename):
    f = open(filename, 'r')
    jf = open('/var/log/suricata/fast.json', 'w', newline='')
    lines = f.readlines()
    line_info = {}
    jf.write('[')
    check=len(lines)
    checking=0
    for line in lines:
        checking+=1
        line_list = line.split(' [**] ')
        Timestamp = line_list[0].strip().split('-')
        line_info['Date'] = Timestamp[0]
        line_info['Time'] = Timestamp[1].split('.')[0]
        sid = line_list[1].split(' ')
        line_list[1] = line_list[1].replace(sid[0], '')
        sid = sid[0].split(':')[1]
        line_info['Signature Id'] = sid
        line_info['Rule Discription'] = line_list[1].strip()
        suri_type = line_list[2].split('] ')
        line_info['Classification'] = suri_type[0].replace('[Classification: ', '')
        line_info['Priority'] = suri_type[1].replace('[Priority: ', '')
        protocol = suri_type[2].split(' ')
        proto = protocol[0][1:-1]
        line_info['Protocol'] = proto
        line_info['Source'] = protocol[1]
        line_info['Destination'] = protocol[3].strip()
        json.dump(line_info, jf)
        if checking != check:
            jf.write(',')
            jf.write('\n')
    jf.write(']')
    f.close()
    jf.close()

def log2dic(line):
    keyList = ['Date', 'Time', 'Sinature id', 'Rule Discription', 
               'Classification', 'Priority', 'Protocol', 'Source', 'Destination']
    
    dic = {}
    ######################################################
    ##      Ollie: split所有特殊符號，留下有意義的部分       ##
    ##      Ollie: 這個方法要import re                    ##
    ##      Ollie: r""裡面的格式叫做RegEx正規寫法           ##
    ##      Ollie: 以下為參考的示例                        ##
    ##           \[ : 左括號                             ##
    ##            | : 或                                ##
    ##         \]\s : 右括號+空白鍵                       ##
    ## \s\[\*\*\]\s : " [**] "                          ##
    ##           \{ : 左大括號                           ##
    ##         \}\s : 右大括號+空白鍵                     ##
    ######################################################

    info_split = re.split(r"\[|\]\s|\s\[\*\*\]\s|\{|\}\s", line)
    clean_info = list(filter(None, info_split))

    dic['Date'] = clean_info[0].split('-')[0].strip()
    dic['Time'] = clean_info[0].split('-')[1].strip()
    dic['Signature_Id'] = clean_info[1].split(':')[1]
    dic['Rule_Discription'] =  clean_info[2]
    dic['Classification'] = clean_info[3].split(':')[1].strip()
    dic['Priority'] = clean_info[4].split(':')[1].strip()
    dic['Protocol'] = clean_info[5]
    dic['Source'] = clean_info[6].split('->')[0].strip()
    dic['Destination'] = clean_info[6].split('->')[1].strip()

    return dic
###########測試用input##############
# logtodic("04/04/2023-15:25:03.863168  [**] [1:5000066:1676950202] ETN AGGRESSIVE IPs Group 66 [**] [Classification: Misc Attack] [Priority: 2] {TCP} 62.204.41.8:55769 -> 140.116.82.33:2108")