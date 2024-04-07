from api.model.model_roomunivailable import RoomUnavailableDAO
from flask import jsonify, request, make_response
class RoomUnavailableController():
    def __init__(self):
        self.dao = RoomUnavailableDAO()

    def make_json(self,tuples):
        return [{'ruid': t[0], 'rid': t[1], 'startdate': t[2], 'enddate': t[3]} for t in tuples]

    def getAllRoomsUnavailable(self):
        result = self.dao.getAllRoomsUnavailable()
        answer = self.make_json(result)
        return jsonify(answer)

    def getRoomUnavailableById(self, ruid):
        roomunavailable = self.dao.getRoomUnavailableById(ruid)
        if roomunavailable is None:
            return make_response(jsonify({"error": f"La habitacion indisponible con el id {ruid} no se encuentra"}), 404)
        result = self.make_json([roomunavailable])
        return result[0]

    def postRoomUnavailable(self):
        data = request.get_json()
        if not all(key in data for key in ('rid', 'startdate', 'enddate')):
            return make_response(jsonify({"error": "Faltan datos"}), 400)
        try:
            success, message = self.dao.postRoomUnavailable(data['rid'], data['startdate'], data['enddate'])
            return make_response(jsonify({"message": message}), 201)
        except Exception as e:
            return make_response(jsonify({"error": "Error al agregar habitacion indisponible"}), 500)


    def deleteRoomUnavailable(self, ruid):
        roomunavailable = self.dao.getRoomUnavailableById(ruid)
        if roomunavailable is None:
            return make_response(jsonify({"error": f"La habitacion indisponible con el id {ruid} no se encuentra"}),
                                 404)
        try:
            success, message = self.dao.deleteRoomUnavailable(ruid)
            return make_response(jsonify({"message": message}), 200)
        except Exception as e:
            return make_response(jsonify({"error": "Error al eliminar habitacion indisponible"}), 500)

    def putRoomUnavailable(self, ruid):
        data = request.get_json()
        if not all(field in data for field in ['rid', 'startdate', 'enddate']):
            return make_response(jsonify({"error": "Faltan datos"}), 400)
        try:
            success, message = self.dao.putRoomUnavailable(ruid, data['rid'], data['startdate'], data['enddate'])
            if success:
                return make_response(jsonify({"message": message}), 200)
            return make_response(jsonify({"error": message}), 400)
        except Exception as e:
            return make_response(jsonify({"error": f"Error al actualizar habitacion indisponible: {e}"}), 500)
