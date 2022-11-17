from flask_restful import Resource
from flask import request
import json

class Upload(Resource):
    
    def post(file):
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)
        return json.dumps({'upload':"completed"})