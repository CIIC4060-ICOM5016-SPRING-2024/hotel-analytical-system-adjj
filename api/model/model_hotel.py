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