# from model.client import ClientDAO
from api.model.model_chain import ChainsDAO

from flask import jsonify

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
        au_dict = dao.getChain(id)
        result=[]
        for element in au_dict:
            result.append(self.dicBuild(element))
        return jsonify(result)
    
    def postChain(self,new_chain:dict):
        dao = ChainsDAO()
        au_dict = dao.postChain(new_chain)
        result=[]
        for element in au_dict:
            result.append(self.dicBuild(element))
        return jsonify(result)
        
    
        
