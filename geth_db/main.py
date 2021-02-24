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

    account, password = node.get_first_account()
    node.w3.geth.personal.unlock_account(account, password)
    return node, account, password


def run_child_node():
    node = Node(datadir=datadir, genesis_file="/home/matus/Desktop/Uni/genesis.json")
    enode = "enode://a0b3e17e95f377525b41009208fa32b2e45b5bfe6b20028ea7f027038ebc24abe3edf31924d079232a986fa22f63ae76b6ac58970da59aba014cda5044dc6644@192.168.0.73:30303?discport=0"

    # Start node
    node.start_node()
    node.w3.geth.admin.add_peer(enode)
    node.add_foreign_account(name="UTC--2021-02-24T07-12-41.183318900Z--41fb9a736bf45288b6cef59d3863f1e836954aaf",
                             key="/home/matus/Desktop/Uni/UTC--2021-02-24T07-12-41.183318900Z--41fb9a736bf45288b6cef59d3863f1e836954aaf")

    password = "6798e3fca05bc61d0c74a3186bd90f2d75586c65cfe99f8fc678cbb1f22a4567"
    account = "0x41fb9a736bf45288B6Cef59d3863F1e836954AAF"
    r = node.w3.geth.personal.unlock_account(account, password)
    print("UNLOCK ACCOUNT: {}".format(r))
    print("PEER COUNT: {}".format(node.w3.net.peerCount))

    return node, account, password


if __name__ == "__main__":
    num = input("Is this the 1 node or 2 node?")

    if num == "1":
        datadir = "C:\\Users\\matus\\Desktop\\Uni\\node01"
        os.system("rm -rf \"{}\"".format(datadir))  # debug purposes
        node, account, password = run_parent_node()
    else:
        datadir = "/home/matus/Desktop/node01"
        os.system("rm -rf \"{}\"".format(datadir))  # debug purposes
        node, account, password = run_child_node()
    node.configure_truffle()
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
        except Exception as e:
            print(e)
            node.stop_node()
    else:
        input("Enter to map contract")
        guid_db_contract = CI.get_contract_from_source(source="C:\\Users\\matus\\Desktop\\Uni\\GUID_mapping.json")
    app.run(port=5002)
