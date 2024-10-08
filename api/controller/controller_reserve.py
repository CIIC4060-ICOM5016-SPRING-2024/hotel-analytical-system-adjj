from ..model.model_reserve import ReserveDAO
from flask import jsonify, request, make_response

class ReserveController():
    def dicBuild(self, row):
        dict = {
            'reid':row[0],
            'ruid':row[1],
            'clid':row[2],
            'total_cost':row[3],
            'payment':row[4],
            'guests':row[5]
        }
        return dict
    
    def getAllReservations(self):
        dao = ReserveDAO()
        dict = dao.getAllReservations()
        result = []
        for element in dict:
            result.append(self.dicBuild(element))
        return jsonify(result)
    
    def getReservation(self,reid:int):
        dao = ReserveDAO()
        reservation = dao.getReservation(reid)

        if reservation:
            result = self.dicBuild(reservation)
            return jsonify(result)
        else:
            return make_response(jsonify({"error":"Reservation Not Found"}, 400))
        
    def addReservation(self):
        data = request.get_json()

        if not all(key in data for key in('ruid','clid','payment','guests','eid')):
            message = "Data to be sent was missing in the request json"
            id = None
            status = "error"
            return make_response(jsonify({"message":message, "id":id, "status":status}), 400)

        dao = ReserveDAO()

        id, message, status = dao.postReservation(data)
        json = jsonify({"message":message, "id":id, "status":status})
        if id:
            return make_response(json,201)
        else:
            return make_response(json,500)
        

    def deleteReservation(self, id:int):
        dao = ReserveDAO()
        success, message = dao.deleteReservation(id)
        if success:
            return make_response(jsonify({"message":message, "status":"success"}),200)
        else:
            return make_response(jsonify({"message":message, "status":"error"},500))

    def putReservation(self, id: int):
        data = request.get_json()

        if not all(key in data for key in ('ruid', 'clid', 'total_cost', 'payment', 'guests')):
            return make_response(jsonify({"error": "Missing Values"}), 400)

        dao = ReserveDAO()

        success = dao.putReservation(id,data)
        if success:
            return make_response(jsonify({"message": "Reservation Updated"}), 200)
        else:
            return make_response(jsonify({"error": "Error updating reservation"}, 500))

    def getReserveByPayMethod(self):
        def make_json1(row):
            dic = {
                'payment': row[0],
                'num_reservations_pay_method': row[1],
                'percentage_reservations_pay_method': row[2]
            }
            return dic
        data = request.get_json()
        required_fields = ['eid']

        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)
        dao = ReserveDAO()
        dic = dao.getReserveByPayMethod(data["eid"])
        if dic == None:
            return make_response(jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas."))
        result = []
        for element in dic:
            result.append(make_json1(element))
        return jsonify(result)
    
    def getTop3RoomsLeastGuestCapacity(self,hid):
        def json(row):
            dic={
                'rid':row[0],
                'rname':row[1],
                'avg_guest_to_capacity_ratio':row[2]
            }
            return dic
        data = request.get_json()
        required_fields = ['eid']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)
        dao = ReserveDAO()
        dic = dao.getTop3RoomsLeastCapacityRatio(data["eid"],hid)
        if dic == None:
            return make_response(jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas. (Found in Controller)"))
        result = []
        for element in dic:
            result.append(json(element))
        return jsonify(result)

        
