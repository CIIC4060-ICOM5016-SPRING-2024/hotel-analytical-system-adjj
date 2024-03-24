import configparser
import csv

import psycopg2

class Database:
    def __init__(self):
        self.credentials = self.connect_db()
        self.conexion = psycopg2.connect(
            host=self.credentials['host'],
            user=self.credentials['user'],
            password=self.credentials['password'],
            port=self.credentials['port'],
            database=self.credentials['database'],
        )

    def connect_db(self):
        with open("credentials.csv", 'r', newline='') as credencial:
            reader = csv.reader(credencial)
            next(reader)
            host, db, user, password, port = next(reader)
            db_dict = {'host':host, 'user':user, 'password':password, 'port':port, 'database':db}
            return db_dict

    def close(self):
        self.conexion.close()