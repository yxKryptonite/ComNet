from server import MyServer
import yaml
from database import MySQLDatabase

def main():
    with open("../config.yml", 'r') as stream:
        try:
            args = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
        
    my_database = MySQLDatabase(args)
    my_database.connect()
    my_database.create_table(inplace=False)
    
    my_server = MyServer(host=args['server_ip'], port=args['server_port'], \
        mobile_mac=args['mobile_mac'], database=my_database)
    try:
        my_server.run()
    except KeyboardInterrupt:
        my_server.kill_self()
        
        
if __name__ == "__main__":
    main()
    
    