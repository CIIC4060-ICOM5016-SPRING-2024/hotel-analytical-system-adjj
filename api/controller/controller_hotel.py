
from api.model.model_hotel import HotelDAO
from flask import jsonify, request, make_response

class HotelContoller:

    def dicBuild(self, row):
        a_dict = {'hid':row[0],
                  'chid':row[1],
                  'hname':row[2],
                  'hcity':row[3],
                  }
        return a_dict

    def getAllHotels(self):
        dao = HotelDAO()
        au_dict = dao.getAllHotels()
        result = []
        for element in au_dict:
            result.append(self.dicBuild(element))
        return jsonify(result)

    def addHotel(self):
        if request.method == 'POST':
            # Obtener datos del cuerpo de la petición
            data = request.get_json()
            # Validar que todos los campos necesarios están presentes
            if not all(key in data for key in ('chid', 'hname', 'hcity')):
                return make_response(jsonify({"error": "Faltan datos"}), 400)

            # Crear una instancia de ClientDAO
            dao = HotelDAO()
            # Llamar al método para insertar el nuevo empleado
            success, message = dao.postHotel(data['chid'], data['hname'], data['hcity'])

            if success:
                return make_response(jsonify({"message": f"Hotel agregado exitosamente"}), 201)
            else:
                return make_response(jsonify({"error": f"Error al agregar hotel"}), 500)