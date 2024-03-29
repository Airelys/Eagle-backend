import base64
from flask_restful import Resource
from flask import jsonify,send_file,request
from services.parameter_estimation_service import*
import json
from PIL import Image
from numpy import asarray

class ParameterEstimation(Resource):
    def __init__(self) -> None:
        res = request.get_json()
        print(res)
        self.s = ParameterEstimationService(str(res['model_name']),
                                            list(res['vars_initials']),
                                            list(res['params']),
                                            list(res['params_est']),
                                            int(res['t']),
                                            str(res['method']),
                                            int(res['P']),
                                            list(res['params_min']), 
                                            list(res['params_max']), 
                                            str(res['classical_method']), 
                                            str(res['metaheuristic']),
                                            int(res['iter']),
                                            int(res['particle']),
                                            float(res['cognitive']),
                                            float(res['social']),
                                            float(res['inercia']),
                                            int(res['population']),
                                            float(res['crossing']),
                                            float(res['scaled']),
                                            bool(res['di']))
    
    def post(self):
        opt,sol,imgs,fun = self.s.solve_model()
        
        return json.dumps({'opt': opt, 'sol': sol, 'img': imgs, 'fun': fun})