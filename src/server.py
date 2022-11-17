from flask import Flask
from flask_cors import CORS,cross_origin
from flask_restful import Api
from json import dumps
from flask_jsonpify import jsonify
from controllers.solve_epidemiological_models import *
from controllers.parameter_estimation import *
from controllers.uploadFile import *

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources=r'/api/*')

@app.route("/api/")
def home():
    return jsonify({'text':'Wellcome to EaglePro!!'})


api.add_resource(SolveEpidemiologicalModels, '/api/SolveEpidemiologicalModels')
api.add_resource(ParameterEstimation, '/api/ParameterEstimation')
api.add_resource(Upload,'/api/UploadFile')


if __name__ == '__main__':
   app.run(port=8000)