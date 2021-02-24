import csv
import json
import random

import requests


def simple_get(URL, data):
    return requests.get(url=URL + "get",
                        params=data)


def simple_create(URL, data):
    return requests.post(url=URL + "create",
                         json=data)


def simple_update(URL, data):
    return requests.put(url=URL + "update",
                        json=data)


def simple_mongo():
    URL = "http://localhost:12346/"
    for i in range(3):
        print("ROUND MONGO: {}".format(i + 1))
        data = {"GUID": "2265{}72g".format(random.randint(0, 1000)), "subject": "PSI", "grade": "A3"}

        r = json.loads(simple_create(URL, data).text)
        print("\t Create: {} ms".format(r['time']))

        data['grade'] = "A1"
        r = json.loads(simple_update(URL, data).text)
        print("\t Update: {} ms".format(r['time']))

        r = json.loads(simple_get(URL, data).text)
        print("\t Get: {} ms".format(r['time']))
        print()


def simple_geth():
    URL = "http://192.168.0.73:5002/"
    for i in range(3):
        print("ROUND GETH: {}".format(i + 1))
        data = {"GUID": "2265{}72g".format(random.randint(0, 1000)), "subject": "PSI", "grade": "A3"}

        r = json.loads(simple_create(URL, data).text)
        print("\t Create: {} s".format(r['time']))

        data['grade'] = "A1"
        r = json.loads(simple_update(URL, data).text)
        print("\t Update: {} s".format(r['time']))

        r = json.loads(simple_get(URL, data).text)
        print("\t Get: {} s".format(r['time']))
        print()


def bulk_create_100(URL, name):
    with open('100guid.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]: rows[1] for rows in reader}
    total_time = 0.0
    counter = 0
    for key, value in mydict.items():
        v = value.strip('[]\'')
        v = v.split(', ')
        data = {"GUID": key, "subject": v[0].strip('\''), "grade": v[1].strip('\'')[1]}
        r = simple_create(URL, data)

        if r.status_code != 200:
            exit(0)
        else:
            r = json.loads(r.text)
            total_time = total_time + float(r['time'])
        counter += 1
        print("Item {}/{}".format(counter, len(mydict.items())))
    print("BULK CREATE 100 {0}: {1}".format(name, total_time))


def bulk_get_100(URL, name):
    with open('100guid.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]: rows[1] for rows in reader}
    total_time = 0.0
    counter = 0
    for key, value in mydict.items():
        v = value.strip('[]\'')
        v = v.split(', ')
        data = {"GUID": key, "subject": v[0].strip('\''), "grade": v[1].strip('\'')[1]}
        r = simple_get(URL, data)

        if r.status_code != 200:
            exit(0)
        else:
            r = json.loads(r.text)
            total_time = total_time + float(r['time'])
        counter += 1
        print("Item {}/{}".format(counter, len(mydict.items())))

    print("BULK GET 100 {0}: {1}".format(name, total_time))


if __name__ == '__main__':
    # bulk_create_100("http://localhost:5002/", "Geth (s)")
    # bulk_get_100("http://localhost:5002/", "Geth (s)")
    simple_geth()

    # bulk_create_100("http://localhost:12346/", "Mongo (ms)")
    # bulk_get_100("http://localhost:12346/", "Mongo (ms)")
    # simple_mongo()
