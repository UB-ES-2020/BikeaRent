import requests
import json

#S'ha de posar la matricula com a unique, sino no esta be i no funciona el metode correctament

def test_postMoto():

    url = "http://127.0.0.1:5000/bike"

    headers = {'Content-Type': 'application/json'}

    payload = {'model': 'VespaTest', 'active': True, 'charge': 9999, 'latitude': 9999, 'longitude': 999, 'plate': "aaaa"}

    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    assert resp.status_code == 500



