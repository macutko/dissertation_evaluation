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
    node.w3.geth.miner.start(1)
    node.configure_truffle()
    account, password = node.get_first_account()
    node.w3.geth.personal.unlock_account(account, password)
    CI = ContractInterface(w3=node.w3,
                           datadir=datadir)
    try:
        guid_db_contract = CI.deploy_contract(
            contract_file="/home/matus/Desktop/Uni/dissertation_evaluation/geth_db/db/GUID_db"
                          ".sol")[0]
        return guid_db_contract, node, account, password
    except:
        node.stop_node()
        return None, node, account, password


def run_child_node():
    node = Node(datadir=datadir, genesis_file="/home/matus/Desktop/Uni/genesis.json")
    enode = "enode://8bf847cc041d60c6103f06b8dd3d3bebc48689699c8763cf3db7ba2ac26d4c08f7df4fa122caf168dfd51fd5089813d7ab181c1ff915c434256491ee01ea117e@192.168.0.73:30303?discport=0"

    password = "3e12431c5eda9823afbfe5b1011aaa31c54ad4efe4ae68911fca2696a0a7ddf8"

    # Start node
    node.start_node()
    node.w3.geth.admin.add_peer(enode)
    # add parent node
    node.add_foreign_account(name="UTC--2021-02-19T11-15-19.419344900Z--953df1654446f34626b734d6e6ce5a0ba49309bd",
                             key="/home/matus/Desktop/Uni/UTC--2021-02-19T11-15-19.419344900Z--953df1654446f34626b734d6e6ce5a0ba49309bd")

    # need a dummy contract to start syncing
    account = node.w3.geth.personal.new_account(password)
    node.w3.geth.personal.unlock_account(account, password)

    print("PEER COUNT: {}".format(node.w3.net.peerCount))
    node.w3.geth.miner.start(1)

    account = "0x953dF1654446f34626b734d6e6CE5a0Ba49309bd"
    r = node.w3.geth.personal.unlock_account(account, password)
    print("UNLOCK ACCOUNT: {}".format(r))

    CI = ContractInterface(w3=node.w3,
                           datadir=datadir)

    guid_db_contract = CI.get_contract_from_source(source="/home/matus/Desktop/Uni/GUID_mapping.json")
    return guid_db_contract, node, account, password


# guid_db_contract.functions.get_studentSubjectAmount("2265072g").call()
# return guid_db_contract, node, account, password


if __name__ == "__main__":
    num = input("Is this the 1 node or 2 node?")
    datadir = "/home/matus/Desktop/node01"
    os.system("rm -rf \"{}\"".format(datadir))  # debug purposes

    if num == "1":
        guid_db_contract, node, account, password = run_parent_node()
    else:
        guid_db_contract, node, account, password = run_child_node()
    print("Address:" + guid_db_contract.address)
    print(node.w3.eth.getCode(guid_db_contract.address))
    # print(guid_db_contract.functions.get_studentSubjectAmount("2265072g").call(
    #     {"from": node.w3.toChecksumAddress(account)}))
    app.run(port=5002)
