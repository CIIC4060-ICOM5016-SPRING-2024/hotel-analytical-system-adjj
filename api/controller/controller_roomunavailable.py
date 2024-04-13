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
        if not all(key in data for key in ('eid', 'rid', 'startdate', 'enddate')):
            message = "Data to be sent was missing in the request json"
            id = None
            status = "error"
            return make_response(jsonify({"message": message, "id": id, "status": status}), 400)

        # Se pasa el eid al método postRoomUnavailable
        id, message, status = self.dao.postRoomUnavailable(data['eid'], data['rid'], data['startdate'],data['enddate'])
        json = jsonify({"message": message, "id":id, "status":status})
        if id:
            return make_response(json, 201)
        else:
            # Manejo del caso donde el empleado no tiene autorización o hay otro error
            return make_response(json), 403 if message == "El empleado no tiene autorización" else 500




    def deleteRoomUnavailable(self, ruid):
        roomunavailable = self.dao.getRoomUnavailableById(ruid)
        if roomunavailable is None:
            return make_response(jsonify({"message": f"The unavailable room with id {ruid} is not found", "status":"error"}),
                                 404)
        try:
            success, message = self.dao.deleteRoomUnavailable(ruid)
            return make_response(jsonify({"message": message, "status":"success"}), 200)
        except Exception as e:
            return make_response(jsonify({"message": "Error when deleting unavailable room", "status":"error"}), 500)

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

    def getTop3LeastUnavailable(self, hid):
        def make_json1(row):
            dic = {
                'hid': row[0],
                'rid': row[1],
                'reserved days': row[2]
            }
            return dic
        data = request.get_json()
        required_fields = ['eid']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)
        dic = self.dao.getTop3LeastUnavailable(hid, data["eid"])
        if dic == None:
            return make_response(jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas del hotel {hid}."))
        result =[]
        for element in dic:
            result.append(make_json1(element))
        return jsonify(result)
