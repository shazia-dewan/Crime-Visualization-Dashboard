# main.py
import os
import pymongo
import requests

# Global variables
os.environ['API_KEY'] = 'bRq78semcp0aCbNf5JXRiKa2hvl03XuGWsE7caMG'
api_key = os.getenv('API_KEY')
headers = {'Accept': 'application/json'}
year = "2022"

# MongoDB connection setup
def setup_database():
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["CrimeDatabase"]
        return mydb["CrimeCollection"], mydb["RobberyData"], mydb["HomicideData"]
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(f"Failed to connect to server: {err}")
        return None, None, None

def fetch_data(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def store_data(collection, data):
    collection.insert_many(data) if isinstance(data, list) else collection.insert_one(data)

def fetch_and_store_arrest_data(arrest_collection):
    url = f"https://api.usa.gov/crime/fbi/cde/arrest/national/all?from=2022&to=2024&API_KEY={api_key}"
    resp = fetch_data(url)
    if resp:
        store_data(arrest_collection, resp['data'])
    return resp

def fetch_and_store_robbery_data(robbery_collection):
    states = ["CA", "TX", "NY", "FL", "IL", "PA", "VA", "MA", "WI", "OH", "IN", "MI"]
    robbery_data = {}
    for state in states:
        url = f'https://api.usa.gov/crime/fbi/cde/estimate/state/{state}/robbery?from={year}&to={year}&API_KEY={api_key}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            resp = response.json()
            results = resp['results']
            first_city = list(results.keys())[0]
            first_city_value = results[first_city][year]
            robbery_data[state] = first_city_value
    store_data(robbery_collection, robbery_data)
    return robbery_data

def fetch_and_store_homicide_data(homicide_collection):
    url = f'https://api.usa.gov/crime/fbi/cde/estimate/national/homicide?from=2012&to=2022&API_KEY={api_key}'
    homicide_data = fetch_data(url)
    if homicide_data:
        store_data(homicide_collection, homicide_data)
    return homicide_data

def main():
    ArrestData, RobberyData, HomicideData = setup_database()

    # Fetch and store arrest data
    fetch_and_store_arrest_data(ArrestData)

    # Fetch and store robbery data
    fetch_and_store_robbery_data(RobberyData)

    # Fetch and store homicide data
    fetch_and_store_homicide_data(HomicideData)

if __name__ == "__main__":
    main()
