import requests
import json


def test_postMoto():
    url = "http://127.0.0.1:5000/bike"

    headers = {'Content-Type': 'application/json'}

    payload = {'model': 'VespaTest', 'active': True, 'charge': 9999, 'latitude': 9999, 'longitude': 999,
               'plate': "aaaa"}

    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 500


'''
def test_postMotoHeroku():

    url = "http://127.0.0.1:5000/bike"

    headers = {'Content-Type': 'application/json'}

    payload = {'model': 'vespa', 'active': False, 'charge': 100, 'latitude': 32, 'longitude': 45, 'plate': "123abc"}

    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 500
'''
