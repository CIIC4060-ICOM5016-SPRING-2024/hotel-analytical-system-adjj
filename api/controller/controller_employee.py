# from model.client import ClientDAO
from api.model.model_employee import EmployeeDAO
from api.model.model_hotel import HotelDAO
from flask import jsonify, request, make_response

class EmployeeController:


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

    def getEmployeeById(self,eid):
        def fict_build(row):
            a_dict = {'eid': eid,
                      'hid': row[0],
                      'fname': row[1],
                      'lname': row[2],
                      'position': row[3],
                      'salary': row[4],
                      'age': row[5],
                      }
            return a_dict

        dao = EmployeeDAO()
        employee = dao.getEmployeeById(eid)  # Esto ahora espera una sola fila o None
        if employee:
            # Ya que esperamos un único resultado, no hay necesidad de iterar
            result = fict_build(employee)
            return jsonify(result)
        else:
            # Manejar el caso en que no se encuentre el hotel
            return make_response(jsonify({"error": f"No se encontró el employee con ID {eid}"}), 404)

    def addEmployee(self):
        if request.method == 'POST':
            # Obtener datos del cuerpo de la petición
            data = request.get_json()
            # Validar que todos los campos necesarios están presentes
            if not all(key in data for key in ('hid', 'fname', 'lname', 'age', 'salary', 'position')):
                message = "Data to be sent was missing in the request json"
                id = None
                status = "error"
                return make_response(jsonify({"message": message, "id": id, "status": status}), 400)

            # Crear una instancia de EmployeeDAO
            dao = EmployeeDAO()
            # Llamar al método para insertar el nuevo empleado
            id, message, status = dao.postEmployee(data['hid'], data['fname'], data['lname'], data['age'], data['salary'],
                                       data['position'])

            json = jsonify({"message": message, "id": id, "status": status})
            if id:
                return make_response(json, 201)
            else:
                return make_response(json, 500)

    def deleteEmployee(self, eid):
        dao = EmployeeDAO()
        success, message = dao.deleteEmployee(eid)
        if success:
            return make_response(jsonify({"message": message, "status":"success"}), 200)
        else:
            return make_response(jsonify({"message": message, "status":"error"}), 500)

    def putEmployee(self, eid):
        if request.method == 'PUT':
            # Obtener los datos actualizados del cuerpo de la petición
            data = request.get_json()
            # Validar que todos los campos necesarios están presentes
            required_fields = ['hid', 'fname', 'lname', 'age', 'salary', 'position']
            if not all(field in data for field in required_fields):
                return make_response(jsonify({"error": "Faltan datos"}), 400)

            # Crear una instancia de EmployeeDAO
            dao = EmployeeDAO()
            # Llamar al método para actualizar el empleado
            success = dao.putEmployee(eid, data['hid'], data['fname'], data['lname'], data['age'], data['salary'],
                                      data['position'])

            if success:
                return make_response(jsonify({"message": "Empleado actualizado exitosamente"}), 200)
            else:
                # Si no se pudo actualizar, podría ser debido a un eid inválido o problemas internos del servidor
                return make_response(jsonify({"error": "Error al actualizar empleado"}), 500)

    def getTopPaidRegularEmployeesByHotel(self, hid):
        data = request.get_json()
        # Validar que todos los campos necesarios están presentes
        required_fields = ['eid']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)


        dao = EmployeeDAO()
        au_dict = dao.getTopPaidRegularEmployeesByHotel(hid, data['eid'])
        if au_dict == None:
            return jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas del hotel {hid}.")
        result = []
        for element in au_dict:
            result.append(self.dicBuild(element))
        return jsonify(result)



    def get_hotels_employee_can_access(self, eid):

        def dicBuild(row):
            a_dict = {'hid': row[0],
                      'chid': row[1],
                      'hname': row[2],
                      'hcity': row[3],
                      }
            return a_dict

        # Obtener la posición del empleado
        employee_info = self.getEmployeeById(eid)
        if not employee_info:
            return make_response(jsonify({"error": "Empleado no encontrado"}), 404)

        position = employee_info.json['position']

        employee_dao = EmployeeDAO()  # Instancia de HotelDAO
        hotel_dao = HotelDAO()

        # Lógica para determinar qué hoteles son accesibles basado en la posición
        if position == 'Regular':
            hid = self.getEmployeeById(eid).get_json()['hid']
            hotel = hotel_dao.getHotelById(hid)
            return make_response(jsonify([dicBuild(hotel)]),200) if hotel else make_response(jsonify(
                {"error": "No se encontró el hotel para el empleado regular"}), 404)
        elif position == 'Supervisor':
            hotels = employee_dao.getHotelsForSupervisor(eid)
            return make_response(jsonify([dicBuild(h) for h in hotels]), 200) if hotels else make_response(jsonify(
                {"error": "No se encontraron hoteles para el supervisor"}), 404)
        elif position == 'Administrator':
            # Suponiendo que un administrador puede acceder a todos los hoteles
            hotels = hotel_dao.getAllHotels()
            return jsonify([dicBuild(h) for h in hotels])
        else:
            return make_response(jsonify({"error": "Posición del empleado no reconocida"}), 400)