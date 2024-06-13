myclient = pymongo.MongoClient(
    "mongodb+srv://shaziadewan:123@cluster77.uwhpj3s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster77"
)
mydb = myclient["CrimeDatabase"]
ArrestData = mydb["CrimeCollection"]
robberyData = mydb["RobberyData"]
HomicideData = mydb["HomicideData"]

### Global variables ###
my_secret = os.environ['api_key']
api_key = my_secret[2:-1]
headers = {'Accept': 'application/json'}
year = "2022"

### Collecting API Data ###

#Total number of arrests this year (A grand total)
url = f"https://api.usa.gov/crime/fbi/cde/arrest/national/all?from=2022&to=2024&API_KEY={api_key}"
resp = requests.get(url, headers=headers)
if resp.status_code == 200:
  resp = resp.json()
  print(resp)

#Insert national arrest data into mongoDB
#ArrestData.insert_many(resp)

data = resp['data'][0]
total_crimes = sum(value for key, value in data.items() if key != 'data_year')
print(f"Total number of Arrests in {year}: {total_crimes}")

#Most Common crime type this year (A single word)
most_common_crime = max(
    (key, value) for key, value in data.items() if key != 'data_year')
print(f"Most common crime type in {year}: {most_common_crime[0]}")

### Crime breakdown ###
#Types of crimes (Pie graph percentage of each crime)
types_crimes = []
crime_num = []
for key, value in data.items():
  if key != 'data_year' and len(types_crimes) <= 7:
    types_crimes.append(key)
    crime_num.append(value)

plt.pie(crime_num, labels = types_crimes)
#plt.show()

### Geographical analysis ###
#Heatmap showing crime robbery hotspots
states = [
    "CA", "TX", "NY", "FL", "IL", "PA", "VA", "MA", "WI", "OH", "IN", "MI"
]
crime_count = []
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
for state in states:
  url = f'https://api.usa.gov/crime/fbi/cde/estimate/state/{state}/robbery?from={year}&to={year}&API_KEY={api_key}'
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    resp = response.json()
    results = resp['results']
    first_city = list(results.keys())[0]
    first_city_value = results[first_city][year]
    crime_count.append(first_city_value)

#Make heatmap
fig, ax = plt.subplots(figsize=(12, 8))
m = Basemap(llcrnrlon=-125, llcrnrlat=24, urcrnrlon=-66, urcrnrlat=50, projection='merc', ax=ax)

m.drawcoastlines()
m.drawcountries()
m.drawstates()

# Extract latitudes and longitudes
lats = [state_coordinates[state][0] for state in states]
lons = [state_coordinates[state][1] for state in states]

# Convert lat/lon to map projection coordinates
x, y = m(lons, lats)

# Plot each state with a circle whose size represents the crime count
max_crime = max(crime_count)
min_crime = min(crime_count)

for (xi, yi, crime) in zip(x, y, crime_count):
    size = (crime - min_crime) / (max_crime - min_crime) * 1000 + 100
    m.scatter(xi, yi, s=size, color='red', alpha=0.5, edgecolor='k', linewidth=0.5, zorder=10)

plt.title('Crime Heatmap in Different States')
#plt.show()
#Insert estimates into mongoDB
#robberyData.insert_one(resp)

#Bar graph crime by state
#Already have crime count and cities from previous API call
fig = plt.figure(figsize=(10, 5))

# creating the bar plot
plt.bar(states, crime_count, color='maroon', width=0.4)

plt.xlabel("States")
plt.ylabel("Crime Count")
plt.title("Crime count by state")
#plt.show()

### Trend analysis ###
# Line graoh showing a secific type of crime overtime
url = f'https://api.usa.gov/crime/fbi/cde/estimate/national/homicide?from=2012&to=2022&API_KEY={api_key}'
response = requests.get(url, headers=headers)
if response.status_code == 200:
  resp = response.json()
  results = resp['results']

print(resp)

#Insert homicide data into mongoDB
#HomicideData.insert_one(resp)

#Make line graph
crime_data = resp['results']['United States Homicide']

# Extract years and numbers into separate lists
years = list(crime_data.keys())
numbers = list(crime_data.values())

crime_trend = pd.DataFrame({'year': years, 'crime count': numbers})

# Ensure the 'year' column is numerical
crime_trend['year'] = pd.to_numeric(crime_trend['year'])

# Plot the line graph
plt.figure(figsize=(10, 6))
plt.plot(crime_trend['year'], crime_trend['crime count'], marker='o')
plt.xlabel('Year')
plt.ylabel('Crime Count')
plt.title('Crime Trend Over Years')
plt.grid(True)
plt.show()

for x in HomicideData.find():
  print(x)
