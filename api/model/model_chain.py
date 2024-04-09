
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
        chains_list = cur.fetchone()
        self.db.close()
        cur.close()

        return chains_list
    
    def postChain(self, new_chain:dict):
        cur = self.db.conexion.cursor()
        try:
            query = """INSERT INTO chains (cname,springmkup,summermkup,fallmkup,wintermkup) VALUES (%s,%s,%s,%s,%s)"""
            cur.execute(query,(new_chain['cname'],new_chain['springmkup'],new_chain['summermkup'],new_chain['fallmkup'],new_chain['wintermkup']))
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
            cur.execute(query,(updated_chain['cname'],updated_chain['springmkup'],updated_chain['summermkup'],updated_chain['fallmkup'],updated_chain['wintermkup'],id))
            self.db.conexion.commit()
        except Exception as e:
            print(f"Error al actualizar chain: {e}")
            return False
        finally:
            cur.close()
            self.db.close()

        return True

    def get_top_3_chains_with_least_rooms(self, eid):
        if not self.db.canAccessGlobalStats(eid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas globales.")
            return None

        cur = self.db.conexion.cursor()

        try:
            query = """
                    SELECT
                        C.chid AS Chain_ID,
                        C.cname AS Chain_Name,
                        COUNT(RO.rid) AS Room_Count
                    FROM
                        Chains C
                        LEFT JOIN Hotel H ON C.chid = H.chid
                        LEFT JOIN Room RO ON H.hid = RO.hid
                    GROUP BY
                        C.chid, C.cname
                    ORDER BY
                        Room_Count ASC
                    LIMIT 3;
                    """
            cur.execute(query)
            chains_list = cur.fetchall()
            return chains_list

        except Exception as e:
            print(f"Error al los tres meses con mayor reservación por cadena {e}")
            return None
        finally:
            self.db.conexion.close()
            cur.close()




    def get_top_3_chains_with_highest_revenue(self,eid):

        if not self.db.canAccessGlobalStats(eid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas globales.")
            return None


        cur = self.db.conexion.cursor()
        try:

            query = """
                    SELECT
                        C.chid AS Chain_ID,
                        C.cname AS Chain_Name,
                        SUM(R.total_cost) AS Total_Revenue
                    FROM
                        Chains C
                        INNER JOIN Hotel H ON C.chid = H.chid
                        INNER JOIN Room RO ON H.hid = RO.hid
                        INNER JOIN RoomUnavailable RU ON RO.rid = RU.rid
                        INNER JOIN Reserve R ON RU.ruid = R.ruid
                    GROUP BY
                        C.chid, C.cname
                    ORDER BY
                        Total_Revenue DESC
                    LIMIT 3;
                    """
            cur.execute(query)
            chains_list = cur.fetchall()
            return chains_list

        except Exception as e:
            print(f"Error al los tres meses con mayor reservación por cadena {e}")
            return None

        finally:
            self.db.conexion.close()
            cur.close()







            



