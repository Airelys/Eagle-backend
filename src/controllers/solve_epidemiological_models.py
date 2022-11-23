from flask_restful import Resource
from flask import request
from services.solve_epidemiological_models_service import*
import json

class SolveEpidemiologicalModels(Resource):
    def __init__(self) -> None:
        res = request.get_json()
        print(res)
        self.s = SolveEpidemiologicalModelsService(str(res['model_name']),
                                                   list(res['vars_initials']),
                                                   list(res['params']),
                                                   list(res['params_est']),
                                                   int(res['t']),
                                                   str(res['method']), int(res['P']),bool(res['di']))
    
    def post(self):
        sol,imgs = self.s.solve_model()

        return json.dumps({'sol': sol, 'img': imgs})
        

    