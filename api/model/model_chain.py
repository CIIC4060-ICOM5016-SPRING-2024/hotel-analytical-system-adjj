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
    
    def postChain(self, new_chain:dict):
        cur = self.db.conexion.cursor()
        post_query = f"INSERT INTO chains (chid,cname,springmkup,summermkup,fallmkup,wintermkup) VALUES ({new_chain['chid'],new_chain['cname'],new_chain['springmkup'],new_chain['summermkup'],new_chain['fallmkup'],new_chain['wintermkup']})"
        cur.execute(post_query)
        new_chain_query = f"SELECT * FROM chains WHERE chid={new_chain['chid']}"
        cur.execute(new_chain_query)
        chains_list = cur.fetchall()
        self.db.close()
        cur.close()

        return chains_list



