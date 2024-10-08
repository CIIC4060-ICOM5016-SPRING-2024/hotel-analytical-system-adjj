from api.model.model_chain import ChainsDAO
from flask import jsonify, request, make_response
import json


class ChainsContoller:

    def dicBuild(self, row):
        a_dict = {'chid':row[0],
                  'cname':row[1],
                  'springmkup':row[2],
                  'summermkup':row[3],
                  'fallmkup':row[4],
                  'wintermkup':row[5]
                  }
        return a_dict

    def getAllChains(self):
        dao = ChainsDAO()
        au_dict = dao.getAllChains()
        result = []
        for element in au_dict:
            result.append(self.dicBuild(element))
        return jsonify(result)
    
    def getChain(self,id:int):
        dao = ChainsDAO()
        chain = dao.getChain(id)

        # employee = dao.getClientById(id)  # Esto ahora espera una sola fila o None
        if chain:
            # Ya que esperamos un único resultado, no hay necesidad de iterar
            result = self.dicBuild(chain)
            return jsonify(result)
        else:
            # Manejar el caso en que no se encuentre el hotel
            return make_response(jsonify({"error": f"No se encontró el chain con ID {id}"}), 404)
    
    def addChain(self):
        data = request.get_json()
        
        if not all(key in data for key in ('cname', 'springmkup','summermkup','fallmkup','wintermkup')):
            message = "Data to be sent was missing in the request json"
            id = None
            status = "error"
            return make_response(jsonify({"message": message, "id": id, "status": status}), 400)

        dao = ChainsDAO()

        id, message, status = dao.postChain(data)
        json = jsonify({"message": message, "id": id, "status":status})
        if id:
            return make_response(json, 201)
        else:
            return make_response(json, 500)

    def deleteChain(self,id:int):
        dao = ChainsDAO()
        success, message = dao.deleteChain(id)
        if success:
            return make_response(jsonify({"message": message, "status":"success"}), 200)
        else:
            return make_response(jsonify({"message": message, "status":"error"}), 500)

    def putChain(self,id:int):
        dao = ChainsDAO()
        data = request.get_json()

        if not all(key in data for key in ('cname', 'springmkup','summermkup','fallmkup','wintermkup')):
            return make_response(jsonify({"error": "Missing Values"}), 400)
        
        success = dao.putChain(id=id, updated_chain=data)
        if success:
            return make_response(jsonify({"message":"Chain updated successfully"},200))
        else:
            return make_response(jsonify({"error":"Error updating chain"},500))

    def getTop3ProfitMonthsByChain(self):
        def make_json1(row):
            dic = {
                'chid': row[0],
                'month': row[1],
                'count_reservation': row[2]
            }
            return dic
        data = request.get_json()
        required_fields = ['eid']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)
        dao = ChainsDAO()
        dic = dao.getTop3ProfitMonthsByChain(data["eid"])
        if dic == None:
            return make_response(jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas."))
        result = []
        for element in dic:
            result.append(make_json1(element))
        return jsonify(result)

    def get_least_rooms_chains(self):

        def dict_build(row):
            return {
                'chain_id': row[0],
                'chain_name': row[1],
                'room_count': row[2]
            }

        data = request.get_json()
        # Validar que todos los campos necesarios están presentes
        required_fields = ['eid']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)

        dao = ChainsDAO()
        au_dict = dao.get_top_3_chains_with_least_rooms(data['eid'])
        if au_dict is None:
            return jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas globales.")
        result = []
        for chain in au_dict:
            result.append(dict_build(chain))
        return jsonify(result)
    def get_highest_revenue_chains(self):

        def dict_build(row):
            return {
                'chain_id': row[0],
                'chain_name': row[1],
                'total_revenue': row[2]
            }

        data = request.get_json()
        # Validar que todos los campos necesarios están presentes
        required_fields = ['eid']
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Faltan datos"}), 400)

        dao = ChainsDAO()
        au_dict = dao.get_top_3_chains_with_highest_revenue(data['eid'])
        if au_dict is None:
            return jsonify(f"El empleado {data['eid']} no tiene acceso a las estadísticas globales.")
        result = []
        for chain in au_dict:
            result.append(dict_build(chain))
        return jsonify(result)


