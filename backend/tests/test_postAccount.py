import requests
import json

def test_postAccountExists():

    url = "http://127.0.0.1:5000/account"

    headers = {'Content-Type': 'application/json'}

    payload = {'firstname': 'testadd', 'surname': 'testadd', 'email': 'testadd@dd', 'username': 'testadd', 'password': 'testadd', 'dni': '31testadd', 'dataEndDrivePermission': 'testaddads', 'status': 'testadddew', 'creditCard': '2332', 'availableMoney': 1212, 'type': 1}

    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 400



def test_postAccountAdded():
    url = "http://127.0.0.1:5000/account"

    headers = {'Content-Type': 'application/json'}

    payload = {'firstname': 'testadd1', 'surname': 'testadd1', 'email': 'testadd1@dd', 'username': 'testadd1', 'password': 'testadd1', 'dni': 'testadd1', 'dataEndDrivePermission': 'testadd1', 'status': 'testadd1', 'creditCard': 'testadd1', 'availableMoney': 99999, 'type': 1}

    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 200


def test_postAccoutDeleteOK():

    url = "http://127.0.0.1:5000/account/testadd1"

    headers = {'Content-Type': 'application/json'}

    resp = requests.delete(url, headers=headers)

    assert resp.status_code == 200

def test_postAccountDeleteFail():

    url = "http://127.0.0.1:5000/account/user2"

    headers = {'Content-Type': 'application/json'}

    payload = {'firstname': 'user2', 'surname': 'user2', 'email': 'juser2@dd', 'username': 'user2',
               'password': 'user2', 'dni': '331', 'dataEndDrivePermission': 'sads', 'status': 'aw',
               'creditCard': '2332', 'availableMoney': 12122, 'type': 1}

    resp = requests.delete(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 404