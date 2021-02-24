import json
import os
import time

from flask import Flask, request
from flask_cors import CORS
from python_geth.contract_interface import ContractInterface

from web3 import Web3

from db.db_util import get_by_guid, create_or_update, run_parent_node, run_child_node

app = Flask(__name__)
CORS(app)


@app.route('/get', methods=['GET'])
def get():
    guid = request.args.get('GUID')
    start_time = time.time()

    node.w3.geth.personal.unlock_account(account, password)

    res = get_by_guid(guid, guid_db_contract)
    res = json.loads(Web3.toJSON(res))
    res.update({'time': (time.time() - start_time)})
    return json.dumps(res)


@app.route('/create', methods=['POST'])
def create():
    guid = request.get_json()['GUID']
    subject = request.get_json()['subject']
    grade = request.get_json()['grade']
    start_time = time.time()

    print('ACCOUTN UNLOK: {}'.format(node.w3.geth.personal.unlock_account(account, password)))
    print(account)
    print(password)

    res = create_or_update(guid, subject, grade, guid_db_contract, node.w3, account)
    res = json.loads(Web3.toJSON(res))
    return json.dumps({'tx': res, 'time': (time.time() - start_time)})


@app.route('/update', methods=['PUT'])
def update():
    guid = request.get_json()['GUID']
    subject = request.get_json()['subject']
    grade = request.get_json()['grade']
    start_time = time.time()

    node.w3.geth.personal.unlock_account(account, password)

    res = create_or_update(guid, subject, grade, guid_db_contract, node.w3, account)
    res = json.loads(Web3.toJSON(res))
    return json.dumps({'tx': res, 'time': (time.time() - start_time)})


if __name__ == "__main__":
    num = input("If this is single node press 3\n If this is 1st node of double press 1, otherwise press 2")

    if os.name == 'nt':
        datadir = "C:\\Users\\matus\\Desktop\\Uni\\node01"
    else:
        datadir = "/home/matus/Desktop/node01"

    os.system("rm -rf \"{}\"".format(datadir))  # debug purposes

    if num == "1" or num == "3":
        node, account, password = run_parent_node(datadir)
    else:
        node, account, password = run_child_node(datadir)

    node.configure_truffle()

    input("To start mining hit enter")
    node.w3.geth.miner.start(1)

    guid_db_contract = None
    CI = ContractInterface(w3=node.w3,
                           datadir=datadir)

    if num == "2" or num == '3':
        print("deploying")
        try:
            guid_db_contract = CI.deploy_contract(
                contract_file="/home/matus/Desktop/Uni/dissertation_evaluation/geth_db/db/GUID_db"
                              ".sol")[0]
        except Exception as e:
            print(e)
            node.stop_node()
    else:
        input("Enter to map contract")
        guid_db_contract = CI.get_contract_from_source(source="C:\\Users\\matus\\Desktop\\Uni\\GUID_mapping.json")
    app.run(port=5002)
