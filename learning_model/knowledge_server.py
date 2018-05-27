import json

from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


@app.route('/ask', methods=['GET'])
def get_knowledge():
    if request.method == 'GET':
        if len(request.data) == 0:
            return "1"
        data = json.loads(request.data)
        if len(data) > 0:
            length = len(data["maps"])
            response = jsonify([1.0/length]*length)
            return response
        else:
            return "1"


@app.route('/tell', methods=['POST'])
def post_knowledge():
    return 'Hello, World!'
