import json
import yaml
from logger import Logger
from database import MySQLDatabase
import socket

logger = Logger()
with open("../config.yml", 'r') as stream:
    try:
        args = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logger.echo(exc)
    
my_database = MySQLDatabase(args, logger)
my_database.connect()
my_database.create_table(inplace=False)
        

class MyServer():
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        
    def run(self):
        logger.log(f"Server started at {self.host}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            
            while True:
                try:
                    conn, addr = s.accept()
                    with conn:
                        logger.log(f'Connected by {addr}')
                        data = b''
                        while True:
                            chunk = conn.recv(1024)
                            if not chunk:
                                break
                            data += chunk
                            
                        req_datas = data.decode('utf-8').split("=")[-1]
                        print(req_datas)
                        json_data = json.loads(req_datas)
                        my_database.insert(json_data, mac="54:f2:94:0f:71:ba")
                        
                except Exception as e:
                    if e != KeyboardInterrupt:
                        logger.log(e)
                    continue
                    
        
    def kill_self(self):
        logger.log("Server closed")
        my_database.close()
        exit(0)


def main():
    my_server = MyServer(host="192.168.195.45", port=8000)
    try:
        my_server.run()
    except KeyboardInterrupt:
        my_server.kill_self()

#------------------------------ Main Function ---------------------------------

if __name__ == '__main__':
    main()