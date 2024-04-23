from api.model.model_all import AllDAO
from flask import jsonify, request, make_response
import json

class AllController:
    def tablesBuild(self, row):
        a_dict = {'table_name':row[0]}
        return a_dict
    def columnBuild(self, row):
        a_dict = {'column_name':row[0]}
        return a_dict
    def keyBuild(self, row):
        a_dict = {'attname':row[0]}
        return a_dict
    def getAllTables(self):
        dao = AllDAO()
        a_dict = dao.getAllTables()
        result = []
        for element in a_dict:
            result.append(self.tablesBuild(element))
        return jsonify(result)
    def getColumnNames(self,table):
        dao = AllDAO()
        a_dict = dao.getColumnNames(table)
        result=[]
        for element in a_dict:
            result.append(self.columnBuild(element))
        return jsonify(result)
    def getPrimaryKey(self,table):
        dao = AllDAO()
        a_dict = dao.getPrimaryKey(table)
        result=[]
        for element in a_dict:
            result.append(self.keyBuild(element))
        return jsonify(result)
        



    