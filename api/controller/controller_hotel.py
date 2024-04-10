
from api.model.model_hotel import HotelDAO
from flask import jsonify, request, make_response

class HotelContoller:

    def dicBuild(self, row):
        a_dict = {'hid':row[0],
                  'chid':row[1],
                  'hname':row[2],
                  'hcity':row[3],
                  }
        return a_dict

    def getAllHotels(self):
        dao = HotelDAO()
        au_dict = dao.getAllHotels()
        result = []
        for element in au_dict:
            result.append(self.dicBuild(element))
        return jsonify(result)

    def getHotelById(self,hid):
        dao = HotelDAO()
        hotel = dao.getHotelById(hid)  # Esto ahora espera una sola fila o None
        if hotel:
            # Ya que esperamos un único resultado, no hay necesidad de iterar
            result = self.dicBuild(hotel)
            return jsonify(result)
        else:
            # Manejar el caso en que no se encuentre el hotel
            return make_response(jsonify({"error": f"No se encontró el hotel con ID {hid}"}), 404)

    def addHotel(self):
        if request.method == 'POST':
            # Obtener datos del cuerpo de la petición
            data = request.get_json()
            # Validar que todos los campos necesarios están presentes
            if not all(key in data for key in ('chid', 'hname', 'hcity')):
                return make_response(jsonify({"error": "Faltan datos"}), 400)

            # Crear una instancia de ClientDAO
            dao = HotelDAO()
            # Llamar al método para insertar el nuevo empleado
            success, message = dao.postHotel(data['chid'], data['hname'], data['hcity'])

            if success:
                return make_response(jsonify({"message": f"Hotel agregado exitosamente", "hid":success}), 201)
            else:
                return make_response(jsonify({"error": f"Error al agregar hotel"}), 500)

    def deleteHotel(self, hid):
        dao = HotelDAO()
        success = dao.deleteHotel(hid)
        if success:
            return make_response(jsonify({"message": "Hotel eliminado exitosamente"}), 200)
        else:
            return make_response(jsonify({"error": "Error al eliminar hotel"}), 500)

    def putHotel(self, hid):
        if request.method == 'PUT':
            # Obtener los datos actualizados del cuerpo de la petición
            data = request.get_json()
            # Validar que todos los campos necesarios están presentes
            required_fields = ['chid', 'hname', 'hcity']
            if not all(field in data for field in required_fields):
                return make_response(jsonify({"error": "Faltan datos"}), 400)

            # Crear una instancia de EmployeeDAO
            dao = HotelDAO()
            # Llamar al método para actualizar el empleado
            success = dao.putHotel(hid, data['chid'], data['hname'], data['hcity'])

            if success:
                return make_response(jsonify({"message": "Hotel actualizado exitosamente"}), 200)
            else:
                # Si no se pudo actualizar, podría ser debido a un eid inválido o problemas internos del servidor
                return make_response(jsonify({"error": "Error al actualizar hotel"}), 500)


    def get_most_reservations(self):

        def fict_build(row):
            # Ajusta los índices de acuerdo a lo que devuelve tu consulta específica
            a_dict = {
                'hid': row[0],
                'hname': row[1],
                'reservation_count': row[2]  # Asumiendo que este es el orden de los campos devueltos por tu consulta
            }
            return a_dict

        data = request.get_json()
        # Validar que todos los campos necesarios están presentes
        required_fields = ['eid']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)

        dao = HotelDAO()
        au_dict = dao.get_most_reservations(data['eid'])
        if au_dict == None:
            return jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas globales.")
        result = []
        for element in au_dict:
            result.append(fict_build(element))
        return jsonify(result)


    def get_most_capacity(self):

        def fict_build(row):
            # Ajusta los índices de acuerdo a lo que devuelve tu consulta específica
            a_dict = {
                'hid': row[0],
                'hname': row[1],
                'total_capacity': row[2]  # Asumiendo que este es el orden de los campos devueltos por tu consulta
            }
            return a_dict

        data = request.get_json()
        # Validar que todos los campos necesarios están presentes
        required_fields = ['eid']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)

        dao = HotelDAO()
        au_dict = dao.get_most_capacity(data['eid'])
        if au_dict == None:
            return jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas globales.")
        result = []
        for element in au_dict:
            result.append(fict_build(element))
        return jsonify(result)

    def get_total_reservations_by_room_type(self,hid):
        def fict_build(row):
            dict = {
                "rtype":row[0],
                "total_reservations":row[1]
            }
            return dict
        data = request.get_json()

        dao = HotelDAO()

        required_fields = ['eid']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)

        result_dict = dao.get_total_reservation_by_room_type(hid,data['eid'])
        if result_dict == None:
            return make_response(jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas del hotel {hid}."))
        result = []
        for element in result_dict:
            result.append(fict_build(element))
        return jsonify(result)


