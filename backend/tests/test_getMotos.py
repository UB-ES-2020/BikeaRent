import requests
import json

def test_getMoto():

    url = "http://127.0.0.1:5000/bike/1"

    headers = {'Content-Type': 'application/json'}

    payload = {'model': 'VESPIN', 'active': True, 'charge': 32132, 'latitude': 231, 'longitude': 42, 'plate': "fds"}

    resp = requests.get(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 200


def test_getMotoFail():
    url = "http://127.0.0.1:5000/bike/99"

    headers = {'Content-Type': 'application/json'}

    payload = {'model': 'VESPIN99', 'active': True, 'charge': 332, 'latitude': 231, 'longitude': 42, 'plate': "fds"}

    resp = requests.get(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 404


