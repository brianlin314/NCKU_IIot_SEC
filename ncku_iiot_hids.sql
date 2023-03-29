CREATE TABLE `AGENT`(
    Agent_id VARCHAR(3) NOT NULL,
    Agent_name VARCHAR(100) NOT NULL,
    PRIMARY KEY(Agent_id)
);

CREATE TABLE `USB_CDB`(
    Cdb_num VARCHAR(100) NOT NULL,
    Agent_id VARCHAR(3) NOT NULL,
    PRIMARY KEY(Cdb_num, Agent_id),
    FOREIGN KEY(Agent_id) REFERENCES AGENT(Agent_id)
);

CREATE TABLE `USB_LOG`(
    In_timestamp DATETIME NOT NULL,
    SerialNUM VARCHAR(100) NOT NULL,
    Out_timestamp DATETIME,
    Agent_id VARCHAR(3) NOT NULL,
    Authorized VARCHAR(5) NOT NULL,
    Connected INT NOT NULL,
    USBPort VARCHAR(10) NOT NULL,
    PRIMARY KEY(In_timestamp, SerialNUM),
    FOREIGN KEY(Agent_id) REFERENCES AGENT(Agent_id)
);

