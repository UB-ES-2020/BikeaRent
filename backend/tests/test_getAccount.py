import requests
import json

def test_getAccount():

    url = "http://127.0.0.1:5000/account/user1"

    headers = {'Content-Type': 'application/json'}

    payload = {'firstname': 'lokt', 'surname': 'dada', 'email': 'jofna@dd', 'username': 'user1',
               'password': 'user1', 'dni': '3124431', 'dataEndDrivePermission': 'sddsdsads', 'status': 'aedew',
               'creditCard': '2343432', 'availableMoney': 12, 'type': 1}
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

