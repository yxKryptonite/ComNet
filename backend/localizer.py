from utils import trilateration, smooth_avg
import pandas as pd

class Localizer():
    def __init__(self) -> None:
        self.buffer = pd.DataFrame()
    
    def read_from_csv(self, path):
        pass
        
        
    def clear_buffer(self):
        self.buffer = pd.DataFrame()
    
    def get_buffer(self):
        return self.buffer
    
    def add_to_buffer(self, data):
        self.buffer = self.buffer.append(data, ignore_index=True)
        
    def get_location(self, data):
        pass
