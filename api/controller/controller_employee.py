# from model.client import ClientDAO
from api.model.model_employee import EmployeeDAO
from flask import jsonify, request, make_response

class EmployeeContoller:


    def dicBuild(self, row):
        a_dict = {'eid':row[0],
                  'hid':row[1],
                  'fname':row[2],
                  'lname':row[3],
                  'age':row[4],
                  'salary':row[5],
                  'position':row[6]
                  }
        return a_dict

    def getAllEmployees(self):
        dao = EmployeeDAO()
        au_dict = dao.getAllEmployees()
        result = []
        for element in au_dict:
            result.append(self.dicBuild(element))
        return jsonify(result)

    def addEmployee(self):
        if request.method == 'POST':
            # Obtener datos del cuerpo de la petición
            data = request.get_json()
            # Validar que todos los campos necesarios están presentes
            if not all(key in data for key in ('hid', 'fname', 'lname', 'age', 'salary', 'position')):
                return make_response(jsonify({"error": "Faltan datos"}), 400)

            # Crear una instancia de EmployeeDAO
            dao = EmployeeDAO()
            # Llamar al método para insertar el nuevo empleado
            success = dao.postEmployee(data['hid'], data['fname'], data['lname'], data['age'], data['salary'],
                                       data['position'])

            if success:
                return make_response(jsonify({"message": "Empleado agregado exitosamente"}), 201)
            else:
                return make_response(jsonify({"error": "Error al agregar empleado"}), 500)