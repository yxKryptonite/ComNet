import http
import socketserver
from http import server
import json
import yaml
from logger import Logger
from database import MySQLDatabase
from configargparse import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mmac", type=str)
mmac = parser.parse_args().mmac

logger = Logger()
with open("../config.yml", 'r') as stream:
    try:
        args = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logger.echo(exc)
    
my_database = MySQLDatabase(args, logger)
my_database.connect()
my_database.create_table(inplace=True)

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        logger.echo(self.requestline)
        if self.path != '/hello':
            self.send_error(404, "Page not Found!")
            return
 
        response = {
            'Method': 'GET',
            'Status': 'Success',
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
        
        
    def do_POST(self):
        logger.echo(self.headers)
        logger.echo(self.command)
        req_datas = self.rfile.read(int(self.headers['content-length']))

        response = {
            'Method': 'POST',
            'Status': 'Success',
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
        
        received_data = req_datas.decode().split("=")[-1]
        print(received_data)
        json_data = json.loads(received_data)
        id = json_data['id']
        json_data = json_data['data']
        json_data['id'] = id

        my_database.filter_insert(json_data, mmac=mmac)
        

class MyServer(http.server.HTTPServer):
    def __init__(self, host='localhost', port=8000, HandlerClass=RequestHandler):
        super().__init__((host, port), HandlerClass)
        self.host = host
        self.port = port
        
    def run(self):
        logger.log(f"Server started at {self.host}:{self.port}")
        self.serve_forever()
        
    def kill_self(self):
        self.server_close()
        logger.log("Server closed")


def main():
    my_server = MyServer()
    try:
        my_server.run()
    except KeyboardInterrupt:
        my_server.kill_self()
        my_database.close()

#------------------------------ Main Function ---------------------------------

if __name__ == '__main__':
    main()