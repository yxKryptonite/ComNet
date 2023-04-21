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
    def __init__(self, host, port, mobile_mac):
        self.host = host
        self.port = port
        self.mobile_mac = mobile_mac.lower()
        
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
                        json_data = json.loads(req_datas)
                        my_database.insert(json_data, mac=self.mobile_mac)
                        
                except Exception as e:
                    if e != KeyboardInterrupt:
                        logger.log(e)
                    continue
                    
        
    def kill_self(self):
        logger.log("Server closed")
        my_database.close()
        exit(0)


def main(cmd_args):
    my_server = MyServer(host=cmd_args.server_ip, \
        port=cmd_args.server_port, mobile_mac=cmd_args.mobile_mac)
    try:
        my_server.run()
    except KeyboardInterrupt:
        my_server.kill_self()

#------------------------------ Main Function ---------------------------------

if __name__ == '__main__':
    from configargparse import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--server_ip", type=str, default="192.168.195.45", \
        help="Server IP address")
    parser.add_argument("--server_port", type=int, default=8000, \
        help="Server port")
    parser.add_argument("--mobile_mac", type=str, default="54:f2:94:0f:71:ba", \
        help="Mobile MAC address, which is the target to be localized")
    cmd_args = parser.parse_args()
    main(cmd_args)