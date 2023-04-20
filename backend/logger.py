import datetime

class Logger():
    def __init__(self):
        pass 
    
    def echo(self, msg):
        print(msg)
        
    def log(self, msg):
        print(f"{datetime.datetime.now()} - {msg}")