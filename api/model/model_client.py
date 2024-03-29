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

    def putClient(self, clid, fname, lname, age, memberyear):

        # if not (employee_inputs_are_correct(position, salary)):
        #     return False

        cur = self.db.conexion.cursor()
        try:
            # Construye la consulta SQL de actualización
            query = """
                    UPDATE client
                    SET fname = %s, lname = %s, age = %s, memberyear = %s
                    WHERE clid = %s
                    """
            # Ejecuta la consulta con los valores proporcionados
            cur.execute(query, (fname, lname, age, memberyear, clid))
            # Si no se actualizó ningún registro, podría significar que el clid no existe
            if cur.rowcount == 0:
                self.db.conexion.rollback()  # Opcional: revertir en caso de no encontrar el client
                return False
            # Si se actualizó el registro, hacer commit de los cambios
            self.db.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar client: {e}")
            self.db.conexion.rollback()
            return False
        finally:
            cur.close()
            self.db.close()