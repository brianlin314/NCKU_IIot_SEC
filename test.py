import os

lists = os.listdir("./wirepcap/pcap/")     #列出目錄的下所有文件和文件夾保存到lists

q_list = []
for pcap in lists:
    print(os.path.getsize("./wirepcap/pcap/"+pcap))