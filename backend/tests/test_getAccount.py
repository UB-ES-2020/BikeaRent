import requests
import json

def addAcc():

    url = "http://127.0.0.1:5000/account"

    headers = {'Content-Type': 'application/json'}

    payload = {'firstname': 'adminTest', 'surname': 'adminTest', 'email': 'adminTest@dd', 'username': 'adminTest',
               'password': 'adminTest', 'dni': 'adminTest', 'dataEndDrivePermission': 'adminTest', 'status': False,
               'creditCard': 'adminTest', 'availableMoney': 999, 'type': 3, 'latitude': 932, 'longitude': -231}

    requests.post(url, headers=headers, data=json.dumps(payload, indent=4))


def test_getAccount():
    url = "http://127.0.0.1:5000/account/adminTest"

    headers = {'Content-Type': 'application/json'}

    payload = {'firstname': 'adminTest', 'surname': 'adminTest', 'email': 'adminTest@dd', 'username': 'adminTest',
               'password': 'adminTest', 'dni': 'adminTest', 'dataEndDrivePermission': 'adminTest', 'status': False,
               'creditCard': 'adminTest', 'availableMoney': 999, 'type': 3, 'latitude': 932, 'longitude': -231}
    resp = requests.get(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 200


def test_getAccountFail():
    url = "http://127.0.0.1:5000/account/user2"

    headers = {'Content-Type': 'application/json'}

    payload = {'firstname': 'user2', 'surname': 'user2', 'email': 'juser2@dd', 'username': 'user2',
               'password': 'user2', 'dni': '331', 'dataEndDrivePermission': 'sads', 'status': 'aw',
               'creditCard': '2332', 'availableMoney': 12122, 'type': 1, 'latitude': 932, 'longitude': -231}

    resp = requests.get(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 404


'''
def test_getAccountHeroku():

    url = "bike-a-rent.herokuapp.com/account/admin"

    headers = {'Content-Type': 'application/json'}

    payload = {'firstname': 'admin', 'surname': 'admin', 'email': 'admin', 'username': 'admin',
               'password': 'admin', 'dni': 'admin', 'dataEndDrivePermission': 'admin', 'status': True,
               'creditCard': '12345', 'availableMoney': 100, 'type': 3, 'latitude': 932, 'longitude': -231}

    resp = requests.get(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 200
'''

'''
def test_getAccountFailHeroku():

    url = "bike-a-rent.herokuapp.com/account/testingUser"

    payload = {'firstname': 'user2', 'surname': 'user2', 'email': 'juser2@dd', 'username': 'user2',
               'password': 'user2', 'dni': '331', 'dataEndDrivePermission': 'sads', 'status': 'aw',
               'creditCard': '2332', 'availableMoney': 12122, 'type': 1, 'latitude': 932, 'longitude': -231}

    resp = requests.get(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 404
'''