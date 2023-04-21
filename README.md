# Lab1: WiFi Localization

## Preparation

1. Install [MySQL](https://www.mysql.com/cn/), [Node.js 12.22.0+](https://nodejs.org/en/) and [Python 3.7+](https://www.python.org/downloads/)
2. Create a database named `ComNet` [in MySQL](https://www.runoob.com/mysql/mysql-create-database.html)
3. Run `sh setup.sh`
4. Fill in `config.yml`

## Backend

```bash
cd backend
python server.py --server_ip <your_server_ip> \
                 --server_port <your_server_port> \
                 --mobile_mac <your_mobile_mac>
```

## Frontend

```bash
cd frontend
pc run
```

