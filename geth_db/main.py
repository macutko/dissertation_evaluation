import json
import os
import time

from flask import Flask, request
from flask_cors import CORS
from python_geth.contract_interface import ContractInterface
from python_geth.node import Node
from web3 import Web3

from db.db_test import getByGUID, createOrUpdate

app = Flask(__name__)
CORS(app)


@app.route('/get', methods=['GET'])
def get():
    guid = request.args.get('GUID')
    start_time = time.time()

    node.w3.geth.personal.unlock_account(account, password)

    res = getByGUID(guid, guid_db_contract)
    res = json.loads(Web3.toJSON(res))
    res.update({'time': (time.time() - start_time)})
    return json.dumps(res)


@app.route('/create', methods=['POST'])
def create():
    guid = request.get_json()['GUID']
    subject = request.get_json()['subject']
    grade = request.get_json()['grade']
    start_time = time.time()

    node.w3.geth.personal.unlock_account(account, password)

    res = createOrUpdate(guid, subject, grade, guid_db_contract, node.w3)
    res = json.loads(Web3.toJSON(res))
    res.update({'time': (time.time() - start_time)})
    return json.dumps(res)


@app.route('/update', methods=['PUT'])
def update():
    guid = request.get_json()['GUID']
    subject = request.get_json()['subject']
    grade = request.get_json()['grade']
    start_time = time.time()

    node.w3.geth.personal.unlock_account(account, password)

    res = createOrUpdate(guid, subject, grade, guid_db_contract, node.w3)
    res = json.loads(Web3.toJSON(res))
    res.update({'time': (time.time() - start_time)})
    return json.dumps(res)


def run_parent_node():
    node = Node(datadir=datadir, port=30303,
                rpcport=8000, name="Node01")
    node.start_node()

    node.configure_truffle()
    account, password = node.get_first_account()
    node.w3.geth.personal.unlock_account(account, password)
    return node, account, password


def run_child_node():
    node = Node(datadir=datadir, genesis_file="/home/matus/Desktop/Uni/genesis.json")
    enode = "enode://aee4b611831031f837bbf059e770fcaa10e3823ecded04e6c5faada5d64ba4fd3009eface6e7b6ea475e0e186bd6798e66da5e18dcc2d75956eb3abbf5820ae8@192.168.0.73:30303?discport=0"

    password = "d1c8e5d790703ffeee04ea173bc58ca2761aa2832a4b41dea3a9d6fe07e3c30c"

    # Start node
    node.start_node()
    node.w3.geth.admin.add_peer(enode)
    node.add_foreign_account(name="UTC--2021-02-24T06-01-26.904529800Z--146a331246f3fbd67f644d419b3582606625f777",
                             key="/home/matus/Desktop/Uni/UTC--2021-02-24T06-01-26.904529800Z--146a331246f3fbd67f644d419b3582606625f777")

    # need a dummy account to start syncing
    account = node.w3.geth.personal.new_account(password)
    node.w3.geth.personal.unlock_account(account, password)

    print("PEER COUNT: {}".format(node.w3.net.peerCount))

    account = "0x146a331246f3fBD67F644d419B3582606625F777"
    r = node.w3.geth.personal.unlock_account(account, password)
    print("UNLOCK ACCOUNT: {}".format(r))

    return node, account, password


if __name__ == "__main__":
    num = input("Is this the 1 node or 2 node?")
    datadir = "/home/matus/Desktop/node01"
    os.system("rm -rf \"{}\"".format(datadir))  # debug purposes

    if num == "1":
        node, account, password = run_parent_node()
    else:
        node, account, password = run_child_node()

    input("To start mining hit enter")
    node.w3.geth.miner.start(1)

    guid_db_contract = None
    CI = ContractInterface(w3=node.w3,
                           datadir=datadir)
    if num == "2":
        print("deploying")
        try:
            guid_db_contract = CI.deploy_contract(
                contract_file="/home/matus/Desktop/Uni/dissertation_evaluation/geth_db/db/GUID_db"
                              ".sol")[0]
        except:
            node.stop_node()
    else:
        path = input("Please give me the path to contract")
        guid_db_contract = CI.get_contract_from_source(source=path)
        guid_db_contract.functions.get_studentSubjectAmount("2265072g").call()
        guid_db_contract.functions.add_grade("2265072g", "PSI", "A1").call()
        guid_db_contract.functions.get_studentSubjectAmount("2265072g").call()

    app.run(port=5002)
