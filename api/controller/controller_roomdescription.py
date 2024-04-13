from api.model.model_roomdescription import RoomDescriptionDAO
from flask import jsonify, request, make_response


class RoomDescriptionController():
    def dicBuild(self, row):
        a_dict = {'rdid': row[0],
                  'rname': row[1],
                  'rtype': row[2],
                  'capacity': row[3],
                  'ishandicap': row[4]
                  }
        return a_dict

    def getAllRoomDescriptions(self):
        dao = RoomDescriptionDAO()
        au_dict = dao.getAllRoomsDescriptions()
        result = []
        for element in au_dict:
            result.append(self.dicBuild(element))
        return jsonify(result)

    def getRoomsDescriptionById(self, rdid):
        dao = RoomDescriptionDAO()
        RoomsDescription = dao.getRoomsDescriptionById(rdid)
        if RoomsDescription:
            result = self.dicBuild(RoomsDescription)
            return jsonify(result)
        else:
            return make_response(jsonify({"error": f"No se encontró la descripcion del cuarto con ID {rdid}"}), 404)

    def addRoomDescription(self):
        # if request.method == 'POST':
            # Obtener datos del cuerpo de la petición
            data = request.get_json()
            # Validar que todos los campos necesarios están presentes
            if not all(key in data for key in ('rname', 'rtype', 'capacity', 'ishandicap')):
                message = "Data to be sent was missing in the request json"
                id = None
                status = "error"
                return make_response(jsonify({"message": message, "id": id, "status": status}), 400)

            # Crear una instancia de ClientDAO
            dao = RoomDescriptionDAO()
            # Llamar al método para insertar el nuevo empleado

            id, message, status = dao.postRoomDescription(data['rname'], data['rtype'], data['capacity'], data['ishandicap'])
            json = jsonify({"message": message, "id":id, "status":status})
            if id:
                return make_response(json, 201)
            else:
                return make_response(json, 500)



    def deleteRoomDescription(self, rdid):
        dao = RoomDescriptionDAO()
        success, message = dao.deleteRoomDescription(rdid)
        if success:
            return make_response(jsonify({"message": message, "status":"success"}), 200)
        else:
            return make_response(jsonify({"message": message, "status":"error"}), 500)


    def putRoomDescription(self, rdid):
        if request.method == 'PUT':
            # Obtener los datos actualizados del cuerpo de la petición
            data = request.get_json()
            # Validar que todos los campos necesarios están presentes
            required_fields = ['rname', 'rtype', 'capacity', 'ishandicap']
            if not all(field in data for field in required_fields):
                return make_response(jsonify({"error": "Faltan datos"}), 400)

            # Crear una instancia de EmployeeDAO
            dao = RoomDescriptionDAO()
            # Llamar al método para actualizar el empleado
            success = dao.putRoomDescription(rdid, data['rname'], data['rtype'], data['capacity'], data['ishandicap'])

            if success:
                return make_response(jsonify({"message": "Descripcion de habitacion actualizado exitosamente"}), 200)
            else:
                # Si no se pudo actualizar, podría ser debido a un eid inválido o problemas internos del servidor
                return make_response(jsonify({"error": "Error al actualizar Descripcion de habitacion"}), 500)

