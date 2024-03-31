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

    def getTop5CreditCardReservations(self,hid):

        def fict_build(row):
            a_dict = {
                'clid': row[0],
                'fname': row[1],
                'lname': row[2],
                'reservation_count': row[3]
            }
            return a_dict

        dao = ClientDAO()
        au_dict = dao.getTop5CreditCardReservations(hid)
        result = []
        for element in au_dict:
            result.append(fict_build(element))
        return jsonify(result)