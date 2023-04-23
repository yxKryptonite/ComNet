from utils import trilateration, smooth_avg
import pandas as pd
import yaml
from matplotlib import pyplot as plt
from matplotlib import patches

class BaseLocalizer():
    def __init__(self, database):
        self.database = database
        self.data = pd.DataFrame()
        
    def set_data_from_database(self):
        sql = f"SELECT * FROM {self.database.args['table']}"
        self.data = self.database.query(sql)
        self.data = pd.DataFrame(self.data, \
            columns=['ID', 'MMAC', 'TIME', 'MAC', 'RNG', 'RSSI'])
    
    def set_data_from_csv(self, path):
        # for debugging, headless csv file
        self.data = pd.read_csv(path, sep=',', header=None, \
            names=['ID', 'MMAC', 'TIME', 'MAC', 'RNG', 'RSSI'])
        
    def get_length(self):
        return len(self.data)
    
    def get_data(self):
        return self.data
    
    def check_pos(self, room_size, pos):
        x_min, x_max = 0, room_size[0]
        y_min, y_max = 0, room_size[1]
        if pos[0] < x_min or pos[0] > x_max or pos[1] < y_min or pos[1] > y_max:
            return False
        return True
    
    def localize(self):
        '''naive inplementation'''
        if len(self.data) == 0:
            print("No data to localize")
            return
        
        trajectory = []
        args = self.database.get_args()
        room_size = args['room_size']
        positions = [tuple(data) for data in args['coordinates']]
        mmacs = args['mmacs']
        
        placeholders = {mmacs[0]: None, mmacs[1]: None, mmacs[2]: None}
        for _, row in self.data.iterrows():
            placeholders[row['MMAC']] = row['RNG']
            if None in placeholders.values():
                continue
            else:
                pos = trilateration(positions[0], \
                        positions[1], positions[2], placeholders[mmacs[0]], \
                            placeholders[mmacs[1]], placeholders[mmacs[2]])
                
                if self.check_pos(room_size, pos):
                    trajectory.append(pos)
                    placeholders = {mmacs[0]: None, mmacs[1]: None, mmacs[2]: None}
                
        trajectory = smooth_avg(trajectory)
        return positions, trajectory, room_size
        
    def plot_trajectory(self):
        positions, trajectory, room_size = self.localize()
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.add_patch(patches.Rectangle((0, 0), room_size[0], room_size[1], color='blue', fill=False))
        plt.scatter([xy[0] for xy in positions], \
            [xy[1] for xy in positions], color='red')
        x = [xy[0] for xy in trajectory]
        y = [xy[1] for xy in trajectory]
        plt.plot(x, y, color='green')
        plt.show()


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
    
    my_localizer.set_data_from_csv('./0421-1.csv')
    my_localizer.plot_trajectory()