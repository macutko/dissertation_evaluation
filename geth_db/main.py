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
    enode = "enode://f2c0ad6e407bfcfa8e93cba51c5de7aa14374845461b70c7ba76b4f91a7e14afc9293cbcaa79d16ba0db702fd44e9bfb8e002573dafda801534a69a4b357c348@192.168.0.73:30303?discport=0"

    password = "d6f0fc48d449c2f28bd9ffb6228a3cfc96cfae0bd98a0c5d4bc11875978ff398"

    # Start node
    node.start_node()
    node.w3.geth.admin.add_peer(enode)
    node.add_foreign_account(name="UTC--2021-02-24T05-21-26.252696300Z--cf7c9836521259c9ed75b35d53c199581219b0f3",
                             key="/home/matus/Desktop/Uni/UTC--2021-02-24T05-21-26.252696300Z--cf7c9836521259c9ed75b35d53c199581219b0f3")

    # need a dummy account to start syncing
    account = node.w3.geth.personal.new_account(password)
    node.w3.geth.personal.unlock_account(account, password)

    print("PEER COUNT: {}".format(node.w3.net.peerCount))

    account = "0xCF7C9836521259c9eD75B35d53c199581219B0f3"
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

    num = input("Can I start the miner?")
    if num == "1":
        print("starting")
        node.w3.geth.miner.start(1)
    else:
        exit(0)

    num = input("Can I deploy the contract?")

    guid_db_contract = None
    CI = ContractInterface(w3=node.w3,
                           datadir=datadir)
    if num == "1":
        print("deploying")
        try:
            guid_db_contract = CI.deploy_contract(
                contract_file="/home/matus/Desktop/Uni/dissertation_evaluation/geth_db/db/GUID_db"
                              ".sol")[0]
        except:
            node.stop_node()
    else:
        contract_addr = input("Is the contract deployed? gimme his address!")
        guid_db_contract = CI.get_contract_from_source(source="/home/matus/Desktop/Uni/GUID_mapping.json")
        guid_db_contract.functions.get_studentSubjectAmount("2265072g").call()
        guid_db_contract.functions.add_grade("2265072g", "PSI", "A1").call()
        guid_db_contract.functions.get_studentSubjectAmount("2265072g").call()

    if guid_db_contract is not None:
        print("Address:" + guid_db_contract.address)
        print(node.w3.eth.getCode(guid_db_contract.address))

    # print(guid_db_contract.functions.get_studentSubjectAmount("2265072g").call(
    #     {"from": node.w3.toChecksumAddress(account)}))
    app.run(port=5002)
