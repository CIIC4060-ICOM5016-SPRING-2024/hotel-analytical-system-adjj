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