import os
import json
import glob
f = open('/var/log/suricata/2023/eve-2023-04-02.json', 'r')
lines = f.readlines()
for i, line in enumerate(lines):
    li = json.loads(line)
    print(li)
    if i > 5:
        break