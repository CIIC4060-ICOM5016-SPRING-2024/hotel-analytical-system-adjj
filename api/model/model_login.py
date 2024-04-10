from .db import Database
from ..validate_inputs import employee_inputs_are_correct
from api.controller.controller_employee import EmployeeController
from api.model.model_employee import EmployeeDAO



class LoginDAO:
    def __init__(self):
        self.db = Database()

    def getAllLogins(self):
        cur = self.db.conexion.cursor()
        query = "SELECT lid, eid, username, password FROM login"
        cur.execute(query)
        login_list = cur.fetchall()
        self.db.close()
        cur.close()

        return login_list

    def getLoginById(self, lid):
        cur = self.db.conexion.cursor()
        try:
            query = "SELECT eid, username, password  FROM login where lid = %s"
            cur.execute(query, (lid,))
            login = cur.fetchone()
            return login
        except Exception as e:
            print(f"Error al obtener el login con ID {lid}:{e}")
            self.db.conexion.rollback()
            return None
        finally:
            self.db.close()
            cur.close()







    # def postLogin(self, eid, username, password):
    #
    #     # Additional validation can be done here if necessary
    #     cur = self.db.conexion.cursor()  # Assuming this correctly opens the cursor
    #     try:
    #         query = """
    #                 INSERT INTO login (eid, username, password)
    #                 VALUES (%s, %s, %s)
    #                 """
    #         cur.execute(query, (eid, username, password))
    #         self.db.conexion.commit()
    #     except Exception as e:
    #         print(f"Error inserting login information: {e}")
    #         self.db.conexion.rollback()  # Optional: undo changes in case of error
    #         return False
    #     finally:
    #         self.db.close()
    #         cur.close()
    #     return True

    def postLogin(self, eid, username, password):
        cur = self.db.conexion.cursor()  # Assuming this correctly opens the cursor

        # Check if the eid exists in the Employee table
        cur.execute("SELECT COUNT(*) FROM Employee WHERE eid = %s", (eid,))
        if cur.fetchone()[0] == 0:
            print("Please create an employee before attempting to create a login for this eid.")
            return "employee_not_found"

        # Check if there is already a login associated with this eid
        cur.execute("SELECT COUNT(*) FROM Login WHERE eid = %s", (eid,))
        if cur.fetchone()[0] > 0:
            print("There is already login information related to this eid.")
            return "login_exists"
        lid = None
        try:
            query = """
                    INSERT INTO Login (eid, username, password) 
                    VALUES (%s, %s, %s) RETURNING lid
                    """
            cur.execute(query, (eid, username, password))
            self.db.conexion.commit()
            lid = cur.fetchone()[0]
        except Exception as e:
            print(f"Error inserting login information: {e}")
            self.db.conexion.rollback()  # Optional: undo changes in case of error
        finally:
            cur.close()  # Moved up to ensure the cursor is always closed before db connection
            self.db.close()
            return lid

    def deleteLogin(self, lid):
        cur = self.db.conexion.cursor()
        try:
            query = "DELETE FROM login WHERE lid = %s"
            cur.execute(query, (lid,))
            self.db.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar login: {e}")
            self.db.conexion.rollback()
            return False
        finally:
            cur.close()
            self.db.close()

    def putLogin(self, lid, eid, username, password):
        cur = self.db.conexion.cursor()

        try:
            query = """UPDATE login SET eid = %s, username = %s, password =%s WHERE lid = %s"""

            cur.execute(query, (eid, username, password, lid))

            if cur.rowcount == 0:
                self.db.conexion.rollback()
                return False
            self.db.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar el login con ID {e}")
            self.db.conexion.rollback()
            return False
        finally:
            cur.close()
            self.db.close()



    def putLogin(self, lid, eid, username, password):
        cur = self.db.conexion.cursor()

        try:
            query = """UPDATE login SET eid = %s, username = %s, password =%s WHERE lid = %s"""

            cur.execute(query, (eid, username, password, lid))

            if cur.rowcount == 0:
                self.db.conexion.rollback()
                return False
            self.db.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar el login con ID {e}")
            self.db.conexion.rollback()
            return False
        finally:
            cur.close()
            self.db.close()
