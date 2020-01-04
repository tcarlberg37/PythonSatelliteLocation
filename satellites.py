import requests, json, googlemaps, gmplot, sqlite3, time
import matplotlib.pyplot as plt

gmaps = googlemaps.Client(key="API KEY HERE")

def get_satellite_data(s_id): # satellite id for ISS = 25544
    file = open('isslocation.txt', 'w') # change to 'a' to add to file
    response = requests.get("https://api.wheretheiss.at/v1/satellites/" + str(s_id))
    print("Status Code:", response.status_code)
    json.dump(response.json(), file, indent=4)
    file.close()

    print(response.json())
    return response.json()

    
def get_earth_location(data):
    lat = data['latitude']
    long = data['longitude']

    gmap = gmplot.GoogleMapPlotter(lat, long, 5)
    gmap.apikey = "API KEY HERE"
    gmap.marker(lat, long)
    gmap.draw("C:\\Users\\tcarl\\Dropbox\\Python\\Satellites\\map.html")

    return gmaps.reverse_geocode((lat, long))


def save_to_db(conn, data):  # data is a dict from get_satellite_data()
    c = conn.cursor()
    query = "INSERT INTO satellites VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, '{}', {})".format(data['id'], data['daynum'], data['timestamp'],
    data['latitude'], data['longitude'], data['altitude'], data['velocity'], data['solar_lat'], data['solar_lon'], data['visibility'], data['footprint'])

    c.execute(query)
    conn.commit()
    c.close()


def read_data(conn):
    c = conn.cursor()
    query = "SELECT * FROM satellites"
    c.execute(query)
    count = 0
    lats = []
    lons = []
    timestamps = []
    for record in c.fetchall():
        print("ID:", record[0], "\tDay Number:", record[1], "\tTimestamp:", record[2], "\nLatitude:", record[3], "\tLongitude:", record[4],
            "\tAltitude:", record[5], "\tVelocity:", record[6])
        count += 1
        lats.append(record[3])
        lons.append(record[4])
        timestamps.append(record[2])
    c.close()
    print("There are", count, "rows in the table.")

    return {"latitudes": lats, "longitudes": lons, "timestamps": timestamps}


def create_table(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS satellites(id INTEGER, DayNumber REAL, timestamp INTEGER, latitude REAL, longitude REAL, altitude REAL, velocity REAL, solar_lat REAL, solar_lon REAL, visibility TEXT, footprint REAL)")
    c.close()


if __name__ == "__main__":
    # establish connection to database
    conn = sqlite3.connect("satellites.db")
    create_table(conn)
    data = get_satellite_data(25544)
    map = get_earth_location(data) # saves the map locally
    save_to_db(conn, data) # saves to database
    coords = read_data(conn)
    #print(coords)
    # create a scatter plot for (long, lat) vs time of day
    times = [time.time() - t for t in coords['timestamps']]
    plt.scatter(coords['longitudes'], coords['latitudes']) 
    #plt.plot(times, coords['longitudes'], 'ro', times, coords['latitudes'], 'bs')
    plt.show()
    conn.close()
