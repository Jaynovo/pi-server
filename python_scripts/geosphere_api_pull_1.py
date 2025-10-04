import psycopg2
import requests
import logging
import datetime
import time

logging.basicConfig(level=logging.INFO)

# Example endpoint (Vienna)
API_BASE = "https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min?parameters=TL"

state_view = ["state_tirol", "state_vbg", "state_kntn", "state_stmk", "state_ooe", "state_noe", "state_burgenland", "state_sbg", "state_wien"]

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_station_ids(conn, state_view):
    cursor = conn.cursor()
    cursor.execute(f"SELECT station_id FROM {state_view}")
    stations = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return stations

def fetch_url_for_stations(conn, station_ids):
    return f"{API_BASE}&station_ids={','.join(map(str, station_ids))}"

def fetch_all_stations(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT station_id FROM stations")
    stations = [row[0] for row in cursor.fetchall()]
    cursor.close()
    print( f"Fetched {len(stations)} stations from database.")
    return stations

def fetch_and_store_data(conn, url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logging.error("Failed to fetch data: %s", e)
        return
    
    cursor = conn.cursor()
    
    #timestamp handling
    timestamp = data.get("timestamps", [None])
    if timestamp is None or len(timestamp) == 0:
        timestamp = datetime.utcnow().isoformat()
    else:
        timestamp = timestamp[0]
    
    # parameters handling
    # hardcoded for now, but could be dynamic if needed
    # records only current temperature (TL)
    features = data.get("features", [])
    for feature in features:
        properties = feature.get("properties", {})
        station_id = int(properties.get("station"))
        parameters = properties.get("parameters", {})

        if "TL" not in parameters:
            logging.warning("No temperature data for station %s", station_id)
            continue
        tl_val = parameters.get("TL", {}).get("data", [None])[0]
        try:
            if tl_val is not None:
                cursor.execute("""
                    INSERT INTO weather_data (station_id, timestamp, temperature)
                    VALUES (%s, %s, %s)
                """, (station_id, timestamp, tl_val))
        except Exception as e:
            logging.error("Failed to insert data for station %s: %s", station_id, e)
    conn.commit()
    cursor.close()
    logging.info("Data insertion complete for %d stations", len(features))
def fetch_and_store_one_station(conn, station_id):
    url = f"{API_BASE}&station_ids={station_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(f"response for station {station_id}: {response}")
        data = response.json()
    except Exception as e:
        logging.error("Failed to fetch data for station %s: %s", station_id, e)
        return
    cursor = conn.cursor()
    
    #timestamp handling
    timestamp = data.get("timestamps", [])
    if timestamp is None or len(timestamp) == 0:
        timestamp = datetime.utcnow().isoformat()
    else:
        timestamp = timestamp[0]
    
    # parameters handling
    # hardcoded for now, but could be dynamic if needed
    # records only current temperature (TL)
    features = data.get("features", [])
    for feature in features:
        properties = feature.get("properties", {})
        station_id = int(properties.get("station"))
        parameters = properties.get("parameters", {})

        if "TL" not in parameters:
            logging.warning("No temperature data for station %s", station_id)
            continue
        tl_val = parameters.get("TL", {}).get("data", [None])[0]
        try:
            cursor.execute("""
                INSERT INTO weather_data (station_id, timestamp, temperature)
                VALUES (%s, %s, %s)
            """, (station_id, timestamp, tl_val))
        except Exception as e:
            logging.error("Failed to insert data for station %s: %s", station_id, e)
    conn.commit()
    cursor.close()
    logging.info("Data insertion complete for station %s", station_id)

def main():
    conn = psycopg2.connect(
        dbname="mydb",
        user="piuser",
        password="secret",
        host="192.168.0.183",
        port="5432"
    )
    all_stations = fetch_all_stations(conn)
    for batch in chunks(all_stations, 30):
        url = fetch_url_for_stations(conn, batch)
        fetch_and_store_data(conn, url)
        time.sleep(1)  # To avoid hitting the API too quickly
    
    """for state in state_view:
        fetch_and_store_data(conn, state)
        time.sleep(2)  # To avoid hitting the API too quickly
    """
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()