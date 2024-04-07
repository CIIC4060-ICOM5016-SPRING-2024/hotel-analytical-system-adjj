from .db import Database
from api.validate_inputs import post_room_description_validation


class RoomDescriptionDAO:
    def __init__(self):
        self.db = Database()

    def getAllRoomsDescriptions(self):
        cur = self.db.conexion.cursor()
        query = "SELECT rdid, rname, rtype, capacity, ishandicap FROM roomdescription"
        cur.execute(query)
        roomdescription_list = cur.fetchall()
        self.db.close()
        cur.close()
        return roomdescription_list

    def getRoomsDescriptionById(self, rdid):
        cur = self.db.conexion.cursor()
        try:
            query = "SELECT rdid, rname, rtype, capacity, ishandicap FROM roomdescription WHERE rdid = %s"
            cur.execute(query, (rdid,))
            roomdescription = cur.fetchone()
            return roomdescription
        except Exception as e:
            print(f"Error al obtener la descripcion del cuarto con ID {rdid}: {e}")
            self.db.conexion.rollback()
            return None
        finally:
            self.db.close()
            cur.close()

    def postRoomDescription(self, rname, rtype, capacity, ishandicap):
        # Ensure that the room description is valid

        if not post_room_description_validation(rname, rtype, capacity):
            return False

        cur = self.db.conexion.cursor()  # Assuming this opens the cursor correctly.
        try:
            query = """
                    INSERT INTO roomdescription (rname, rtype, capacity, ishandicap) 
                    VALUES (%s, %s, %s, %s)
                    """
            cur.execute(query, (rname, rtype, capacity,ishandicap))
            self.db.conexion.commit()

            return True, "Room description agregada exitosamente"

        except Exception as e:
            print(f"Error when inserting room description: {e}")
            self.db.conexion.rollback()  # Optional: rollback changes in case of an error.
            return False, str(e)
        finally:
            self.db.close()
            cur.close()  # Assuming there's a separate method to close the database connection itself.
        return True



    def deleteRoomDescription(self, rdid):
        cur = self.db.conexion.cursor()
        try:
            query = "DELETE FROM roomdescription WHERE rdid = %s"
            cur.execute(query, (rdid,))
            self.db.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar room description: {e}")
            self.db.conexion.rollback()
            return False
        finally:
            cur.close()
            self.db.close()


###DONE!!!
    def putRoomDescription(self, rdid, rname,rtype,capacity,ishandicap):
        if not post_room_description_validation(rname, rtype, capacity):
            return False

        cur = self.db.conexion.cursor()
        try:
            # Construye la consulta SQL de actualización
            query = """
                    UPDATE roomdescription 
                    SET rname = %s, rtype = %s, capacity = %s, ishandicap = %s
                    WHERE rdid = %s
                    """
            # Ejecuta la consulta con los valores proporcionados
            cur.execute(query, (rname,rtype,capacity,ishandicap,rdid))
            # Si no se actualizó ningún registro, podría significar que el hid no existe
            if cur.rowcount == 0:
                self.db.conexion.rollback()  # Opcional: revertir en caso de no encontrar el hotel
                return False
            # Si se actualizó el registro, hacer commit de los cambios
            self.db.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar descripcion de habitacion: {e}")
            self.db.conexion.rollback()
            return False
        finally:
            cur.close()
            self.db.close()


