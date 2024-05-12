
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
        chid = None
        message = "Chain added successfully"
        status = "success"
        try:
            query = """INSERT INTO chains (cname,springmkup,summermkup,fallmkup,wintermkup) VALUES (%s,%s,%s,%s,%s) RETURNING chid;"""
            cur.execute(query,(new_chain['cname'],new_chain['springmkup'],new_chain['summermkup'],new_chain['fallmkup'],new_chain['wintermkup']))
            self.db.conexion.commit()
            chid = cur.fetchone()[0]
        except Exception as e:
            #print(f"Error adding chain: {e}")
            message = str(e)
            status = "error"
            self.db.conexion.rollback()
        finally:
            self.db.close()
            cur.close()
            return chid, message, status

    
    def deleteChain(self,id:int):
        cur = self.db.conexion.cursor()
        message = "Chain removed successfully"
        success = True
        try: 
            query = "DELETE FROM chains WHERE chid = %s"
            cur.execute(query,(id,))
            self.db.conexion.commit()
        except Exception as e:
            #print(f"Error al eliminar chain: {e}")
            message = str(e)
            success = False
            self.db.conexion.rollback()
        finally:
            cur.close()
            self.db.close()
            return success, message

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

    def getTop3ProfitMonthsByChain(self, eid):
        if not self.db.canAccessGlobalStats(eid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas.")
            return None
        cur = self.db.conexion.cursor()
        try:
            query = """
                    WITH RankedReservations AS (
                        SELECT
                            c.chid AS Chain_ID,
                            EXTRACT(MONTH FROM ru.startdate) AS Reservation_Month,
                            COUNT(r.reid) AS Total_Reservations,
                            ROW_NUMBER() OVER (PARTITION BY c.chid ORDER BY COUNT(r.reid) DESC) AS Rank
                        FROM
                            Chains c
                            JOIN Hotel h ON c.chid = h.chid
                            JOIN Room ro ON h.hid = ro.hid
                            JOIN RoomUnavailable ru ON ro.rid = ru.rid
                            JOIN Reserve r ON ru.ruid = r.ruid
                        GROUP BY
                            c.chid,
                            EXTRACT(MONTH FROM ru.startdate)
                    )
                    SELECT
                        Chain_ID,
                        Reservation_Month,
                        Total_Reservations
                    FROM
                        RankedReservations
                    WHERE
                        Rank <= 3
                    ORDER BY
                        Chain_ID, Rank;

                        """
            cur.execute(query)
            most_profit_list = cur.fetchall()
            return most_profit_list
        except Exception as e:
            print(f"Error al los tres meses con mayor reservación por cadena {e}")
            return None
        finally:
            self.db.conexion.close()
            cur.close()

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
                    WHERE
                        C.chid <> -1
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




