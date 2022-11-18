from flask_restful import Resource
from flask import request
from services.solve_epidemiological_models_service import*
import json
import base64

class SolveEpidemiologicalModels(Resource):
    def __init__(self) -> None:
        res = request.get_json()
        print(res)
        self.s = SolveEpidemiologicalModelsService(str(res['model_name']),
                                                   list(res['vars_initials']),
                                                   list(res['params']),
                                                   list(res['params_est']),
                                                   int(res['t']),
                                                   int(res['total_points']),
                                                   str(res['method']), int(res['N']))
    
    def post(self):
        sol = self.s.solve_model()

        with open("model.png", "rb") as img_file:
            b64_string = base64.b64encode(img_file.read())
            print(b64_string)
        
        import os
        os.remove("model.png")

        return json.dumps({'sol': sol, 'img': str(b64_string)[2:-1]})
        

    