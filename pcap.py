import cicflowmeter
import os
import pandas as pd
import keras
from keras.models import load_model

def ai_result():

    # global pcapdirpath, csvpath, agentpcap_dirpath, serverdirpath, modelpath
    # pcapdirpath = ""
    csvpath = "/feature.csv"
    # agentpcap_dirpath = "" 
    # serverdirpath = ""
    modelpath = "/CICIDS2018_model-2.h5"

    # access_cmd = (f"scp -r {agentpcap_dirpath} {pcapdirpath}")
    # os.system(access_cmd)
    # os.system(f"cicflowmeter -f {pcapdirpath} -c {csvpath}")

    model = load_model(modelpath)

    file = pd.read_csv(csvpath)
    file = file.drop(columns = ["Timestamp", "Protocol","PSH Flag Cnt","Init Fwd Win Byts","Flow Byts/s","Flow Pkts/s"], axis=1)
    result = model.predict(file)
    print(result)
    return result