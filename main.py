import requests
from requests.auth import HTTPBasicAuth
import os
import pymongo
from pymongo.mongo_client import MongoClient
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import pandas as pd

# Global variables
my_secret = os.environ['api_key']
api_key = my_secret[2:-1]
headers = {'Accept': 'application/json'}
year = "2022"

# MongoDB connection setup
def setup_database():
    myclient = pymongo.MongoClient(
        "mongodb+srv://shaziadewan:123@cluster77.uwhpj3s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster77"
    )
    mydb = myclient["CrimeDatabase"]
    return mydb["CrimeCollection"], mydb["RobberyData"], mydb["HomicideData"]

# Function to fetch data from API
def fetch_data(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

# Function to store data in MongoDB
def store_data(collection, data):
    collection.insert_many(data) if isinstance(data, list) else collection.insert_one(data)

# Fetch and store arrest data
def fetch_and_store_arrest_data(arrest_collection):
    url = f"https://api.usa.gov/crime/fbi/cde/arrest/national/all?from=2022&to=2024&API_KEY={api_key}"
    resp = fetch_data(url)
    if resp:
        store_data(arrest_collection, resp)
    return resp
  
# Function to calculate total arrests and most common crime
def analyze_arrest_data(data):
    data = data['data'][0]
    total_crimes = sum(value for key, value in data.items() if key != 'data_year')
    most_common_crime = max((key, value) for key, value in data.items() if key != 'data_year')
    return total_crimes, most_common_crime

# Function to create a pie chart for crime breakdown
def plot_crime_breakdown(data):
    types_crimes = []
    crime_num = []
    for key, value in data.items():
        if key != 'data_year' and len(types_crimes) <= 7:
            types_crimes.append(key)
            crime_num.append(value)
    plt.pie(crime_num, labels=types_crimes)
    plt.show()

# Function to create a heatmap for robbery hotspots
def plot_heatmap(crime_count, state_coordinates, states):
    fig, ax = plt.subplots(figsize=(12, 8))
    m = Basemap(llcrnrlon=-125, llcrnrlat=24, urcrnrlon=-66, urcrnrlat=50, projection='merc', ax=ax)
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()

    lats = [state_coordinates[state][0] for state in states]
    lons = [state_coordinates[state][1] for state in states]
    x, y = m(lons, lats)

    max_crime = max(crime_count)
    min_crime = min(crime_count)

    for (xi, yi, crime) in zip(x, y, crime_count):
        size = (crime - min_crime) / (max_crime - min_crime) * 1000 + 100
        m.scatter(xi, yi, s=size, color='red', alpha=0.5, edgecolor='k', linewidth=0.5, zorder=10)

    plt.title('Crime Heatmap in Different States')
    plt.show()

# Function to create a bar graph for crime by state
def plot_crime_by_state(states, crime_count):
    fig = plt.figure(figsize=(10, 5))
    plt.bar(states, crime_count, color='maroon', width=0.4)
    plt.xlabel("States")
    plt.ylabel("Crime Count")
    plt.title("Crime count by state")
    plt.show()

# Function to create a line graph for crime trends
def plot_crime_trend(data):
    crime_data = data['results']['United States Homicide']
    years = list(crime_data.keys())
    numbers = list(crime_data.values())
    crime_trend = pd.DataFrame({'year': years, 'crime count': numbers})
    crime_trend['year'] = pd.to_numeric(crime_trend['year'])
    plt.figure(figsize=(10, 6))
    plt.plot(crime_trend['year'], crime_trend['crime count'], marker='o')
    plt.xlabel('Year')
    plt.ylabel('Crime Count')
    plt.title('Crime Trend Over Years')
    plt.grid(True)
    plt.show()


def main():
  # Setup database
  ArrestData, RobberyData, HomicideData = setup_database()

  # Fetch and store arrest data
  arrest_data = fetch_and_store_arrest_data(ArrestData)

  if arrest_data:
      # Analyze arrest data
      total_crimes, most_common_crime = analyze_arrest_data(arrest_data['data'][0])
      print(f"Total number of Arrests in {year}: {total_crimes}")
      print(f"Most common crime type in {year}: {most_common_crime[0]}")

      # Plot crime breakdown
      plot_crime_breakdown(arrest_data['data'][0])

  # Fetch and store robbery data
  states = ["CA", "TX", "NY", "FL", "IL", "PA", "VA", "MA", "WI", "OH", "IN", "MI"]
  state_coordinates = {
      "CA": [36.7783, -119.4179],
      "TX": [31.9686, -99.9018],
      "NY": [40.7128, -74.0060],
      "FL": [27.9944, -81.7603],
      "IL": [40.6331, -89.3985],
      "PA": [41.2033, -77.1945],
      "VA": [37.4316, -78.6569],
      "MA": [42.4072, -71.3824],
      "WI": [43.7844, -88.7879],
      "OH": [40.4173, -82.9071],
      "IN": [40.2672, -86.1349],
      "MI": [44.3148, -85.6024]
  }
  crime_count = []

  for state in states:
      url = f'https://api.usa.gov/crime/fbi/cde/estimate/state/{state}/robbery?from={year}&to={year}&API_KEY={api_key}'
      response = requests.get(url, headers=headers)
      if response.status_code == 200:
          resp = response.json()
          results = resp['results']
          first_city = list(results.keys())[0]
          first_city_value = results[first_city][year]
          crime_count.append(first_city_value)

  # Plot heatmap
  plot_heatmap(crime_count, state_coordinates, states)

  # Plot crime by state
  plot_crime_by_state(states, crime_count)
  meanCrimesPerState = np.mean(crime_count)
  medianCrimesPerState = np.median(crime_count)
  modeCrimesPerState = np.std(crime_count)

  # Fetch and store homicide data
  url = f'https://api.usa.gov/crime/fbi/cde/estimate/national/homicide?from=2012&to=2022&API_KEY={api_key}'
  homicide_data = fetch_data(url)
  if homicide_data:
      store_data(HomicideData, homicide_data)

  # Plot crime trend
  if homicide_data:
      plot_crime_trend(homicide_data)

if __name__ == "__main__":
  main()

