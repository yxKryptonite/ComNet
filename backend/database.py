import pymysql as mysql
import yaml
import datetime

class Logger():
    def __init__(self):
        pass 
    
    def echo(self, msg):
        print(msg)
        
    def log(self, msg):
        print(f"{datetime.datetime.now()} - {msg}")


def main(args, logger):
    db = mysql.connect(host=args['host'], user=args['user'], passwd=args['passwd'], db=args['db'])
    logger.log(f"Connected to database {args['db']}")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS WIFI")
    
    sql = """CREATE TABLE WIFI (
             ID VARCHAR(100) NOT NULL,
             MMAC VARCHAR(100) NOT NULL,
             RATE INT,  
             TIME DATETIME,
             LAT FLOAT,
             LON FLOAT,
             MAC VARCHAR(100),
             RSSI FLOAT,
             RNG FLOAT,
             RSSI1 FLOAT,
             RSSI2 FLOAT,
             RSSI3 FLOAT,
             RSSI4 FLOAT,
             RSSI5 FLOAT )""" # RNG is for RANGE (RANGE is a reserved word)
         
    cursor.execute(sql)
    logger.log("Table created")
    
    db.close()
    
    
if __name__ == "__main__":
    logger = Logger()
    with open("./config.yml", 'r') as stream:
        try:
            args = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.echo(exc)
    
    main(args, logger)