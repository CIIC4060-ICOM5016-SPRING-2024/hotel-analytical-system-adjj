import configparser
import csv
import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()


class Database:
    def __init__(self):
        # self.credentials = self.connect_db()
        self.conexion = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT'),
        )

    # def connect_db(self):
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # credentials_path = os.path.join(current_dir, 'credentials.csv')

        # with open(credentials_path, 'r', newline='') as credencial:
        #     reader = csv.reader(credencial)
        #     next(reader)
        #     host, db, user, password, port = next(reader)
        #     db_dict = {'host':host, 'user':user, 'password':password, 'port':port, 'database':db}
        #     return db_dict

        # db_dict = {'host':os.getenv('HOST'), 'user':os.getenv('USER'), 'password':os.getenv('PASSWORD'), 'port':os.getenv('PORT'), 'database':os.getenv('DATABASE')
        # }
        # return db_dict

    def close(self):
        self.conexion.close()