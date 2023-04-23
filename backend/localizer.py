from utils import trilateration, smooth_avg
import pandas as pd
import yaml
from matplotlib import pyplot as plt

class BaseLocalizer():
    def __init__(self, database):
        self.database = database
        self.data = pd.DataFrame()
        
    def get_data_from_database(self):
        sql = f"SELECT * FROM {self.database.args['table']}"
        self.data = self.database.query(sql)
        self.data = pd.DataFrame(self.data, \
            columns=['ID', 'MMAC', 'TIME', 'MAC', 'RNG', 'RSSI'])
    
    def get_data_from_csv(self, path):
        # for debugging, headless csv file
        self.data = pd.read_csv(path, sep=',', header=None, \
            name=['ID', 'MMAC', 'TIME', 'MAC', 'RNG', 'RSSI'])
        
    def get_length(self):
        return len(self.data)
    

class RealTimeLocalizer(BaseLocalizer):
    def __init__(self, args) -> None:
        super.__init__(self, None) # real-time localization does not need database
        self.args = args
        self.buffers = {self.args['mmacs'][0]: pd.DataFrame(), \
            self.args['mmacs'][1]: pd.DataFrame(), self.args['mmacs'][2]: pd.DataFrame()}
        
    def clear_buffer(self):
        self.buffers = {self.args['mmacs'][0]: pd.DataFrame(), \
            self.args['mmacs'][1]: pd.DataFrame(), self.args['mmacs'][2]: pd.DataFrame()}
    
    def get_buffer(self):
        return self.buffers
    
    def add_to_buffer(self, mmac, data):
        self.buffers[mmac] = self.buffers[mmac].append(data)


# test
if __name__ == "__main__":
    from database import MySQLDatabase
    with open("../config.yml", 'r') as stream:
        try:
            args = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    my_database = MySQLDatabase(args)
    my_localizer = BaseLocalizer(my_database)