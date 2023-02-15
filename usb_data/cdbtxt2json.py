import json
# 將txt的值轉換成json
def c2j():
    cdbtxt=open("./usb_data/cdb.txt","r")
    cdbjson=open("./usb_data/usb_cdb.json","w")
    clines=cdbtxt.readlines()
    cdb_temp={}
    for line in clines:
        line=line.strip()
        cdb_temp["cdb_SN"]=line.split(" ")[0]
        cdb_temp["Aid"]=line.split(" ")[1]
        json.dump(cdb_temp,cdbjson)
        cdbjson.write("\n")
    cdbjson.close()
    cdbtxt.close()