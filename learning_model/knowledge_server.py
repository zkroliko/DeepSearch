import json

from flask import Flask
from flask import request
from flask import jsonify

from learning_model.value_model import ValueModel

app = Flask(__name__)

model = ValueModel()

@app.route('/ask', methods=['GET'])
def get_knowledge():
    if request.method == 'GET':
        if len(request.data) == 0:
            return "1"
        data = request.get_json()
        if len(data) > 0:
            response = model.value_maps(data)
            print(response)
            return response
        else:
            return "1"


@app.route('/tell', methods=['POST'])
def post_knowledge():
    return 'Hello, World!'
