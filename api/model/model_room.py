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
            try:
                hid = int(hid)
                rdid = int(rdid)
                rprice = float(rprice)
                query = "INSERT INTO room (hid, rdid, rprice) VALUES (%s, %s, %s)"
                cur.execute(query, (hid, rdid, rprice))
                self.db.conexion.commit()
                return True, f"Habitacion agregada exitosamente"
            except Exception as e:
                print(f"Error al insertar habitación: {e}")
                self.db.conexion.rollback()
                return False, "Error al agregar habitacion"
            finally:
                cur.close()


    def deleteRoom(self,rid):
        with self.db.conexion.cursor() as cur:
            try:
                query = "DELETE FROM room WHERE rid = %s"
                cur.execute(query, (rid,))
                self.db.conexion.commit()
                return True, f"Habitacion eliminada exitosamente"
            except Exception as e:
                print(f"Error al eliminar habitacion: {e}")
                self.db.conexion.rollback()
                return False, "Error al eliminar habitacion"

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