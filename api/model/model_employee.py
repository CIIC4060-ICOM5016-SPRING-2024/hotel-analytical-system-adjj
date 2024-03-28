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