import json
import os
import time

from flask import Flask, request
from flask_cors import CORS
from python_geth.contract_interface import ContractInterface
from python_geth.node import Node
from web3 import Web3

from db.db_util import getByGUID, createOrUpdate

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
    enode = "enode://20ab04b6abe745b103aa2d366889b55d747b78edf7265cbd1dd17c83cd9428ddb26fa721e27d113f3c09e16931711f343c98535ddf28aae3d3e931744dfabcb8@127.0.0.1:30303?discport=0"

    # Start node
    node.start_node()
    node.w3.geth.admin.add_peer(enode)

    name = "UTC--2021-02-24T09-46-48.819455600Z--e5d1d5eac3b806f817c6abc5cf8cb2bb86502d8f"
    key = "/home/matus/Desktop/Uni/{}".format(name)
    account = "0xe5D1D5eAC3B806F817C6abc5cF8cB2Bb86502D8F"
    password = "2e847a7039d88c8770cbfb62bb0e73e54f7c775f1434552dde7a4ec66692ed48"
    node.add_foreign_account(name=name, key=key, password=password)
    r = node.w3.geth.personal.unlock_account(account, password)
    print("PEER COUNT: {}".format(node.w3.net.peerCount))
    print("UNLOCK ACCOUNT: {}".format(r))

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
