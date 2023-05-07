import pymysql as mysql
import yaml
import datetime
import re
from localizer import BaseLocalizer
import pandas as pd

class MySQLDatabase():
    def __init__(self, args) -> None:
        self.args = args
        
    def get_args(self):
        return self.args

    def connect(self):
        self.db = mysql.connect(host=self.args['host'], user=self.args['user'], passwd=self.args['passwd'], db=self.args['db'])
        self.cursor = self.db.cursor()
        self.log(f"Connected to database {self.args['db']}")
        
    def close(self):
        self.log(f"Closed connection to database {self.args['db']}")
        self.db.close()
        
    def table_exists(self, table_name):
        sql = "show tables;"
        self.cursor.execute(sql)
        tables = [self.cursor.fetchall()]
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]
        if table_name in table_list:
            return True
        else:
            return False

    def create_table(self, inplace=True):
        if not inplace: # 不重写表
            if self.table_exists(self.args['table']):
                self.log(f"Table {self.args['table']} already exists")
                return
            
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.args['table']}")
        
        VARCHAR = "VARCHAR(100)"
        sql = f"""CREATE TABLE {self.args['table']} (
                ID {VARCHAR} NOT NULL,
                MMAC {VARCHAR} NOT NULL,
                TIME {VARCHAR} NOT NULL,
                MAC {VARCHAR} NOT NULL,
                RNG {VARCHAR} NOT NULL,
                RSSI {VARCHAR} NOT NULL )""" # RNG is for RANGE (RANGE is a reserved word)
            
        self.cursor.execute(sql)
        self.log(f"Table {self.args['table']} created")
    
    def insert(self, json_data, mac):
        id: str = json_data['id']
        data: list = json_data['data']
        mmac = json_data['mmac']
        time = json_data['time']
        for datum in data:
            data_mac = datum['mac']
            if data_mac != mac:
                continue
            sql = f"""INSERT INTO {self.args['table']} (ID, MMAC, TIME, MAC, RNG, RSSI) \
            VALUES ('{id}', '{mmac}', '{time}', '{datum['mac']}', '{datum['range']}', '{datum['rssi']}');"""
            self.log(f"Inserting data into {self.args['table']}: {sql}")
            self.cursor.execute(sql)
            self.db.commit()
        
    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def execute(self, sql):
        self.cursor.execute(sql)
        self.db.commit()
        
    def echo(self, msg):
        print(msg)
        
    def log(self, msg):
        print(f"[{datetime.datetime.now()}] - {msg}")
    

# test  
if __name__ == "__main__":
    with open("../config.yml", 'r') as stream:
        try:
            args = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    my_database = MySQLDatabase(args)
    my_database.create_table()