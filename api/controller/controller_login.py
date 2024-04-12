from flask import jsonify, request, make_response
from api.model.model_login import LoginDAO


class LoginController:
    def dicBuild(self, row):
        a_dict = {'lid': row[0],
                  'eid': row[1],
                  'username': row[2],
                  'password': row[3]}
        return a_dict

    def getAllLogins(self):
        dao = LoginDAO()
        au_dict = dao.getAllLogins()
        result = []
        for elements in au_dict:
            result.append(self.dicBuild(elements))
        return jsonify(result)

    def getLoginById(self, lid):
        def fict_build(row):
            a_dict = {'lid': lid,
                      'eid': row[0],
                      'username': row[1],
                      'password': row[2]
                      }
            return a_dict

        dao = LoginDAO()
        login = dao.getLoginById(lid)
        if login:
            result = fict_build(login)
            return jsonify(result)
        else:
            return make_response(jsonify({"error": f"No se encontró el Login con ID {lid}"}), 404)


    def addLogin(self):
        if request.method == 'POST':
            data = request.get_json()
            if not all(key in data for key in ['eid', 'username', 'password']):
                message = "Data to be sent was missing in the request json"
                id = None
                status = "error"
                return make_response(jsonify({"message": message, "id": id, "status": status}), 400)

            dao = LoginDAO()  # Assuming this is properly defined and instantiated
            id, message, status = dao.postLogin(data['eid'], data['username'], data['password'])
            json = jsonify({"message": message, "id": id, "status": status})

            if id:
                return make_response(json,201)
            else:
                return make_response(json,500)

    def deleteEmployee(self, lid):
        dao = LoginDAO()
        success = dao.deleteLogin(lid)
        if success:
            return make_response(jsonify({"message": "Login eliminado exitosamente", "status":"success"}), 200)
        else:
            return make_response(jsonify({"message": "Error al eliminar login", "status":"error"}), 500)



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







