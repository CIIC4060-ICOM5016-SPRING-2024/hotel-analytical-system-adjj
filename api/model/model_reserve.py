from .db import Database

class ReserveDAO:
    def __init__(self) -> None:
        self.db = Database()
    def getAllReservations(self) -> list:
        cur = self.db.conexion.cursor()
        query="SELECT * FROM reserve"
        cur.execute(query=query)
        reservations_list = cur.fetchall()
        self.db.close()
        cur.close()
        return reservations_list
    def getReservation(self,id:int) -> list:
        cur = self.db.conexion.cursor()
        query=f"SELECT * FROM reserve WHERE reid={id}"
        cur.execute(query=query)
        reservation=cur.fetchone()
        self.db.close()
        cur.close()
        return reservation
    def postReservation(self,new_reservation:dict) -> bool:

        if not self.db.canPostInReserveTable(new_reservation['eid']):
            print(f"El empleado {new_reservation['eid']} no tiene acceso a las estadísticas globales.")
            return None

        cur = self.db.conexion.cursor()
        try:
            query="INSERT into reserve(ruid,clid,total_cost,payment,guests) VALUES(%s,%s,%s,%s,%s)"
            cur.execute(query=query,vars=(new_reservation['ruid'],new_reservation['clid'],new_reservation['total_cost'],new_reservation['payment'],new_reservation['guests']))
            self.db.conexion.commit()
        except Exception as e:
            print(f"Error adding reservation: {e}")
            self.db.conexion.rollback()
            return False
        finally:
            self.db.close()
            cur.close()
        return True
    def putReservation(self,id:int,updated_reservation:dict) -> bool:
        cur = self.db.conexion.cursor()
        try:
            query = "UPDATE reserve SET ruid=%s,clid=%s,total_cost=%s,payment=%s,guests=%s WHERE reid=%s"
            cur.execute(query=query,vars=(updated_reservation['ruid'],updated_reservation['clid'],updated_reservation['total_cost'],updated_reservation['payment'],updated_reservation['guests'],id))
            self.db.conexion.commit()
        except Exception as e:
            print(f"Error updating chain: {e}")
            self.db.conexion.rollback()  
            return False
        finally:
            self.db.close()
            cur.close()
        return True
    def deleteReservation(self,id:int) ->bool:
        cur = self.db.conexion.cursor()
        try:
            query = "DELETE FROM reserve WHERE reid=%s"
            cur.execute(query=query,vars=(id,))
            self.db.conexion.commit()
        except Exception as e:
            print(f"Error deleting chain: {e}")
            self.db.conexion.rollback()  
            return False
        finally:
            self.db.close()
            cur.close()
        return True