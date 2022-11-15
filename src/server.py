from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from json import dumps
from flask_jsonpify import jsonify
from controllers.solve_epidemiological_models import *
from controllers.parameter_estimation import *

app = Flask(__name__)
api = Api(app)

CORS(app)

@app.route("/")
def home():
    return jsonify({'text':'Wellcome to EaglePro!!'})

api.add_resource(SolveEpidemiologicalModels, '/SolveEpidemiologicalModels')
api.add_resource(ParameterEstimation, '/ParameterEstimation')


if __name__ == '__main__':
   app.run(port=8000)