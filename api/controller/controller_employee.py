# from model.client import ClientDAO
from api.model.model_employee import EmployeeDAO
from flask import jsonify

class EmployeeContoller:


    def dicBuild(self, row):
        a_dict = {'eid':row[0],
                  'hid':row[1],
                  'fname':row[2],
                  'lname':row[3],
                  'age':row[4],
                  'salary':row[5],
                  'position':row[6]
                  }
        return a_dict

    def getAllEmployees(self):
        dao = EmployeeDAO()
        au_dict = dao.getAllEmployees()
        result = []
        for element in au_dict:
            result.append(self.dicBuild(element))
        return jsonify(result)