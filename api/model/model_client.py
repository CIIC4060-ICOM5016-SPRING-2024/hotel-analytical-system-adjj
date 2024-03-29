from .db import Database
class ClientDAO:
    def __init__(self):
        self.db = Database()

    def getAllClients(self):
        cur = self.db.conexion.cursor()
        query = "SELECT clid, fname, lname, age, memberyear  FROM client"
        cur.execute(query)
        client_list = cur.fetchall()
        self.db.close()
        cur.close()

        return client_list

    def postClient(self, fname, lname, age, memberyear):
        # Asegurarse de que la posición sea válida
        # if not (employee_inputs_are_correct(position, salary)):
        #     return False

        cur = self.db.conexion.cursor()  # Asumiendo que esto abre el cursor correctamente.
        try:
            query = """
                    INSERT INTO client (fname, lname, age, memberyear) 
                    VALUES (%s, %s, %s, %s)
                    """
            cur.execute(query, (fname, lname, age, memberyear))
            self.db.conexion.commit()
        except Exception as e:
            print(f"Error al insertar cliente: {e}")
            self.db.conexion.rollback()  # Opcional: deshacer cambios en caso de error.
            return False
        finally:
            self.db.close()
            cur.close()
        return True


    def deleteClient(self, clid):
        cur = self.db.conexion.cursor()
        try:
            query = "DELETE FROM client WHERE clid = %s"
            cur.execute(query, (clid,))
            self.db.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar client: {e}")
            self.db.conexion.rollback()
            return False
        finally:
            cur.close()
            self.db.close()