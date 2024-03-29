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