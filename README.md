# Lab1: WiFi Localization

## Preparation

1. Install [MySQL](https://www.mysql.com/cn/), and [Python 3.7+](https://www.python.org/downloads/)
2. Create a database named `ComNet` [in MySQL](https://www.runoob.com/mysql/mysql-create-database.html)
3. Run `sh setup.sh`
4. Fill in `config.yml`

## Run

```bash
cd src
# data collection
python main.py
# data processing and visualization
python localizer.py
```


