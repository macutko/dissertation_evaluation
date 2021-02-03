def getByGUID(GUID, db):
    amount_of_subjects = db.functions.get_studentSubjectAmount(GUID).call()
    subjects = {}
    for i in range(amount_of_subjects):
        s = db.functions.get_studentSubject(GUID, i).call()
        subjects[s] = db.functions.get_grade(GUID, s).call()

    return subjects


def createOrUpdate(GUID, subject, grade, db, CI):
    tx_hash = db.functions.add_grade(GUID, subject, grade).transact()
    tx_receipt = CI.w3.eth.waitForTransactionReceipt(tx_hash)

    return tx_receipt

# if __name__ == '__main__':
#     datadir = "C:\\Users\\matus\\Desktop\\Uni\\lvl_5\\disseration\\bin\\node01"
#     os.system("rm -rf \"{}\"".format(datadir))  # debug purposes
#
#     node1 = Node(datadir=datadir, port=30303,
#                  rpcport=8000, name="Node01")
#     node1.start_node()
#     node1.w3.geth.miner.start(1)
#     node1.configure_truffle()
#     account, password = node1.get_first_account()
#     node1.w3.geth.personal.unlock_account(account, password)
#     CI = ContractInterface(w3=node1.w3,
#                            datadir=datadir)
#     try:
#         db = CI.deploy_contract(
#             contract_file="C:\\Users\\matus\\Desktop\\Uni\\lvl_5\\disseration\\dissertation_evaluation\\geth_db\\db\\GUID_db"
#                           ".sol")[0]
#     except:
#         node1.stop_node()
#
#     createOrUpdate('2265072m', 'PSI', 'A3')
#     createOrUpdate('2265072g', 'AI', 'B3')
#     createOrUpdate('2265072g', 'AI', 'B2')
#     createOrUpdate('2265072g', 'PSI', 'A2')
#
#     print(get('2265072g'))
#     print(get('2265072m'))
