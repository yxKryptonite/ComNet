pip install -r requirements.txt
touch config.yml
echo "# Path: config.yml
# This is the configuration file for the project.
# It is used to store the password and other sensitive information.
# It is not tracked by git, so you can safely edit it.

host: localhost
user: root
passwd: 
db: ComNet
table: WIFI
" > config.yml