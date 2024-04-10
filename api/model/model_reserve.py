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
            print(f"El empleado {new_reservation['eid']} no tiene acceso a crear un reserve.")
            return None


        guest_validity,message = self.db.validGuests(reid=new_reservation['reid'])
        if guest_validity == False:
            print(message)
            return False
        
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
        guest_validity,message = self.db.validGuests(reid=updated_reservation['reid'])
        if guest_validity == False:
            print(message)
            return False
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

    def getReserveByPayMethod(self, eid):
        if not self.db.canAccessGlobalStats(eid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas.")
            return None
        cur = self.db.conexion.cursor()
        try:
            query = """
                    SELECT payment,
                    COUNT (*) as num_payment_method,
                    (COUNT(*) * 100.0) / SUM(COUNT(*)) OVER() AS reservation_percentage
                    FROM reserve
                    GROUP BY payment
                    ORDER BY reservation_percentage
                    """
            cur.execute(query)
            payments_list = cur.fetchall()
            return payments_list
        except Exception as e:
            print(f"Error al obtener el porcentaje de metodos de pagos utilizados por reservaciones en total {e}")
            return None
        finally:
            self.db.conexion.close()
            cur.close()

    def getTop3RoomsLeastCapacityRatio(self,eid):
        if not self.db.canAccessGlobalStats(eid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas.")
            return None
        cur = self.db.conexion.cursor()
        try:
            query="""
                SELECT 
                    R.rid,
                    RD.rname,
                    ROUND(AVG(Res.guests::decimal / RD.capacity) * 100, 2) AS avg_guest_to_capacity_ratio
                FROM 
                    Room R
                JOIN RoomDescription RD ON R.rdid = RD.rdid
                JOIN Reserve Res ON R.rid = Res.rid
                GROUP BY 
                    R.rid, RD.rname
                ORDER BY 
                    avg_guest_to_capacity_ratio ASC
                LIMIT 3;
            """
            cur.execute(query)
            result=cur.fetchall
            return result
        except Exception as e:
            print(f"Error al obtener estadística {e}")
            return None
        finally:
            self.db.conexion.close()
            cur.close()

