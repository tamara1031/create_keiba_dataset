import yaml
import mysql.connector

class Connection(object):
    def __init__(self, config_key, config_path = "./config/database.yml"):
        with open(config_path, 'r') as yml:
            config = yaml.safe_load(yml)

        self.conn = mysql.connector.connect(
            user=config[config_key]["username"],
            password=config[config_key]["password"],
            host=config[config_key]["host"],
            port=config[config_key]["port"],
            database=config[config_key]["database"]
        )

        # DBの接続確認
        if not self.conn.is_connected():
            raise Exception("failed to connect mysql server")

    def execute(self, sql, *params) -> dict: 
        cur = self.conn.cursor(dictionary=True)
        cur.execute(sql, params)

        return cur.fetchall()

    def commit(self):
        self.conn.commit()

        