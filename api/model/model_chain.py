from .db import Database


class ChainsDAO:
    def __init__(self):
        self.db = Database()

    def getAllChains(self):
        cur = self.db.conexion.cursor()
        query = "SELECT * FROM chains"
        cur.execute(query)
        chains_list = cur.fetchall()
        self.db.close()
        cur.close()

        return chains_list
    
    def getChain(self,id:int):
        cur = self.db.conexion.cursor()
        query = f"SELECT * FROM chains WHERE chid={id}"
        cur.execute(query)
        chains_list = cur.fetchall()
        self.db.close()
        cur.close()

        return chains_list


