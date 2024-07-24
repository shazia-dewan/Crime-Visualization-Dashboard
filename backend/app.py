# app.py
from flask import Flask, send_file, jsonify
import matplotlib.pyplot as plt
import io
import os
import pymongo
import requests
from mpl_toolkits.basemap import Basemap
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

ArrestData, RobberyData, HomicideData = setup_database()

if ArrestData is None or RobberyData is None or HomicideData is None:
    print("Database connection failed. Exiting...")
    exit(1)

# Fetch data from MongoDB
def fetch_data_from_db(collection):
    data = collection.find_one()
    return data

@app.route('/test')
def test():
    print("here")
    return {"hello":"there"}

@app.route('/api/plot/pie')
def get_pie_chart():
    data = fetch_data_from_db(ArrestData)
    if data:
        data.pop('_id', None)
        data.pop('data_year', None)
        types_crimes = []
        crime_num = []
        
        # Extracting and sorting crime types by number of offenses
        sorted_crimes = sorted(data.items(), key=lambda item: item[1], reverse=True)
        
        for key, value in sorted_crimes:
            if key != 'data_year' and len(types_crimes) < 7:
                types_crimes.append(key)
                crime_num.append(value)
        
        fig, ax = plt.subplots()
        ax.pie(crime_num, labels=types_crimes, autopct='%1.1f%%')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    
    return jsonify({'error': 'No data found'}), 404

@app.route('/api/plot/bar')
def get_bar_chart():
    data = fetch_data_from_db(RobberyData)
    print(data)
    if data:
        # Remove the '_id' key from the data
        data.pop('_id', None)

        states = list(data.keys())
        crime_count = list(data.values())

        fig = plt.figure(figsize=(10, 5))
        plt.bar(states, crime_count, color='maroon', width=0.4)
        plt.xlabel("States")
        plt.ylabel("Crime Count")
        plt.title("Crime Count by State")

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    
    return jsonify({'error': 'No data found'}), 404

state_coordinates = {
    'CA': (36.7783, -119.4179),
    'TX': (31.9686, -99.9018),
    'NY': (40.7128, -74.0060),
    'FL': (27.9944, -81.7603),
    'IL': (40.6331, -89.3985),
    'PA': (41.2033, -77.1945),
    'VA': (37.4316, -78.6569),
    'MA': (42.4072, -71.3824),
    'WI': (43.7844, -88.7879),
    'OH': (40.4173, -82.9071),
    'IN': (40.2672, -86.1349),
    'MI': (44.3148, -85.6024)
}

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
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

@app.route('/api/plot/heatmap')
def get_heatmap():
    data = fetch_data_from_db(RobberyData)
    if data:
        # Remove the '_id' key from the data
        data.pop('_id', None)

        states = list(data.keys())
        crime_count = list(data.values())

        buf = plot_heatmap(crime_count, state_coordinates, states)
        return send_file(buf, mimetype='image/png')
    
    return jsonify({'error': 'No data found'}), 404


@app.route('/api/plot/line')
def get_line_chart():
    data = fetch_data_from_db(HomicideData)
    if data:
        crime_data = data['results']['United States Homicide']
        years = list(map(int, crime_data.keys()))  # Convert year strings to integers
        numbers = list(map(float, crime_data.values()))  # Convert counts to floats if necessary

        # Sort the data by years
        sorted_years_numbers = sorted(zip(years, numbers))
        years, numbers = zip(*sorted_years_numbers)

        plt.figure(figsize=(10, 6))
        plt.plot(years, numbers, marker='o')
        plt.xlabel('Year')
        plt.ylabel('Crime Count')
        plt.title('Crime Trend Over Years')
        plt.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    
    return jsonify({'error': 'No data found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
