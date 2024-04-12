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
            message = "Data to be sent was missing in the request json"
            id = None
            status = "error"
            return make_response(jsonify({"message": message, "id": id, "status": status}), 400)

        # Assuming data validation and conversion (if necessary) are done here
        id, message, status = self.dao.postRoom(data['hid'], data['rdid'], data['rprice'])
        json = jsonify({"message": message, "id": id, "status":status})
        if id:
            return make_response(json, 201)
        else:
            return make_response(json, 500)

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


    def get_top_5_handicap_reserved(self, hid):
        def make_json1(row):
            dic = {
                'room_id': row[0],
                'room_name': row[1],
                'room_type': row[2],
                'reservation_count': row[3]
            }
            return dic
        data = request.get_json()
        required_fields = ['eid']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)
        dic = self.dao.get_top_5_handicap_reserved(hid, data["eid"])
        if dic == None:
            return make_response(jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas del hotel {hid}."))
        result =[]
        for element in dic:
            result.append(make_json1(element))
        return jsonify(result)