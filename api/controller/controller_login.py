from flask import jsonify, request, make_response
from api.model.model_login import LoginDAO
class LoginController:
    def dicBuild(self, row):
        a_dict = {'lid': row[0], 'eid': row[1], 'username': row[2], 'password': row[3]}
        return a_dict
    def getAllLogins(self):
        dao = LoginDAO()
        au_dict = dao.getAllLogins()
        result = []
        for elements in au_dict:
            result.append(self.dicBuild(elements))
        return jsonify(result)
    def getLoginById(self,lid):
        dao = LoginDAO()
        login = dao.getLoginById(lid)
        if login:
            result = self.dicBuild(login)
            return jsonify(result)
        else:
            return make_response(jsonify({"error": f"No se encontró el Login con ID {lid}"}), 404)

    def addLogin(self):
        if request.method == "POST":
            data = request.get_json()
            if not all(key in data for key in ('eid', 'username', 'password')):
                return make_response(jsonify({"error": "Faltan datos"}), 400)


            dao = LoginDAO()
            success, message = dao.postLogin(data['eid'], data['username'], data['password'])

            if success:
                return make_response(jsonify({"message": f"Login agregado exitosamente"}), 201)
            else:
                return make_response(jsonify({"error": f"Error al agregar Login"}), 500)

    def deleteLogin(self, lid):
        dao = LoginDAO()
        success = dao.deleteLogin(lid)
        if success:
            return make_response(jsonify({"message": "Login eliminado exitosamente"}), 200)
        else:
            return make_response(jsonify({"error": "Error al eliminar Login"}), 500)



    def putLogin(self, lid):
        if request.method == "PUT":
            data = request.get_json()
            required_fields = ('eid', 'username', 'password')

            if not all(field in data for field in required_fields):
                return make_response(jsonify({"error": "Faltan datos"}), 400)

            dao = LoginDAO()

            success = dao.putLogin(lid, data['eid'], data['username'], data['password'])
            if success:
                return make_response(jsonify({"message": "Login actualizado exitosamente"}), 200)
            else:
                return make_response(jsonify({"error": "Error al actualizar Login"}), 500)

