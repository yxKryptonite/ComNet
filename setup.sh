pip install -r requirements.txt
touch config.yml
echo "# Path: config.yml
# This is the configuration file for the project.
# It is used to store the password and other sensitive information.
# It is not tracked by git, so you can safely edit it.

# The following is the database information.
host: localhost
user: root
passwd: 
db: ComNet
table: WIFI

# The following is your server IP, server port and the MAC of your mobile phone to be localized.
server_ip: 
server_port: 
mobile_mac: 

# The following is the mMACs of the 3 WIFI detector.
mmacs: 
  - 
  - 
  - 

# The following is the coordinates of the 3 WIFI detector (corresponding to the mMACs above)
coordinates: 
  - 
  - 
  - 

# The following is the room size in xy (in meters). e.g [10, 10]
room_size: []


# The following is the size and location of obstacles in xy (in meters). e.g [1, 2, 3, 4] means [1, 2] * [3, 4]
obstacle: []" > config.yml