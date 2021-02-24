from python_geth.node import Node


def get_by_guid(GUID, db):
    amount_of_subjects = db.functions.get_studentSubjectAmount(GUID).call()
    subjects = {}
    for i in range(amount_of_subjects):
        s = db.functions.get_studentSubject(GUID, i).call()
        subjects[s] = db.functions.get_grade(GUID, s).call()

    return subjects


def create_or_update(GUID, subject, grade, db, w3, account):
    tx_hash = db.functions.add_grade(GUID, subject, grade).transact({'from': account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    return tx_receipt


def run_parent_node(datadir):
    node = Node(datadir=datadir, port=30303,
                rpcport=8000, name="Node01")
    node.start_node()

    account, password = node.get_first_account()
    node.w3.geth.personal.unlock_account(account, password)
    return node, account, password


def run_child_node(datadir):
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
