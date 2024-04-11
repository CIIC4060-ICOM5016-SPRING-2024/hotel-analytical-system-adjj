from .db import Database
from datetime import datetime

class RoomUnavailableDAO():
    def __init__(self):
        self.db = Database()

    def getAllRoomsUnavailable(self):
        cur = self.db.conexion.cursor()
        query = "SELECT * FROM roomunavailable"
        cur.execute(query)
        roomunavailable = cur.fetchall()
        self.db.close()
        cur.close()
        return roomunavailable


    def getRoomUnavailableById(self, ruid):
        cur = self.db.conexion.cursor()
        try:
            query = "SELECT * FROM roomunavailable WHERE ruid = %s"
            cur.execute(query, (ruid,))
            roomunavailable = cur.fetchone()
            return roomunavailable
        except Exception as e:
            print(f'La habitacion indisponible con el id {ruid} no se encuentra')
            return False, "La habitacion indisponible no se encuentra'"
        finally:
            cur.close()

    def postRoomUnavailable(self, eid, rid, startdate, enddate):
        ruid = None
        message = "Room unavailable added successfully"
        status = "success"
        if not self.db.canPostUnavailableRoom(eid):
            #print(f"El empleado {eid} no tiene autorización para añadir una habitación indisponible.")
            message = f"Employee {eid} does not have authorization to add an unavailable room."
            status = "unauthorized"
            return ruid, message, status

        # Verifica si la fecha de comienzo es mayor que la fecha de finalizacion
        if (startdate >= enddate):
            #print("Error al añadir la habitacion indisponible")
            message ="The start date must be a date before the end date"
            status = "error"
            return ruid, message, status

        date_format = "%Y-%m-%d"
        with self.db.conexion.cursor() as cur:
            try:
                rid = int(rid)
                try:
                    startdate = datetime.strptime(startdate, date_format).date()
                    enddate = datetime.strptime(enddate, date_format).date()
                except ValueError:
                    self.db.conexion.rollback()
                    return False, "Error al insertar la fecha. Asegurate que el formato sea el siguiente: (YYYY-MM-DD)"
                query = "INSERT INTO roomunavailable (rid, startdate, enddate) VALUES(%s, %s, %s) RETURNING ruid"
                cur.execute(query, (rid, startdate,enddate))
                self.db.conexion.commit()
                ruid = cur.fetchone()[0]
            except Exception as e:
                #print(f"Error al añadir la habitación indisponible: {e}")
                self.db.conexion.rollback()
                message = str(e)
                status = "error"
            finally:
                cur.close()
                return ruid, message, status

    def deleteRoomUnavailable(self, ruid):
        with self.db.conexion.cursor() as cur:
            try:
                # Verifica si habitacion indisponible existe
                cur.execute("SELECT COUNT(*) FROM roomunavailable WHERE ruid = %s", (ruid,))
                room_count = cur.fetchone()[0]
                if room_count == 0:
                    return False, "La habitación no existe"
                #Si existe, elimina
                query = "DELETE FROM roomunavailable WHERE ruid = %s"
                cur.execute(query, (ruid,))
                self.db.conexion.commit()
                return True, "La habitacion indisponible eliminada exitosamente"
            except Exception as e:
                print(f"Error el eliminar habitacion indisponible: {e}")
                return False, "Error al eliminar habitacion indisponible."
            finally:
                cur.close()

    def putRoomUnavailable(self, ruid, rid, startdate, enddate):
        # Verifica si la fecha de comienzo es mayor que la fecha de finalizacion
        if (startdate >= enddate):
            print("Error al cambiar la informacion de la habitacion indisponible")
            return False, "La fecha en que comienza debe ser una fecha anterior a la fecha en la que termina"

        date_format = "%Y-%m-%d"
        with self.db.conexion.cursor() as cur:
            # Verifica si la habitacion indisponible existe
            cur.execute("SELECT COUNT(*) FROM roomunavailable WHERE ruid = %s", (ruid,))
            room_count = cur.fetchone()[0]
            if room_count == 0:
                return False, "La habitación indisponible no existe"


            try:
                rid = int(rid)
                # Verifica el formato de la fecha
                try:
                    startdate = datetime.strptime(startdate, date_format).date()
                    enddate = datetime.strptime(enddate, date_format).date()
                except ValueError:
                    self.db.conexion.rollback()
                    return False, "Error al insertar la fecha. Asegurate que el formato sea el siguiente: (YYYY-MM-DD)"

                # Actualiza
                query = "UPDATE  roomunavailable SET rid = %s, startdate = %s, enddate = %s WHERE ruid = %s"
                cur.execute(query, (rid, startdate, enddate, ruid))

                # Verifica si se actualizó alguna fila
                if cur.rowcount == 0:
                    self.db.conexion.rollback()
                    return False, "No se pudo actualizar la habitación"

                # Confirma la transacción
                self.db.conexion.commit()
                return True, "Habitacion indisponible actualizada exitosamente"
            except Exception as e:
                print(f"Error al actualizar la habitación indisponible: {e}")
                self.db.conexion.rollback()
                return False, "Error al agregar habitacion indisponible."
            finally:
                cur.close()

    def getTop3LeastUnavailable(self, hid, eid):
        if not self.db.canAccessLocalStats(eid, hid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas del hotel {hid}.")
            return None
        cur = self.db.conexion.cursor()
        try:
            query = """SELECT hid, rid, SUM(enddate-startdate) as reserve
                        FROM roomunavailable natural inner join room natural inner join hotel
                        WHERE hid = %s
                        GROUP BY hid, rid
                        ORDER BY reserve
                        ASC LIMIT 3
                    """
            cur.execute(query, (hid,))
            roomsunavailble_list = cur.fetchall()
            return roomsunavailble_list
        except Exception as e:
            print(f"Error al obtener las tres habitaciones menos reservadas del hotel con id {hid} {e}")
            return None
        finally:
            self.db.conexion.close()
            cur.close()
