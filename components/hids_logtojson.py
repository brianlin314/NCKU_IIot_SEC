import pandas as pd
import ast
import json

def log2json(path):
    f = open(path,"r")
    Lines = f.readlines()
    jsons=[]
    count = 0
    # 轉換成正常JSON格式
    for line in Lines:
        count += 1
        if "false" in line:
            line = line.replace('false', "'false'")
        if "true" in line:
            line = line.replace('true', "'true'")
        json_data = ast.literal_eval(line)
        jsons.append(json_data)
    
    path1 = path.split('.')[0]+'_1.json'
    with open(path1, "w") as f:
        json.dump(jsons, f, indent = 4)
