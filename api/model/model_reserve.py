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

    def postReservation(self, new_reservation: dict) -> bool:
        if not self.db.canPostInReserveTable(new_reservation['eid']):
            print(f"El empleado {new_reservation['eid']} no tiene acceso a crear una reserva.")
            return False

        guest_validity, message = self.db.validGuests(ruid=new_reservation['ruid'], guests=new_reservation['guests'])
        if not guest_validity:
            print(message)
            return False

        cur = self.db.conexion.cursor()
        reid = None
        try:
            # Obtener información necesaria para calcular el total_cost
            query = """
            SELECT R.rprice, RU.startdate, RU.enddate, C.springmkup, C.summermkup, C.fallmkup, C.wintermkup, CL.memberyear
            FROM roomunavailable RU
            JOIN room R ON RU.rid = R.rid
            JOIN hotel H ON R.hid = H.hid
            JOIN chains C ON H.chid = C.chid
            JOIN client CL ON CL.clid = %s
            WHERE RU.ruid = %s;
            """
            cur.execute(query, (new_reservation['clid'], new_reservation['ruid']))
            result = cur.fetchone()

            if result:
                rprice, startdate, enddate, springmkup, summermkup, fallmkup, wintermkup, memberyear = result
                # Calcular los días hospedados
                days_stayed = (enddate - startdate).days
                # Determinar el markup de temporada basado en el mes de startdate
                month = startdate.month
                if 3 <= month <= 5:
                    season_markup = springmkup
                elif 6 <= month <= 8:
                    season_markup = summermkup
                elif 9 <= month <= 11:
                    season_markup = fallmkup
                else:
                    season_markup = wintermkup
                # Calcular el descuento de membresía
                if 1 <= memberyear <= 4:
                    membership_discount = 0.98
                elif 5 <= memberyear <= 9:
                    membership_discount = 0.95
                elif 10 <= memberyear <= 14:
                    membership_discount = 0.92
                else:
                    membership_discount = 0.88
                # Calcular el total_cost
                total_cost = round(rprice * days_stayed * season_markup * membership_discount,2)

                # Insertar la nueva reserva con el total_cost calculado
                insert_query = "INSERT INTO reserve (ruid, clid, total_cost, payment, guests) VALUES (%s, %s, %s, %s, %s) RETURNING reid"
                cur.execute(insert_query, (
                new_reservation['ruid'], new_reservation['clid'], total_cost, new_reservation['payment'],
                new_reservation['guests']))
                self.db.conexion.commit()
                reid = cur.fetchone()[0]
            else:
                print("No se encontró la información necesaria para calcular el total_cost.")
        except Exception as e:
            print(f"Error al añadir la reserva: {e}")
            self.db.conexion.rollback()
        finally:
            cur.close()
            self.db.close()
            return reid

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

    def getTop3RoomsLeastCapacityRatio(self,eid,hid):
        if not self.db.canAccessLocalStats(eid=eid,hid=hid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas. (Found in Model)")
            return None
        cur = self.db.conexion.cursor()
        try:
            query="""
            SELECT 
                R.rid,
                RD.rname,
                ROUND(AVG(Res.guests::decimal / RD.capacity) * 100, 2) AS avg_guest_to_capacity_ratio
            FROM 
                Reserve Res
            INNER JOIN RoomUnavailable RU ON Res.ruid = RU.ruid
            INNER JOIN Room R ON RU.rid = R.rid
            INNER JOIN RoomDescription RD ON R.rdid = RD.rdid
            GROUP BY 
                R.rid, RD.rname
            ORDER BY 
                avg_guest_to_capacity_ratio ASC
            LIMIT 3;

            """
            cur.execute(query)
            result=cur.fetchall()
            return result
        except Exception as e:
            print(f"Error al obtener estadística {e}")
            return None
        finally:
            self.db.conexion.close()
            cur.close()

