from model.model_reserve import ReserveDAO
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
        


