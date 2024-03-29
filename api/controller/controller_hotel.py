
from api.model.model_hotel import HotelDAO
from flask import jsonify

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