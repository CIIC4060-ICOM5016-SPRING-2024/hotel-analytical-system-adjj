# from model.client import ClientDAO
from api.model.model_client import ClientDAO
from flask import jsonify, request, make_response
from flask import jsonify

class ClientContoller:

    def dicBuild(self, row):
        a_dict = {'clid':row[0],
                  'fname':row[1],
                  'lname':row[2],
                  'age':row[3],
                  'memberyear':row[4]
                  }
        return a_dict

    def getAllClients(self):
        dao = ClientDAO()
        au_dict = dao.getAllClients()
        result = []
        for element in au_dict:
            result.append(self.dicBuild(element))
        return jsonify(result)

    def getClientById(self,clid):
        def fict_build(row):
            a_dict = {'clid':clid,
                      'fname':row[0],
                      'lname':row[1],
                      'age':row[2],
                      'memberyear':row[3]
                      }
            return a_dict

        dao = ClientDAO()
        employee = dao.getClientById(clid)  # Esto ahora espera una sola fila o None
        if employee:
            # Ya que esperamos un único resultado, no hay necesidad de iterar
            result = fict_build(employee)
            return jsonify(result)
        else:
            # Manejar el caso en que no se encuentre el hotel
            return make_response(jsonify({"error": f"No se encontró el client con ID {clid}"}), 404)

    def addEmployee(self):
        if request.method == 'POST':
            # Obtener datos del cuerpo de la petición
            data = request.get_json()
            # Validar que todos los campos necesarios están presentes
            if not all(key in data for key in ('fname', 'lname', 'age', 'memberyear')):
                return make_response(jsonify({"error": "Faltan datos"}), 400)

            # Crear una instancia de ClientDAO
            dao = ClientDAO()
            # Llamar al método para insertar el nuevo empleado
            success = dao.postClient(data['fname'], data['lname'], data['age'],data['memberyear'])

            if success:
                return make_response(jsonify({"message": "Client agregado exitosamente"}), 201)
            else:
                return make_response(jsonify({"error": "Error al agregar client"}), 500)

    def deleteClient(self, clid):
        dao = ClientDAO()
        success = dao.deleteClient(clid)
        if success:
            return make_response(jsonify({"message": "Client eliminado exitosamente"}), 200)
        else:
            return make_response(jsonify({"error": "Error al eliminar client"}), 500)

    def putClient(self, clid):
        if request.method == 'PUT':
            # Obtener los datos actualizados del cuerpo de la petición
            data = request.get_json()
            # Validar que todos los campos necesarios están presentes
            required_fields = ['fname', 'lname', 'age', 'memberyear']
            if not all(field in data for field in required_fields):
                return make_response(jsonify({"error": "Faltan datos"}), 400)

            # Crear una instancia de EmployeeDAO
            dao = ClientDAO()
            # Llamar al método para actualizar el empleado
            success = dao.putClient(clid, data['fname'], data['lname'], data['age'], data['memberyear'])

            if success:
                return make_response(jsonify({"message": "Client actualizado exitosamente"}), 200)
            else:
                # Si no se pudo actualizar, podría ser debido a un eid inválido o problemas internos del servidor
                return make_response(jsonify({"error": "Error al actualizar client"}), 500)

    def getTop5CreditCardReservations(self, hid):

        def fict_build(row):
            a_dict = {
                'clid': row[0],
                'fname': row[1],
                'lname': row[2],
                'reservation_count': row[3]
            }
            return a_dict

        data = request.get_json()
        # Validar que todos los campos necesarios están presentes
        required_fields = ['eid']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)

        dao = ClientDAO()
        au_dict = dao.getTop5CreditCardReservations(hid, data['eid'])
        if au_dict == None:
            return make_response(jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas del hotel {hid}."))
        result = []
        for element in au_dict:
            result.append(fict_build(element))
        return jsonify(result)

    def getTop5ClientsMostDiscount(self,hid):
        def fict_build(row):
            dict={
                'clid': row[0],
                'fname': row[1],
                'lname': row[2],
                'age': row[3],
                'memberyear':row[4],
                'discount_percentage':row[5]
            }
            return dict
        data = request.get_json()
        required_fields = ['eid']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)

        dao = ClientDAO()
        au_dict = dao.getTop5ClientsMostDiscount(hid, data['eid'])
        if au_dict == None:
            return make_response(jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas del hotel {hid}."))
        result = []
        for element in au_dict:
            result.append(fict_build(element))
        return jsonify(result)

