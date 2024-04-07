from api.model.model_room import RoomDAO
from flask import jsonify, request, make_response

class RoomController:
    def __init__(self):
        self.dao = RoomDAO()

    def make_json(self, tuples):
        return [{'rid': t[0], 'hid': t[1], 'rdid': t[2], 'rprice': t[3]} for t in tuples]

    def getAllRooms(self):
        result = self.dao.getAllRooms()
        answer = self.make_json(result)
        return jsonify(answer)

    def getRoomById(self, rid):
        room = self.dao.getRoomById(rid)
        if not room:
            return make_response(jsonify({"error": f"No se encuentra la habitacion con id {rid}"}), 404)
        return jsonify(self.make_json([room])[0])

    def postRoom(self):
        data = request.get_json()
        if not all(key in data for key in ('hid', 'rdid', 'rprice')):
            return make_response(jsonify({"error": "Faltan datos"}), 400)
        try:
            # Assuming data validation and conversion (if necessary) are done here
            success, message = self.dao.postRoom(data['hid'], data['rdid'], data['rprice'])
            return make_response(jsonify({"message": message}), 201)
        except Exception as e:
            return make_response(jsonify({"error": "Error al agregar habitacion"}), 500)

    def deleteRoom(self, rid):
        try:
            success, message = self.dao.deleteRoom(rid)
            return make_response(jsonify({"message": message}), 200)
        except Exception as e:
            return make_response(jsonify({"error": "Error al eliminar habitacion"}), 500)

    def putRoom(self, rid):
        data = request.get_json()
        if not all(field in data for field in ['hid', 'rdid', 'rprice']):
            return make_response(jsonify({"error": "Faltan datos"}), 400)
        try:
            success, message = self.dao.putRoom(rid, data['hid'], data['rdid'], data['rprice'])
            if success:
                return make_response(jsonify({"message": message}), 200)
            return make_response(jsonify({"error": message}), 400)
        except Exception as e:
            return make_response(jsonify({"error": f"Error al actualizar habitacion: {e}"}), 500)

    def getTop5HandicapReservedRooms(self, hid):
        data = request.get_json()
        # Validar que todos los campos necesarios están presentes
        required_fields = ['eid']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)

        # Assuming you have a RoomDAO or similar for handling room-related queries
        dao = RoomDAO()
        reservations_dict = dao.getTop5HandicapReserved(hid, data['eid'])
        if reservations_dict is None:
            return jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas del hotel {hid}.")

        result = []
        for reservation in reservations_dict:
            # Assuming you have a method to build a dictionary from each reservation tuple
            result.append(self.make_json(reservation))
        return jsonify(result)