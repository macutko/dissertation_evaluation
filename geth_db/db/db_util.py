def getByGUID(GUID, db):
    amount_of_subjects = db.functions.get_studentSubjectAmount(GUID).call()
    subjects = {}
    for i in range(amount_of_subjects):
        s = db.functions.get_studentSubject(GUID, i).call()
        subjects[s] = db.functions.get_grade(GUID, s).call()

    return subjects


def createOrUpdate(GUID, subject, grade, db, w3,account):
    tx_hash = db.functions.add_grade(GUID, subject, grade).transact({'from':account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    return tx_receipt