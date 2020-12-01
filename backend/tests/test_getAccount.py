import requests
import json

def test_getAccount():

    url = "http://127.0.0.1:5000/account/admin"

    headers = {'Content-Type': 'application/json'}

    payload = {'firstname': 'admin', 'surname': 'admin', 'email': 'jofna@dd', 'username': 'admin',
               'password': 'admin', 'dni': '3333', 'dataEndDrivePermission': 'sddsds', 'status': 'aeee',
               'creditCard': '2343432', 'availableMoney': 12, 'type': 3}
    resp = requests.get(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 200


def test_getAccountFail():
    url = "http://127.0.0.1:5000/account/user2"

    headers = {'Content-Type': 'application/json'}

    payload = {'firstname': 'user2', 'surname': 'user2', 'email': 'juser2@dd', 'username': 'user2',
               'password': 'user2', 'dni': '331', 'dataEndDrivePermission': 'sads', 'status': 'aw',
               'creditCard': '2332', 'availableMoney': 12122, 'type': 1}

    resp = requests.get(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 404

'''
def test_getAccountHeroku():

    url = "bike-a-rent.herokuapp.com/account/admin"

    headers = {'Content-Type': 'application/json'}

    payload = {'firstname': 'admin', 'surname': 'admin', 'email': 'admin', 'username': 'admin',
               'password': 'admin', 'dni': 'admin', 'dataEndDrivePermission': 'admin', 'status': True,
               'creditCard': '12345', 'availableMoney': 100, 'type': 3}
    
    resp = requests.get(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 200
'''

'''
def test_getAccountFailHeroku():

    url = "bike-a-rent.herokuapp.com/account/testingUser"

    payload = {'firstname': 'user2', 'surname': 'user2', 'email': 'juser2@dd', 'username': 'user2',
               'password': 'user2', 'dni': '331', 'dataEndDrivePermission': 'sads', 'status': 'aw',
               'creditCard': '2332', 'availableMoney': 12122, 'type': 1}

    resp = requests.get(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 404
'''