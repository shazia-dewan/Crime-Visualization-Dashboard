import requests
import requests_mock
import pytest
import os

api_key = os.environ['api_key']
api_key = api_key[2:-1]
headers = {'Accept': 'application/json'}

def test_collect_arrest_data():
    url = f"https://api.usa.gov/crime/fbi/cde/arrest/national/all?from=2022&to=2024&API_KEY={api_key}"
    mock_response = {
        'data': [{'data_year': '2022', 'arson': 1000, 'burglary': 500}]
    }

    with requests_mock.Mocker() as m:
        m.get(url, json=mock_response)
        response = requests.get(url, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        assert data['data'][0]['arson'] == 1000
        assert data['data'][0]['burglary'] == 500
