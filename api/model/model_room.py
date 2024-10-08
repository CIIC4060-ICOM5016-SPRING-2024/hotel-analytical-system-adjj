from .db import Database
class RoomDAO:

    def __init__(self):
        self.db = Database()

    def getAllRooms(self):
        cur = self.db.conexion.cursor()
        query = "SELECT rid, hid, rdid, rprice  FROM room"
        cur.execute(query)
        room_list = cur.fetchall()
        self.db.close()
        cur.close()
        return room_list

    def getRoomById(self, rid):
        cur = self.db.conexion.cursor()
        query = "SELECT rid, hid, rdid, rprice FROM room WHERE rid = %s"
        cur.execute(query, (rid,))
        room = cur.fetchone()
        self.db.close()
        cur.close()
        return room

    def postRoom(self, hid, rdid, rprice):
        with self.db.conexion.cursor() as cur:
            rid = None
            message = "Room added successfully"
            status = "success"
            try:
                hid = int(hid)
                rdid = int(rdid)
                rprice = float(rprice)
                query = "INSERT INTO room (hid, rdid, rprice) VALUES (%s, %s, %s) RETURNING rid"
                cur.execute(query, (hid, rdid, rprice))
                self.db.conexion.commit()
                rid = cur.fetchone()[0]
            except Exception as e:
                #print(f"Error al insertar habitación: {e}")
                self.db.conexion.rollback()
                message = str(e)
                status = "error"
            finally:
                cur.close()
                return rid,message,status


    def deleteRoom(self,rid):
        with self.db.conexion.cursor() as cur:
            try:
                query = "DELETE FROM room WHERE rid = %s"
                cur.execute(query, (rid,))
                self.db.conexion.commit()
                return True, f"Room successfully deleted"
            except Exception as e:
                #print(f"Error when deleting room: {e}")
                self.db.conexion.rollback()
                return False, "Error when deleting room"

    def putRoom(self, rid, hid, rdid, rprice):
        with self.db.conexion.cursor() as cur:
            try:
                # Verifica si la habitación con el ID dado existe antes de actualizar
                cur.execute("SELECT COUNT(*) FROM room WHERE rid = %s", (rid,))
                room_count = cur.fetchone()[0]
                if room_count == 0:
                    return False, "La habitación no existe"

                # Actualiza la habitación
                query = "UPDATE room SET hid = %s, rdid = %s, rprice = %s WHERE rid = %s"
                cur.execute(query, (hid, rdid, rprice, rid))

                # Verifica si se actualizó alguna fila
                if cur.rowcount == 0:
                    self.db.conexion.rollback()
                    return False, "No se pudo actualizar la habitación"

                # Confirma la transacción
                self.db.conexion.commit()
                return True, "Habitacion actualizada exitosamente"
            except Exception as e:
                print(f"Error al actualizar habitacion: {e}")
                self.db.conexion.rollback()
                return False, f"Error al actualizar habitación: {e}"
            finally:
                cur.close()

    def get_top_5_handicap_reserved(self, hid, eid):
        if not self.db.canAccessLocalStats(eid, hid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas del hotel {hid}.")
            return None
        cur = self.db.conexion.cursor()
        try:
            query = """
                    SELECT
                        RO.rid AS Room_ID,
                        RD.rname AS Room_Name,
                        RD.rtype AS Room_Type,
                        COUNT(R.reid) AS Reservation_Count
                    FROM
                        Reserve R
                        INNER JOIN RoomUnavailable RU ON R.ruid = RU.ruid
                        INNER JOIN Room RO ON RU.rid = RO.rid
                        INNER JOIN RoomDescription RD ON RO.rdid = RD.rdid
                    WHERE
                        RD.ishandicap = TRUE AND RO.hid = %s  -- Add the hotel ID filter here
                    GROUP BY
                        RO.rid, RD.rname, RD.rtype
                    ORDER BY
                        Reservation_Count DESC
                    LIMIT 5;

                    """
            cur.execute(query, (hid,))
            handicaproomsreserved_list = cur.fetchall()
            return handicaproomsreserved_list
        except Exception as e:
            print(f"Error al obtener las top 5 habitaciones handicap mas reservadas del hotel con id {hid} {e}")
            return None
        finally:
            self.db.conexion.close()
            cur.close()



