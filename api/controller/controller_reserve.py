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

        if not all(key in data for key in('ruid','clid','total_cost','payment','guests','eid')):
            return make_response(jsonify({"error": "Missing Values"}), 400)

        dao = ReserveDAO()

        success = dao.postReservation(data)
        if success:
            return make_response(jsonify({"message":"Reservation Added"}),200)
        else:
            return make_response(jsonify({"error":"Error adding reservation"},500))
        

    def deleteReservation(self, id:int):
        dao = ReserveDAO()
        success = dao.deleteReservation(id)
        if success:
            return make_response(jsonify({"message":"Reservation Deleted "},200))
        else:
            return make_response(jsonify({"error":"Error deleting reservation"},500))
        
    def putReservation(self, id:int):
        data = request.get_json()

        if not all(key in data for key in('ruid','clid','total_cost','payment','guests')):
            return make_response(jsonify({"error": "Missing Values"}), 400)
        
        dao = ReserveDAO()

        success = dao.putReservation(data)
        if success:
            return make_response(jsonify({"message":"Reservation Updated"}),200)
        else:
            return make_response(jsonify({"error":"Error updating reservation"},500))


