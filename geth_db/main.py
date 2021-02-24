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
    enode = "enode://76a12d679a699b0a7d13547d8dfea80a5b0deb162b4d05611f3a074aceeca439687d76da8458ede6cd22c407f31ff6fd4791e069c60818041ad4f6432cd62228@192.168.0.73:30303?discport=0"

    password = "0a9730c09dc2886c1a59da5c1ef58748d7497703559283134a771f6337635047"

    # Start node
    node.start_node()
    node.w3.geth.admin.add_peer(enode)
    node.add_foreign_account(name="UTC--2021-02-24T07-02-49.041752700Z--e8cc113e71fd3ea105566195e1699dca00c3a7a7",
                             key="/home/matus/Desktop/Uni/UTC--2021-02-24T07-02-49.041752700Z--e8cc113e71fd3ea105566195e1699dca00c3a7a7")

    # need a dummy account to start syncing
    account = node.w3.geth.personal.new_account(password)
    node.w3.geth.personal.unlock_account(account, password)

    print("PEER COUNT: {}".format(node.w3.net.peerCount))

    account = "0xE8cc113E71Fd3eA105566195E1699DcA00c3a7A7"
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

    if num == "2":
        print("deploying")
        try:
            guid_db_contract = CI.deploy_contract(
                contract_file="/home/matus/Desktop/Uni/dissertation_evaluation/geth_db/db/GUID_db"
                              ".sol")[0]

            print("calling get")
            guid_db_contract.functions.get_studentSubjectAmount("2265072g").call()
            print("calling add")
            guid_db_contract.functions.add_grade("2265072g", "PSI", "A1").call()
            print("calling get")
            guid_db_contract.functions.get_studentSubjectAmount("2265072g").call()

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
    app.run(port=5002)
