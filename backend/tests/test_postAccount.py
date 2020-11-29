import requests
import json
'''
def test_postAccountExists():

    url = "http://127.0.0.1:5000/account"

    headers = {'Content-Type': 'application/json'}

    payload = {'firstname': 'koli', 'surname': 'pepe', 'email': 'jjofnfda@dd', 'username': 'user99', 'password': 'user99', 'dni': '3124431', 'dataEndDrivePermission': 'sddsdsads', 'status': 'aedew', 'creditCard': '2343432', 'availableMoney': 12122, 'type': 1}

    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 400
'''

'''
def test_postAccountAdded():
    url = "http://127.0.0.1:5000/account"

    headers = {'Content-Type': 'application/json'}

    payload = {'firstname': 'testadd1', 'surname': 'testadd1', 'email': 'testadd1@dd', 'username': 'testadd1', 'password': 'testadd1', 'dni': 'testadd1', 'dataEndDrivePermission': 'testadd1', 'status': 'testadd1', 'creditCard': 'testadd1', 'availableMoney': 99999, 'type': 1}

    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    print(resp.json())

    assert resp.status_code == 200
'''