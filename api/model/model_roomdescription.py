from .db import Database
from ..validate_inputs import roomDescription_inputs_are_correct


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
        # Asegurarse de que la posición sea válida
        if not (roomDescription_inputs_are_correct(rname, rtype, capacity,ishandicap)):
            return False, "Inputs no son correctos"

        cur = self.db.conexion.cursor()  # Asumiendo que esto abre el cursor correctamente.
        try:
            query = """
                    INSERT INTO roomdescription ( rname, rtype, capacity, ishandicap ) 
                    VALUES (%s, %s, %s, %s)
                    """
            cur.execute(query, (rname, rtype, capacity, ishandicap))
            self.db.conexion.commit()
        except Exception as e:
            print(f"Error al insertar room description: {e}")
            self.db.conexion.rollback()  # Opcional: deshacer cambios en caso de error.
            return False, f"Error al agregar room description: {e}"
        finally:
            self.db.close()
            cur.close()
        return True, f"room description agregada exitosamente"