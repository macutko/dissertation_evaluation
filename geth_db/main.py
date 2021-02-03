import json
import os

from flask import Flask, request
from flask_cors import CORS
from python_geth.contract_interface import ContractInterface
from python_geth.node import Node

from db.db_test import getByGUID, createOrUpdate

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "<h1 style='color:red'>Hello There!</h1>"


@app.route('/get', methods=['GET'])
def get():
    guid = request.get_json()['guid']
    return json.dumps(getByGUID(guid, guid_db_contract), indent=4)


@app.route('/create', methods=['POST'])
def create():
    guid = request.get_json()['guid']
    subject = request.get_json()['subject']
    grade = request.get_json()['grade']
    createOrUpdate(guid, subject, grade, guid_db_contract, CI)
    return json.dumps({"tx": createOrUpdate(guid, subject, grade, guid_db_contract, CI)}, indent=4)


@app.route('/update', methods=['PUT'])
def update():
    guid = request.get_json()['guid']
    subject = request.get_json()['subject']
    grade = request.get_json()['grade']
    createOrUpdate(guid, subject, grade, guid_db_contract, CI)
    return json.dumps({"tx": createOrUpdate(guid, subject, grade, guid_db_contract, CI)}, indent=4)


if __name__ == "__main__":
    app.run(port=5002)
    datadir = "C:\\Users\\matus\\Desktop\\Uni\\lvl_5\\disseration\\bin\\node01"
    os.system("rm -rf \"{}\"".format(datadir))  # debug purposes

    node1 = Node(datadir=datadir, port=30303,
                 rpcport=8000, name="Node01")
    node1.start_node()
    node1.w3.geth.miner.start(1)
    node1.configure_truffle()
    account, password = node1.get_first_account()
    node1.w3.geth.personal.unlock_account(account, password)
    CI = ContractInterface(w3=node1.w3,
                           datadir=datadir)
    try:
        guid_db_contract = CI.deploy_contract(
            contract_file="C:\\Users\\matus\\Desktop\\Uni\\lvl_5\\disseration\\dissertation_evaluation\\geth_db\\db\\GUID_db"
                          ".sol")[0]
    except:
        node1.stop_node()
