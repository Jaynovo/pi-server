import requests
import psycopg2

url = "https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min/metadata"
resp = requests.get(url)
data = resp.json()

connection = psycopg2.connect(
    dbname="mydb",
    user="piuser",
    password="secret",
    host="192.168.0.183",
    port="5432"
)

try:
    cursor = connection.cursor()

    stations = data.get("stations", [])

    for station in stations:
        station_id = station.get("id")
        name = station.get("name")    
        state = station.get("state")
        latitude = station.get("lat")
        longitude = station.get("lon")
        elevation = station.get("altitude")
        is_active = station.get("is_active")

        cursor.execute("""
            INSERT INTO stations (station_id, name, state, latitude, longitude, elevation, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (station_id) DO UPDATE SET
                name = EXCLUDED.name,
                state = EXCLUDED.state,
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude,
                elevation = EXCLUDED.elevation,
                is_active = EXCLUDED.is_active
        """, (station_id, name, state, latitude, longitude, elevation, is_active))
        connection.commit()
finally:
    if 'cursor' in locals():
        cursor.close()
    connection.close() #all inserts for better performance
    connection.commit()