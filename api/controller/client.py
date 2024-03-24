from model.client import ClientDAO
from flask import jsonify

class ClientContoller:

    def dicBuild(self, row):
        a_dict = {'clid':row[0],
                  'fname':row[1],
                  'lname':row[2],
                  'age':row[3],
                  'memberyear':row[4]
                  }
        return a_dict

    def getAllClients(self):
        dao = ClientDAO()
        au_dict = dao.getAllClients()
        result = []
        for element in au_dict:
            result.append(self.dicBuild(element))
        return jsonify(result)