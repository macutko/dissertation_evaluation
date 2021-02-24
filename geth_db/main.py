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
    enode = "enode://8b117fff23a7a7b30e49a7d8cbfad5e679028b3dd59de52c4ba5318dadcfbee40f1655a4c5862952b25e2237acc4da492d34cb5976b833d4b0efaf50afae0395@192.168.0.73:30303?discport=0"

    password = "aeb5e03adaf8445dcd143c4b1f690403b36d7d8c3ac20f593340b0ac7fb96109"

    # Start node
    node.start_node()
    node.w3.geth.admin.add_peer(enode)
    node.add_foreign_account(name="UTC--2021-02-24T06-26-10.258253600Z--f03c4a7f7dd7f2edbc1c8773ecc16cbedca96d85",
                             key="/home/matus/Desktop/Uni/UTC--2021-02-24T06-26-10.258253600Z--f03c4a7f7dd7f2edbc1c8773ecc16cbedca96d85")

    # need a dummy account to start syncing
    account = node.w3.geth.personal.new_account(password)
    node.w3.geth.personal.unlock_account(account, password)

    print("PEER COUNT: {}".format(node.w3.net.peerCount))

    account = "0xF03c4A7f7dD7F2eDbc1c8773ECC16CBeDCa96d85"
    r = node.w3.geth.personal.unlock_account(account, password)
    print("UNLOCK ACCOUNT: {}".format(r))

    return node, account, password


if __name__ == "__main__":
    num = input("Is this the 1 node or 2 node?")


    if num == "1":
        node, account, password = run_parent_node()
        datadir = "/home/matus/Desktop/node01"
        os.system("rm -rf \"{}\"".format(datadir))  # debug purposes
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

    app.run(port=5002)
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
        path = input("Please give me the path to contract")
        guid_db_contract = CI.get_contract_from_source(source=path)
        print("calling get")
        guid_db_contract.functions.get_studentSubjectAmount("2265072g").call()
        print("calling add")
        guid_db_contract.functions.add_grade("2265072g", "PSI", "A1").call()
        print("calling get")
        guid_db_contract.functions.get_studentSubjectAmount("2265072g").call()
