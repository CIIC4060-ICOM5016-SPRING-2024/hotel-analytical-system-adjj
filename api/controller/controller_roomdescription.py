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
        if request.method == 'POST':
            # Obtener datos del cuerpo de la petición
            data = request.get_json()
            # Validar que todos los campos necesarios están presentes
            if not all(key in data for key in ('rname', 'rtype', 'capacity', 'ishandicap')):
                return make_response(jsonify({"error": "Faltan datos"}), 400)

            # Crear una instancia de ClientDAO
            dao = RoomDescriptionDAO()
            # Llamar al método para insertar el nuevo empleado

            success, message = dao.postRoomDescription(data['rname'], data['rtype'], data['capacity'], data['ishandicap'])

            if success:
                return make_response(jsonify({"message": f"Room description agregada exitosamente"}), 201)
            else:
                return make_response(jsonify({"error": f"Error al agregar room description"}), 500)