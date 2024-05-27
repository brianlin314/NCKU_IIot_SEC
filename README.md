# NCKU_IIoT_SEC 環境安裝
## 使用 Ubuntu 22.04 

可使用虛擬機安裝 ubuntu 系統，或者是灌雙系統

虛擬機安裝ubuntu教學 : https://www.kjnotes.com/linux/29

雙系統教學 : https://www.youtube.com/watch?v=yMHOpOuyjdc&t=208s&ab_channel=%E5%A2%9E%E5%BB%A3%E5%BB%BA%E6%96%87

--- 



## 安裝 Guest Additions
Guest Additions 使虛擬機器與主機系統之間的操作更加方便，提供更好的整合性和性能。

- [參考資料1](https://medium.com/%E8%8A%B1%E5%93%A5%E7%9A%84%E5%A5%87%E5%B9%BB%E6%97%85%E7%A8%8B/%E8%A7%A3%E6%B1%BAvirtualbox%E7%84%A1%E6%B3%95%E9%9B%99%E5%90%91%E8%A4%87%E8%A3%BD%E8%B2%BC%E4%B8%8A-1554d5a81da0)
- [參考資料2](https://www.linuxtechi.com/install-virtualbox-guest-additions-on-ubuntu/)
 
1. 安裝
    ```shell=
    sudo apt update
    sudo apt install dkms build-essential linux-headers-generic 
    ```
    
2. 裝置 > 插入 Guest Additions CD 映像
    ![](https://i.imgur.com/UIUoUj9.png) 
    
3. 重新安裝 GA，右上角的 "Run Software" 點下去!
    ![](https://i.imgur.com/yKqmqS8.png)

    ![](https://i.imgur.com/r1Drplx.png) 

4. 重啟
    ```shell=
    sudo reboot
    ```
---

## 若選擇虛擬機安裝系統，要先解決網路問題

- 下圖是無法對外連線的 VM
![](https://i.imgur.com/XlPQ9Dp.png)
    
- 使用橋接介面卡方可對外連線
![](https://i.imgur.com/e3oBqJI.png)
    
- 記得勾全部允許
![](https://i.imgur.com/s06Hrhq.png)

--- 

# NCKU_IIoT_SEC 系統安裝
## **Wazuh Server 安裝**
:::warning
Wazuh Server 與 Wazuh Agent 必須裝在不同的 PC 上
:::
### Step1. Host based IDS 的管理(Manager)
1. 先進入root權限
    ```shell=
    sudo -s
    ```
    :::info
    `tips:`可以按 `ctrl+d` 退出root
    :::

    
2. 安裝 (Install the necessary packages)
    ```shell=
    apt install curl apt-transport-https unzip wget libcap2-bin software-properties-common lsb-release gnupg
    ```

3. Install the GPG key
    ```shell=
    curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | gpg --no-default-keyring --keyring gnupg-ring:/usr/share/keyrings/wazuh.gpg --import && chmod 644 /usr/share/keyrings/wazuh.gpg
    ```

4. Add the repository
    ```shell=
    echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | tee -a /etc/apt/sources.list.d/wazuh.list
    ```

5. 更新
    ```shell=
    apt-get update
    ```

6. 安裝
    ```shell=
    apt-get install wazuh-manager
    ```

7. Enable and Start service
    ```shell=
    systemctl daemon-reload
    systemctl enable wazuh-manager
    systemctl start wazuh-manager
    ```

8. 確認是否有正常 "active"
    ```shell=
    systemctl status wazuh-manager
    ```
    :::info
    `tips`: `ctrl+c`退出
    :::

---
## **Suricata 安裝**
### Step2. Network based IDS安裝

1. 安裝
    ```shell=
    add-apt-repository ppa:oisf/suricata-stable
    apt update
    apt install suricata jq vim
    ```

2. 設定 IDS 所偵測的 network interface，先輸入`ip addr`，檢查自己的 network interface

    ![](https://i.imgur.com/vSHTCte.png)

    :::info
    `vim` 操作教學:

    `tips`:按 `i` 進入編輯模式，按 `esc` 回到閱讀模式

    輸入 `:wq` 退出 vim，輸入 `/` 可進行搜尋
    :::

3. 設定

    ```shell=
    vim /etc/suricata/suricata.yaml  #進入suricata設定檔
    ```
    針對以下片段進行修改
    ```yaml=
    ## in suricata.yaml##

    af-packet:
        - interface: *your network interface (e.g. ens160)*
          cluster-id: 99
          cluster-type: cluster_flow
          defrag: yes
          use-mmap: yes
          tpacket-v3: yes
    ```
    ```yaml
    pcap:
        - interface: enp0s3
        # On Linux, pcap will try to use mmap'ed capture and will use "buffer-size"
        # as total memory used by the ring. So set this to something bigger
        # than 1% of your bandwidth.
        #buffer-size: 16777216
        #bpf-filter: "tcp and port 25"
        .....
    ```

    設定 IDS 的 內網和外網
    ```yaml=
    ##in /etc/suricata/suricata.yaml##
    vars:
      # more specific is better for alert accuracy and performance
        address-groups:
           #HOME_NET: "[192.168.0.0/16, 10.0.0.0/8,172.16.0.0/12]"
           HOME_NET:"[*suricata 所監控 network interface 的 ip*]" #這邊要修改成這樣，ex:192.168.0.20/24
           #HOME_NET:"[192.168.0.0/16]"
           #HOME_NET:"[10.0.0.0/8]"
           #HOME_NET:"[172.16.0.0/12]"
           #HOME_NET:"any"

           EXTERNAL_NET: "!$HOME_NET" #這邊要修改成這樣

    ```
    
    ```yaml=
    # Configure the type of alert (and other) logging you would like.
    outputs:
      # a line based alerts log similar to Snort's fast.log
      - fast:
          enabled: yes
          filetype: regular
          filename: /var/log/suricata/%Y/fast-%m-%d.log
          append: yes
          rotate-interval: day
    ```
4. 安裝規則到Suricata
    ```shell=
    suricata-update
    ```

5. 嘗試新增規則檔:
    以下為新增偵測 DDoS 的 rule 的範例:
    在 `/var/lib/suricata/rules` 中新增規則檔，指令如下:
    ```shell=
    sudo vim /var/lib/suricata/rules/test-ddos.rules
    ```

    接著在規則檔中填入如下規則:
    ```vim
    alert tcp any any -> $HOME_NET any (msg: "Possible DDoS attack!"; flags: S; flow: stateless; threshold: type both, track by_dst, count 1000, seconds 1; classtype: misc-attack; priority:1; sid:1000001; rev:1;)
    ```

    最後記得設定 IDS 的 設定檔 `vim /etc/suricata/suricata.yaml`
    ```yaml=
    rule-files:
        - suricata.rules
        - test-ddos.rules #要加上這條
    ```
6. 重啟 NIDS
    ```shell=
    systemctl restart suricata
    ```

    添加規則後，請務必驗證 Suricata 的配置。為此，請運行以下命令：
    ```shell=
    sudo suricata -T -c /etc/suricata/suricata.yaml -v
    ```
    
- 創建規則參考資料： https://hackmd.io/5q4wKkr2T0enMZ2FfkHxwQ

#### 測試NIDS
1. 在另一台 PC 上安裝 hping3
    ```shell=
    apt-get install hping3
    ```

2. hping3 模擬 DDoS 攻擊，命令如下:
    ```shell=
    sudo hping3 -S -p 80 --flood --rand-source $被攻擊的那台主機的IP$
    ```
    ![](https://i.imgur.com/fVUtOpi.png)

3. 在被攻擊的那台主機(即裝有 IDS 的主機) 輸入以下命令:
    ```shell
    tail -f /var/log/suricata/fast.log
    ```

    便能看到偵測到 DDoS 攻擊所產生的對應 log
    ![](https://i.imgur.com/wqCP7l1.png)
    :::info
    `tips` : `ctrl+c` #退出
    :::

---
## **Wireshark 安裝**
### Step3. 安裝 Wireshark (用於抓取 AI 所需 Network Flows):
1. 安裝
    ```shell=
    sudo apt update
    sudo apt install wireshark
    sudo dpkg-reconfigure wireshark-common
    sudo chmod +x /usr/bin/dumpcap
    ```

2. 新增使用者到wireshark(不新增會沒有權限):
    ```shell=
    sudo adduser $USERNAME wireshark
    ```

---
## **環境安裝**
### step4. 安裝anaconda
- [anaconda官網](https://repo.anaconda.com/archive/)

1. 下載安裝包指令 (嘗試更換最新版 Anaconda)
      
    ```shell=
    sudo wget https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
    ```
2. 安裝anaconda3
    ```shell=
    bash Anaconda3-2023.09-0-Linux-x86_64.sh 
    ```
3. 測試conda 是否安裝成功
    ```shell=
    conda --version
    ```
    若失敗，則要修改環境變數

    ![](https://i.imgur.com/H87j5E9.png)

    ```shell=
    vim ~/.bashrc
    ```
    將以下指令加在最後
    
    ```vim=
    # added by Anaconda3 5.3.1 installer
    # >>> conda init >>>
    # !! Contents within this block are managed by 'conda init' !!
    __conda_setup="$(CONDA_REPORT_ERRORS=false '/home/server/anaconda3/bin/conda' shell.bash hook 2> /dev/null)"
    if [ $? -eq 0 ]; then
        \eval "$__conda_setup"
    else
        if [ -f "/home/server/anaconda3/etc/profile.d/conda.sh" ]; then
            . "/home/server/anaconda3/etc/profile.d/conda.sh"
            CONDA_CHANGEPS1=false conda activate base
        else
            \export PATH="/home/server/anaconda3/bin:$PATH"
        fi
    fi
    export PATH="/home/server/anaconda3/bin:$PATH"
    unset __conda_setup
    # <<< conda init <<<
    ```
    ![](https://i.imgur.com/HdJNQpB.png)
    :::warning
    注意: 請修改全部的 anaconda 路徑，不要直接複製貼上!
    :::

    
    修改完成後，執行以下
    ```shell=
    source ~/.bashrc
    ```
    ![](https://i.imgur.com/15FDs4D.png)


--- 

### step5. Docker 安裝
- [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

1. Set up Docker's apt repository.
    ```shell=
    # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    # Add the repository to Apt sources:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    ```
2. Install the Docker packages.
    ```shell=
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```
3. Verify that the Docker Engine installation is successful by running the `hello-world` image.
    ```shell=
    sudo docker run hello-world
    ```
4. 將 docker 加入群組，之後就不用 sudo
    ```shell=
    sudo usermod -aG docker <your_username>
    ```
5. 重啟
    ```shell=
    sudo reboot
    ```
---

### step6. mongoDB 安裝
1. 新增一個 docker-compose.yaml 文件
    ```yaml=
    # Use root/example as user/password credentials
    version: '3.1'

    services:

      mongo:
        image: mongo:4.1.10
        restart: always
        ports:
          - 27017:27017
        environment:
          MONGO_INITDB_ROOT_USERNAME: root
          MONGO_INITDB_ROOT_PASSWORD: ncku

      mongo-express:
        image: mongo-express
        restart: always
        ports:
          - 8081:8081
        environment:
          ME_CONFIG_MONGODB_ADMINUSERNAME: root
          ME_CONFIG_MONGODB_ADMINPASSWORD: ncku
          ME_CONFIG_MONGODB_URL: mongodb://root:ncku@mongo:27017/
    ```
2. 開啟 docker
    ```shell=
    sudo docker compose up
    ```
3. 確定是否成功，到 `http://localhost:8081/`，帳號: `admin`、密碼: `pass`
    ![image](https://hackmd.io/_uploads/rJEVFO15a.png)

#### 在 cmd 上面互動
1. 先查看 mongo 的 container id
    ```shell=
    docker ps
    ```
2. 輸入指令
    ```shell=
    docker exec -it <your mongo id> mongo
    ```
3. 進入以後，需驗證密碼
    ```cmd=
    > use admin
    switched to db admin

    > db.auth("root", "ncku")
    1
    
    > show dbs
    admin     0.000GB
    config    0.000GB
    local     0.000GB
    pythondb  0.000GB
    
    > use pythondb
    > db.posts.count() 
    > db.posts.find().pretty()
    ```
---
## **系統安裝**
### step7. NCKU_IIoT_SEC Dashboard 安裝
- Github連結: https://github.com/brianlin314/NCKU_IIot_SEC

1. Git clone 下載檔案
    ```shell=
    git clone https://github.com/brianlin314/NCKU_IIot_SEC.git
    ```
2. 下載完成後，請先新增一 `config.json` 到該資料夾底下，如下:
    - dash_user_name 與 dash_user_password 為 Dashboard 登入的帳號及密碼
    - sudoPassword 為虛擬機的密碼
    - 請設定 agent_ip 為自己端點的 IP
    ```json=
    {
        "mongoUrl": "mongodb://root:ncku@localhost:27017/",
        "dash_user_name": "", 
        "dash_user_password": "",
        "sudoPassword": "",
        "hidsdirpath": "/var/ossec/logs/alerts/",
        "nidsdirpath": "/var/log/suricata/",
        "pcapdirpath": "./wirepcap/pcap/",
        "csvdirpath": "./wirepcap/csv/",
        "model_path": "anomaly_AE_new.pth",
        "nids_agent_options": [
            {"label": "Server", "value": "Server"},
            {"label": "PCs", "value": "PCs"}
        ],
        "hids_agent_options": [
            {"label": "Server", "value": "Server"},
            {"label": "PC_1", "value": "PC_1"},
            {"label": "PC_2", "value": "PC_2"},
            {"label": "PC_3", "value": "PC_3"}
        ],
        "usb_add_options": [
            {"label": "Server", "value": "000"},
            {"label": "PC_1", "value": "001"},
            {"label": "PC_2", "value": "002"},
            {"label": "PC_3", "value": "003"}
        ],
        "agent_ip": {
            "Server": "255.255.255.255",
            "PCs": "255.255.255.255"
        },
        "agent_id": {
            "Server": "000",
            "PC_1": "001",
            "PC_2": "002",
            "PC_3": "003"
        }
    }
    ```

3. 安裝相關套件及虛擬環境
    ```shell=
    conda create -y -n dashboard python=3.8   # 建立虛擬環境
    conda activate dashboard   # 進入虛擬環境
    conda install pytorch torchvision torchaudio cpuonly -c pytorch   # 安裝 pytorch cpu 版本 
    pip install pandas==1.3.5 pymongo==4.0.1 scikit-learn==1.3.2 dash==2.3.1 dash-bootstrap-components==0.13.1 feffery-antd-components==0.1.5 dash-extensions==0.1.3 Flask==2.0.2 Werkzeug==2.2.2 cicflowmeter==0.1.6 scapy==2.4.3 scipy==1.4.1 numpy==1.18.0   # 安裝相關套件
    cd NCKU_IIot_SEC
    mkdir -p /wirepcap/pcap /wirepcap/csv   # 新增 wireshark 資料夾
    python app.py   # 執行dashboard
    ```
    :::info
    如果安裝套件出現`killed`，輸入`pip install <your-package-name> --no-cache-dir`
    :::

    :::warning
    可能遇到的問題:
    oserror: [errno 98] address already in use
    
    使用以下指令:
    ```shell
    sudo lsof -t -i tcp:8050 | xargs kill -9
    ```
    :::

---

### Step8. 新增 HIDS USB 規則集
1. 將 git clone 下來的檔案裡面的 `local_rules.xml` 取代掉`/var/ossec/etc/rules/local_rules.xml`

    ```xml=
    <!-- Local rules -->

    <!-- Modify it at your will. -->
    <!-- Copyright (C) 2015, Wazuh Inc. -->

    <!-- Example -->
    <group name="local,syslog,sshd,">

      <!--
      Dec 10 01:02:02 host sshd[1234]: Failed none for root from 1.1.1.1 port 1066 ssh2
      -->
      <rule id="5760" level="12" overwrite="yes">
        <if_sid>5700,5716</if_sid>
        <match>Failed password|Failed keyboard|authentication error</match>
        <description>sshd: authentication failed.</description>
        <mitre>
          <id>T1110.001</id>
          <id>T1021.004</id>
        </mitre>
        <group>authentication_failed,gdpr_IV_35.7.d,gdpr_IV_32.2,gpg13_7.1,hipaa_164.312.b,nist_800_53_AU.14,nist_800_53_AC.7,pci_dss_10.2.4,pci_dss_10.2.5,tsc_CC6.1,tsc_CC6.8,tsc_CC7.2,tsc_CC7.3,</group>
       </rule>

    </group>

    <group name="usb,">
        <rule id="81104" level="3">
            <if_sid>81100</if_sid>
            <match>SerialNumber</match>
            <description>usb.serial_number</description>
        </rule>
    </group>

    ```
### Step9. Wireshark 設定
設定 wireshark，及時抓取封包，讓 AI 模型能夠辨識

1. 點開 Wireshark，上方工具欄選擇 Capture 
2. pcap 檔案放置處選擇 `NCKU_IIoT_SEC/wirepcap/pcap/`，檔案大小設為 10 MB
![image](https://hackmd.io/_uploads/HkC0UkcqT.png)

    :::warning
    檔案大小請設定為 10 MB，請勿隨意設置
    :::
### Step10. Wazuh Agent 安裝
:::warning
Wazuh (HIDS) Server 與 Agent 必須在不同 PC 上安裝
請根據欲裝 Agent 的 PC 的作業系統，選擇以下安裝步驟
:::

#### Window 系統安裝教學

1. 前往 [wazuh官網](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-windows.html)，點選 **Windows Installer**

    ![](https://i.imgur.com/FOdSgGk.png)

2. 打開 Wazuh Agent Manager 填入 Server IP， 按 save 後， 再點 **Manage** -> restart

    ![](https://i.imgur.com/HNaXLXU.png)

3. 設定
    ```cmd=
    win + R
    secpol.msc
    ```
    ![](https://i.imgur.com/xHjfjU2.png)
    
####  Linux 系統安裝教學
1. 安裝:
    ```shell=
    curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | gpg --no-default-keyring --keyring gnupg-ring:/usr/share/keyrings/wazuh.gpg --import && chmod 644 /usr/share/keyrings/wazuh.gpg
    echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | tee -a /etc/apt/sources.list.d/wazuh.list
    ```
2. 更新:
    ```shell=
    sudo apt-get update
    ```

    ```shell=
    systemctl daemon-reload
    systemctl enable wazuh-agent
    systemctl start wazuh-agent
    ```
3. 關閉自動更新，避免版本不正確導致無法正常運作。
    ```shell
    sed -i "s/^deb/#deb/" /etc/apt/sources.list.d/wazuh.list
    apt-get update
    echo "wazuh-agent hold" | dpkg --set-selections
    ```
4. 設定 `vim /var/ossec/etc/ossec.conf`，修改 Server ip 為 Server 的 ip
    ```conf=
    <client>
      <server>
        <address>SERVER_IP</address>
        ...
      </server>
    </client> 
    ```
--- 

# 系統相關操作手冊
### 檢查 Wazuh Server 與那些 Agent 相連接
```shell=
sudo /var/ossec/bin/agent_control -l
```
![](https://i.imgur.com/m10rwBi.png)

---

### 解決 Ubuntu 無法連接 USB 問題 (Virtual Box)
1. 先查看 virualbox 的版本，並找到對應的[版本](https://www.virtualbox.org/wiki/Download_Old_Builds)
2. 下載對應的 Extension Pack
3. 更改 USB 的設定，改成 USB 3.0(xHCI) Controller
![](https://i.imgur.com/KvC9Ykz.png)

---  
### Gmail Alert with NIDS and USB
https://hackmd.io/HWSChGurR6S2rwUVCklGtA?view

### cicflowmeter 問題
1. 可能只能在 linux 上運行
2. 若無法順利執行，請檢查以下套件版本是否正確
:::info
numpy==1.18.0 scipy==1.4.1 scapy==2.4.3
:::
3. 如遇以下問題，請到該虛擬環境底下修改檔案
:::danger
```
File "/home/p76111262/anaconda3/envs/thesis/lib/python3.8/site-packages/cicflowmeter/features/flow_bytes.py", line 182, in get_min_forward_header_bytes
    return min(
ValueError: min() arg is an empty sequence
```
:::
```java
def get_min_forward_header_bytes(self) -> int:
        """Calculates the amount of header bytes in the header sent in the opposite direction as the flow.

        Returns:
            int: The amount of bytes.

        """

        packets = self.feature.packets

        forward_cnt = 0
        for packet, direction in packets:
            if direction == PacketDirection.FORWARD:
                forward_cnt += 1
            if forward_cnt == 0:
                return 0
        return min(
            self._header_size(packet)
            for packet, direction in packets
            if direction == PacketDirection.FORWARD
        )
```

