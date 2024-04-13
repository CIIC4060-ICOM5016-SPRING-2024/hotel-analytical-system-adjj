from .db import Database
from api.validate_inputs import employee_inputs_are_correct
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

    def getEmployeeById(self, eid):
        cur = self.db.conexion.cursor()
        try:
            query = "SELECT hid, fname, lname, position, salary, age FROM employee WHERE eid = %s"
            cur.execute(query, (eid,))
            employee = cur.fetchone()
            return employee
        except Exception as e:
            print(f"Error al obtener el employee con ID {eid}: {e}")
            self.db.conexion.rollback()
            return None
        finally:
            self.db.close()
            cur.close()

    def postEmployee(self, hid, fname, lname, age, salary, position):
        # Asegurarse de que la posición sea válida
        eid = None
        message = "Employee added successfully"
        status = "success"
        validInput, validMessage = employee_inputs_are_correct(position, salary)
        if not (validInput):
            status = "error"
            return eid, message, status

        cur = self.db.conexion.cursor()  # Asumiendo que esto abre el cursor correctamente.

        try:
            query = """
                    INSERT INTO employee (hid, fname, lname, age, salary, position) 
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING eid
                    """
            cur.execute(query, (hid, fname, lname, age, salary, position))
            self.db.conexion.commit()
            eid = cur.fetchone()[0]
        except Exception as e:
            #print(f"Error al insertar empleado: {e}")
            message = str(e)
            status = "error"
            self.db.conexion.rollback()  # Opcional: deshacer cambios en caso de error.
        finally:
            self.db.close()
            cur.close()
            return eid, message, status

    def deleteEmployee(self, eid):
        cur = self.db.conexion.cursor()
        message = "Employee successfully removed"
        success = True
        try:
            query = "DELETE FROM employee WHERE eid = %s"
            cur.execute(query, (eid,))
            self.db.conexion.commit()
        except Exception as e:
            #print(f"Error al eliminar empleado: {e}")
            self.db.conexion.rollback()
            message = str(e)
            success = False
        finally:
            cur.close()
            self.db.close()
            return success, message

    def putEmployee(self, eid, hid, fname, lname, age, salary, position):

        if not (employee_inputs_are_correct(position, salary)):
            return False

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

    def getTopPaidRegularEmployeesByHotel(self, hid, eid):

        if not self.db.canAccessLocalStats(eid, hid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas del hotel {hid}.")
            return None

        cur = self.db.conexion.cursor()
        try:
            query = """
                    SELECT eid, hid, fname, lname, age, salary, position 
                    FROM employee 
                    WHERE position = 'Regular' AND hid = %s
                    ORDER BY salary DESC 
                    LIMIT 3
                    """
            cur.execute(query, (hid,))
            employees = cur.fetchall()
            return employees
        except Exception as e:
            print(f"Error al obtener los empleados regulares mejor pagados para el hotel {hid}: {e}")
            return None
        finally:
            cur.close()
            self.db.close()