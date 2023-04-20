import http
from http import server
import json
import yaml
from logger import Logger
from database import MySQLDatabase

logger = Logger()
with open("../config.yml", 'r') as stream:
    try:
         args = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
         logger.echo(exc)
    
database = MySQLDatabase(args, logger)

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.requestline)
        if self.path != '/hello':
            self.send_error(404, "Page not Found!")
            return
 
        data = {
            'result_code': '1',
            'result_desc': 'Success',
            'timestamp': '',
            'data': {'message_id': '25d55ad283aa400af464c76d713c07ad'}
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        
        
    def do_POST(self):
        req_datas = self.rfile.read(int(self.headers['content-length']))

        data = {
            'result_code': '2',
            'result_desc': 'Success',
            'timestamp': '',
            'data': {'message_id': '25d55ad283aa400af464c76d713c07ad'}
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        
        received_data = req_datas.decode()
        json_data = json.loads(received_data)
        
        # TODO: add database here
        database.insert(json_data)
        

class SimpleServer(http.server.HTTPServer):
    def __init__(self, host='localhost', port=8000, HandlerClass=RequestHandler):
        super().__init__((host, port), HandlerClass)
        self.host = host
        self.port = port
        
    def run(self):
        self.serve_forever()


def main():
    my_server = SimpleServer()
    my_server.run()

#----------------------------------------------------------------------

if __name__ == '__main__':
    main()