import json

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "<h1 style='color:red'>Hello There!</h1>"


@app.route('/get', methods=['GET'])
def get():
    sound = request.get_json()['soundBits']
    return json.dumps({"text": "hey"}, indent=4)


@app.route('/create', methods=['POST'])
def create():
    sound = request.get_json()['soundBits']
    return json.dumps({"text": "hey"}, indent=4)


@app.route('/update', methods=['PUT'])
def update():
    sound = request.get_json()['soundBits']
    return json.dumps({"text": "hey"}, indent=4)


@app.route('/delete', methods=['DELETE'])
def delete():
    sound = request.get_json()['soundBits']
    return json.dumps({"text": "hey"}, indent=4)


if __name__ == "__main__":
    app.run(port=5002)
