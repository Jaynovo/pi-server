import requests
import csv
import os

url = "https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min/metadata"
resp = requests.get(url)
data = resp.json()

stations = data.get("stations", [])

out_file = os.path.join(os.path.dirname(__file__), "geosphere_stations.csv")

with open(out_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Station ID", "Name", "State",  "Latitude", "Longitude", "Elevation", "Active"])
    for station in stations:
        writer.writerow([
            station.get("id"),
            station.get("name"),
            station.get("state"),
            station.get("lat"),
            station.get("lon"),
            station.get("altitude"),
            station.get("is_active")
        ])

    print(f"Data written to {os.path.abspath(out_file)}")