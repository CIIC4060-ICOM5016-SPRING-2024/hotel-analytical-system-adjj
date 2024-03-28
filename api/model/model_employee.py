from .db import Database
class EmployeeDAO:
    def __init__(self):
        self.db = Database()

    def getAllEmployees(self):
        cur = self.db.conexion.cursor()
        query = "SELECT eid, hid, fname, lname, age, salary, position FROM employee"
        cur.execute(query)
        employee_list = cur.fetchall()
        self.db.close()
        cur.close()

        return employee_list

    def postEmployee(self, hid, fname, lname, age, salary, position):
        cur = self.db.conexion.cursor()  # Asumiendo que esto abre el cursor correctamente.
        try:
            query = """
                    INSERT INTO employee (hid, fname, lname, age, salary, position) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
            cur.execute(query, (hid, fname, lname, age, salary, position))
            self.db.conexion.commit()
        except Exception as e:
            print(f"Error al insertar empleado: {e}")
            self.db.conexion.rollback()  # Opcional: deshacer cambios en caso de error.
            return False
        finally:
            self.db.close()
            cur.close()
        return True

    def deleteEmployee(self, eid):
        cur = self.db.conexion.cursor()
        try:
            query = "DELETE FROM employee WHERE eid = %s"
            cur.execute(query, (eid,))
            self.db.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar empleado: {e}")
            self.db.conexion.rollback()
            return False
        finally:
            cur.close()
            self.db.close()

    def putEmployee(self, eid, hid, fname, lname, age, salary, position):
        cur = self.db.conexion.cursor()
        try:
            # Construye la consulta SQL de actualización
            query = """
                    UPDATE employee
                    SET hid = %s, fname = %s, lname = %s, age = %s, salary = %s, position = %s
                    WHERE eid = %s
                    """
            # Ejecuta la consulta con los valores proporcionados
            cur.execute(query, (hid, fname, lname, age, salary, position, eid))
            # Si no se actualizó ningún registro, podría significar que el eid no existe
            if cur.rowcount == 0:
                self.db.conexion.rollback()  # Opcional: revertir en caso de no encontrar el empleado
                return False
            # Si se actualizó el registro, hacer commit de los cambios
            self.db.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar empleado: {e}")
            self.db.conexion.rollback()
            return False
        finally:
            cur.close()
            self.db.close()