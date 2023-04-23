import json
from database import MySQLDatabase
import socket  

class MyServer():
    def __init__(self, host, port, mobile_mac, database):
        self.host = host
        self.port = port
        self.mobile_mac = mobile_mac.lower()
        self.database = database
        
    def run(self):
        self.database.log(f"Server started at {self.host}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            
            while True:
                try:
                    conn, addr = s.accept()
                    with conn:
                        self.database.log(f'Connected by {addr}')
                        data = b''
                        while True:
                            chunk = conn.recv(1024)
                            if not chunk:
                                break
                            data += chunk
                            
                        req_datas = data.decode('utf-8').split("=")[-1]
                        json_data = json.loads(req_datas)
                        self.database.insert(json_data, mac=self.mobile_mac)
                        
                except Exception as e:
                    if e != KeyboardInterrupt:
                        self.database.log(e)
                    continue
                    
        
    def kill_self(self):
        self.database.log("Server closed")
        self.database.close()
        exit(0)

