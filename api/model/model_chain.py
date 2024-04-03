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
        try:
            query = """INSERT INTO chains (chid,cname,springmkup,summermkup,fallmkup,wintermkup) VALUES (%s,%s,%s,%s,%s,%s)"""
            cur.execute(query,(new_chain['chid'],new_chain['cname'],new_chain['springmkup'],new_chain['summermkup'],new_chain['fallmkup'],new_chain['wintermkup']))
            self.db.conexion.commit()
        except Exception as e:
            print(f"Error adding chain: {e}")
            self.db.conexion.rollback()  
            return False
        finally:
            self.db.close()
            cur.close()

        return True
    
    def deleteChain(self,id:int):
        cur = self.db.conexion.cursor()

        try: 
            query = "DELETE FROM chains WHERE chid = %s"
            cur.execute(query,(id,))
            self.db.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar chain: {e}")
            self.db.conexion.rollback()
            return False
        finally:
            cur.close()
            self.db.close()

    def putChain(self, id:int, updated_chain:dict):
        cur = self.db.conexion.cursor()

        try:
            query = """UPDATE chains SET cname=%s,springmkup=%s,summermkup=%s,fallmkup=%s,wintermkup=%s WHERE chid=%s"""
            cur.execute(query,(updated_chain['cname'],updated_chain['springmkup'],updated_chain['summermkup'],updated_chain['fallmkup'],updated_chain['wintermkup'],updated_chain['chid']))
            self.db.conexion.commit()
        except Exception as e:
            print(f"Error al actualizar chain: {e}")
            return False
        finally:
            cur.close()
            self.db.close()

        return True






            



