from .db import Database
class ClientDAO:
    def __init__(self):
        self.db = Database()

    def getAllClients(self):
        cur = self.db.conexion.cursor()
        query = "SELECT clid, fname, lname, age, memberyear  FROM client"
        cur.execute(query)
        client_list = cur.fetchall()
        self.db.close()
        cur.close()

        return client_list
