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

    def getClientById(self, clid):
        cur = self.db.conexion.cursor()
        try:
            query = "SELECT fname, lname, age, memberyear FROM client WHERE clid = %s"
            cur.execute(query, (clid,))
            client = cur.fetchone()
            return client
        except Exception as e:
            print(f"Error al obtener el client con ID {clid}: {e}")
            self.db.conexion.rollback()
            return None
        finally:
            self.db.close()
            cur.close()

    def postClient(self, fname, lname, age, memberyear):
        # Asegurarse de que la posición sea válida
        # if not (employee_inputs_are_correct(position, salary)):
        #     return False
        clid = None
        message = "Client added successfully"
        status = "success"
        cur = self.db.conexion.cursor()  # Asumiendo que esto abre el cursor correctamente.
        try:
            query = """
                    INSERT INTO client (fname, lname, age, memberyear) 
                    VALUES (%s, %s, %s, %s) RETURNING clid
                    """
            cur.execute(query, (fname, lname, age, memberyear))
            self.db.conexion.commit()
            clid = cur.fetchone()[0]
        except Exception as e:
            #print(f"Error al insertar cliente: {e}")
            message = str(e)
            status = "error"
            self.db.conexion.rollback()  # Opcional: deshacer cambios en caso de error.
        finally:
            self.db.close()
            cur.close()
            return clid, message, status


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


    def getTop5CreditCardReservations(self, hid, eid):
        if not self.db.canAccessLocalStats(eid, hid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas del hotel {hid}.")
            return None

        cur = self.db.conexion.cursor()
        try:
            query = """
                            SELECT 
                                c.clid, c.fname, c.lname, COUNT(re.reid) AS reservation_count
                            FROM 
                                Client c
                            JOIN 
                                Reserve re ON c.clid = re.clid
                            JOIN
                                RoomUnavailable ru ON re.ruid = ru.ruid
                            JOIN
                                Room r ON ru.rid = r.rid
                            WHERE 
                                c.age < 30 AND re.payment = 'credit card' AND r.hid = %s
                            GROUP BY 
                                c.clid
                            ORDER BY 
                                reservation_count DESC
                            LIMIT 5;
                            """
            cur.execute(query, (hid,))
            top_clients = cur.fetchall()
            return top_clients
        except Exception as e:
            print(
                f"Error al obtener el top 5 de clientes menores de 30 con más reservaciones con tarjeta de crédito para el hotel {hid}: {e}")
            return None
        finally:
            self.db.close()
            cur.close()

    def getTop5ClientsMostDiscount(self,hid, eid):
        if not self.db.canAccessLocalStats(eid, hid):
            print(f"El empleado {eid} no tiene acceso a las estadísticas del hotel {hid}.")
            return None
        try:
            cur = self.db.conexion.cursor()

            query="""
                SELECT 
                    clid, 
                    fname, 
                    lname, 
                    age, 
                    memberyear,
                    CASE 
                        WHEN memberyear BETWEEN 1 AND 4 THEN 2
                        WHEN memberyear BETWEEN 5 AND 9 THEN 5
                        WHEN memberyear BETWEEN 10 AND 14 THEN 8
                        WHEN memberyear >= 15 THEN 12
                        ELSE 0
                    END AS discount_percentage
                FROM 
                    Client
                ORDER BY 
                    discount_percentage DESC, 
                    memberyear DESC -- En caso de empates en el descuento, se prioriza al miembro más antiguo
                LIMIT 5;
            """
            cur.execute(query, (hid,))
            top_clients = cur.fetchall()
            return top_clients
        except Exception as e:
            print(
                f"Error al obtener el top 5 de clientes con mas porcentaje de descuento en el hotel {hid}: {e}")
            return None
        finally:
            self.db.close()
            cur.close()
            