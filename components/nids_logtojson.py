import json
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
