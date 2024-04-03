from .db import Database


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
    #     cur = self.db.conexion.cursor()
    #     try:
    #         query = """INSERT INTO login (eid, username, password) VALUES (%s,%s,%s)"""
    #         cur.execute(query, (eid, username, password))
    #         self.db.conexion.commit()
    #     except Exception as e:
    #         print(f"Error al insertar Login: {e}") # decidir que realmente escribir aqui
    #         self.db.conexion.rollback()
    #         return False, f"Error al agregar Login: {e}"
    #     finally:
    #         self.db.close()
    #         cur.close()
    #     return True, f"Login agregado exitosamente"

    # def deleteLogin(self, lid):
    #     cur = self.db.conexion.cursor()
    #     try:
    #         query = "DELETE FROM login where lid = %s"
    #         cur.execute(query, (lid,))
    #         self.db.conexion.commit()
    #         return True
    #     except Exception as e:
    #         print(f"Error al eliminar el login con ID {lid}: {e}")
    #         self.db.conexion.rollback()
    #         return False
    #     finally:
    #         cur.close()
    #         self.db.close()

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
