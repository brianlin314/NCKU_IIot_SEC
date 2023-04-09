import logging
import json 

logging.basicConfig(filename='usb.log', level=logging.DEBUG)

with open("../usb_data/usb_info.json", "w") as jsonfiles:
    lines = jsonfiles.readlines()
    for line in lines:
        info = json.loads(line)
        print(info)
logging.info('This is an info message')
logging.warning('This is a warning message')
