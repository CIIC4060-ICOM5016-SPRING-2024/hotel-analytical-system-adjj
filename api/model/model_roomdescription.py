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
        rdid = None
        message = "Room Description added successfully"
        status = "success"
        if not post_room_description_validation(rname, rtype, capacity):
            valid_descriptions = {
                'Standard': {'capacities': [1], 'types': ['Basic', 'Premium']},
                'Standard Queen': {'capacities': [1, 2], 'types': ['Basic', 'Premium', 'Deluxe']},
                'Standard King': {'capacities': [2], 'types': ['Basic', 'Premium', 'Deluxe']},
                'Double Queen': {'capacities': [4], 'types': ['Basic', 'Premium', 'Deluxe']},
                'Double King': {'capacities': [4, 6], 'types': ['Basic', 'Premium', 'Deluxe', 'Suite']},
                'Triple King': {'capacities': [6], 'types': ['Deluxe', 'Suite']},
                'Executive Family': {'capacities': [4, 6, 8], 'types': ['Deluxe', 'Suite']},
                'Presidential': {'capacities': [4, 6, 8], 'types': ['Suite']}
            }
            message = (f"The values entered to create the room description are incorrect. The options are the following:"
                       f"{valid_descriptions}")
            status = "error"
            return rdid, message, status

        cur = self.db.conexion.cursor()  # Assuming this opens the cursor correctly.

        try:
            query = """
                    INSERT INTO roomdescription (rname, rtype, capacity, ishandicap) 
                    VALUES (%s, %s, %s, %s) RETURNING rdid
                    """
            cur.execute(query, (rname, rtype, capacity,ishandicap))
            self.db.conexion.commit()
            rdid = cur.fetchone()[0]
        except Exception as e:
            #print(f"Error when inserting room description: {e}")
            self.db.conexion.rollback()  # Optional: rollback changes in case of an error.
            message = str(e)
            status = "error"
        finally:
            self.db.close()
            cur.close()  # Assuming there's a separate method to close the database connection itself.
            return rdid,message,status



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


