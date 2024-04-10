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
    def list_tables(self):
        cur = self.conexion.cursor()
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        cur.execute(query)
        list = [table[0] for table in cur.fetchall()]
        return list

    def canAccessLocalStats(self, eid, hid):
        cur = self.conexion.cursor()
        # Obtener la posición del empleado y el hotel/cadena donde trabaja
        cur.execute("SELECT position, hid FROM employee WHERE eid = %s", (eid,))
        employee = cur.fetchone()
        if employee is None:
            return False  # El empleado no existe

        position, employee_hid = employee

        if position == 'Regular':
            return employee_hid == hid
        elif position == 'Supervisor':
            # Asumiendo que existe una relación de hotel a cadena que podemos consultar
            cur.execute("SELECT chid FROM hotel WHERE hid = %s", (hid,))
            hotel_chain_id = cur.fetchone()[0]
            cur.execute("SELECT chid FROM hotel WHERE hid = %s", (employee_hid,))
            employee_chain_id = cur.fetchone()[0]
            return hotel_chain_id == employee_chain_id
        elif position == 'Administrator':
            return True
        else:
            return False

    def canAccessGlobalStats(self, eid):
        cur = self.conexion.cursor()
        query = "SELECT position, eid  FROM employee WHERE position = 'Administrator' AND eid = %s"
        cur.execute(query, (eid,))
        employee = cur.fetchone()

        if employee is None:
            return False
        else:
            return True

    def canPostUnavailableRoom(self, eid):
        cur = self.conexion.cursor()
        query = "SELECT position, eid  FROM employee WHERE position = 'Supervisor' AND eid = %s"
        cur.execute(query, (eid,))
        employee = cur.fetchone()

        if employee is None:
            return False
        else:
            return True


    def canPostInReserveTable(self, eid):
        cur = self.conexion.cursor()
        query = "SELECT position, hid FROM employee WHERE position = 'Regular' AND eid = %s"
        cur.execute(query, (eid,))
        employee = cur.fetchone()

        if employee is None:
            return False
        else:
            return True
    
    def validGuests(self,reid):
        cur = self.conexion.cursor()
        query = """
            SELECT Res.guests, RD.capacity
            FROM Reserve Res
            INNER JOIN RoomUnavailable RU ON Res.ruid = RU.ruid
            INNER JOIN Room R ON RU.rid = R.rid
            INNER JOIN RoomDescription RD ON R.rdid = RD.rdid
            WHERE Res.reid = %s;
        """
        cur.execute(query=query,vars=(reid,))
        result = cur.fetchone()

        if result:
            guests, capacity = result
            # Check if the number of guests does not exceed the room's capacity
            if guests <= capacity:
                return True, "Reservation is valid."
            else:
                return False, f"Reservation exceeds room capacity. Guests: {guests}, Capacity: {capacity}"
        else:
            return False, "Reservation not found."


    def close(self):
        self.conexion.close()