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