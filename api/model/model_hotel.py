from .db import Database
class HotelDAO:
    def __init__(self):
        self.db = Database()

    def getAllHotels(self):
        cur = self.db.conexion.cursor()
        query = "SELECT hid, chid, hname, hcity  FROM hotel"
        cur.execute(query)
        hotel_list = cur.fetchall()
        self.db.close()
        cur.close()

        return hotel_list

    def getHotelById(self, hid):
        cur = self.db.conexion.cursor()
        try:
            query = "SELECT hid, chid, hname, hcity FROM hotel WHERE hid = %s"
            cur.execute(query, (hid,))
            hotel = cur.fetchone()
            return hotel
        except Exception as e:
            print(f"Error al obtener el hotel con ID {hid}: {e}")
            self.db.conexion.rollback()
            return None
        finally:
            self.db.close()
            cur.close()

    def postHotel(self, chid, hname, hcity):
        # Asegurarse de que la posición sea válida
        # if not (employee_inputs_are_correct(position, salary)):
        #     return False

        cur = self.db.conexion.cursor()  # Asumiendo que esto abre el cursor correctamente.
        try:
            query = """
                    INSERT INTO hotel (chid, hname, hcity) 
                    VALUES (%s, %s, %s)
                    """
            cur.execute(query, (chid, hname, hcity))
            self.db.conexion.commit()
        except Exception as e:
            print(f"Error al insertar hotel: {e}")
            self.db.conexion.rollback()  # Opcional: deshacer cambios en caso de error.
            return False, f"Error al agregar hotel: {e}"
        finally:
            self.db.close()
            cur.close()
        return True, f"hotel agregado exitosamente"


    def deleteHotel(self, hid):
        cur = self.db.conexion.cursor()
        try:
            query = "DELETE FROM hotel WHERE hid = %s"
            cur.execute(query, (hid,))
            self.db.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar hotel: {e}")
            self.db.conexion.rollback()
            return False
        finally:
            cur.close()
            self.db.close()


    def putHotel(self, hid, chid, chname, hcity):

        # if not (employee_inputs_are_correct(position, salary)):
        #     return False

        cur = self.db.conexion.cursor()
        try:
            # Construye la consulta SQL de actualización
            query = """
                    UPDATE hotel
                    SET chid = %s, hname = %s, hcity = %s
                    WHERE hid = %s
                    """
            # Ejecuta la consulta con los valores proporcionados
            cur.execute(query, (chid, chname, hcity, hid))
            # Si no se actualizó ningún registro, podría significar que el hid no existe
            if cur.rowcount == 0:
                self.db.conexion.rollback()  # Opcional: revertir en caso de no encontrar el hotel
                return False
            # Si se actualizó el registro, hacer commit de los cambios
            self.db.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar hotel: {e}")
            self.db.conexion.rollback()
            return False
        finally:
            cur.close()
            self.db.close()

    def get_most_reservations(self, eid):

        if not self.db.canAccessGlobalStats(eid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas globales.")
            return None

        cur = self.db.conexion.cursor()
        """
        Para saber en que hotel pertenece un reserve, hay que unir roomUnavailable y room, ya que room contiene el hid.
        Despues a eso se le hace un Select del hid, hname y el count de las reservaciones agrupado por los hid.
        Eso devuelve una tabla con las reservaciones hechas por cada hotel. Esa tabla se utiliza en la proxima consulta.
        
        La consulta RankedHotels utiliza NTILE para dividir la consulta ReservationCounts en 10 grupos en oprden desendiente.
        A cada elemento de cada grupo le da un identificador para saber a que grupo pertenece.
        
        La ultima consulta utiliza ese identificador para extraer los elementos del primero grupo (los que mas reservaciones tienen)
        de forma desendiente. 
        """
        query = """ WITH ReservationCounts AS (
                    SELECT
                        h.hid,
                        h.hname,
                        COUNT(re.reid) AS reservation_count
                    FROM
                        Hotel h
                        JOIN Room r ON h.hid = r.hid
                        JOIN RoomUnavailable ru ON r.rid = ru.rid
                        JOIN Reserve re ON ru.ruid = re.ruid
                    GROUP BY 
                        h.hid
                ),
                RankedHotels AS (
                    SELECT
                        *,
                        NTILE(10) OVER (ORDER BY reservation_count DESC) AS decile
                    FROM
                        ReservationCounts
                )
                SELECT
                    hid,
                    hname,
                    reservation_count
                FROM
                    RankedHotels
                WHERE
                    decile = 1
                ORDER BY
                    reservation_count DESC;
                """
        cur.execute(query)
        hotel_list = cur.fetchall()
        self.db.close()
        cur.close()

        return hotel_list

    def get_most_capacity(self, eid):

        if not self.db.canAccessGlobalStats(eid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas globales.")
            return None

        cur = self.db.conexion.cursor()
        query = """ SELECT
                        h.hid,
                        h.hname,
                        SUM(rd.capacity) AS total_capacity
                    FROM
                        Hotel h
                    JOIN Room r ON h.hid = r.hid
                    JOIN RoomDescription rd ON r.rdid = rd.rdid
                    GROUP BY 
                        h.hid
                    ORDER BY 
                        total_capacity DESC
                    LIMIT 5;

                """
        cur.execute(query)
        hotel_list = cur.fetchall()
        self.db.close()
        cur.close()

        return hotel_list
    
    def get_total_reservation_by_room_type(self ,hid, eid):
        if not self.db.canAccessLocalStats(eid, hid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas del hotel {hid}.")
            return None
        cur = self.db.conexion.cursor()
        query="""
        SELECT 
            RD.rtype, 
            COUNT(R.reid) AS total_reservations
        FROM 
            Reserve R
        INNER JOIN RoomUnavailable RU ON R.ruid = RU.ruid
        INNER JOIN Room Ro ON RU.rid = Ro.rid
        INNER JOIN RoomDescription RD ON Ro.rdid = RD.rdid
        GROUP BY 
            RD.rtype
        ORDER BY 
            total_reservations DESC;"""
        cur.execute(query)
        total_reservations = cur.fetchall()
        self.db.close()
        cur.close()

        return total_reservations



    
