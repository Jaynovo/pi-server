import os
import sys
import requests
import logging
from datetime import datetime

# Always put log next to the script
log_path = os.path.join(os.path.dirname(__file__), "geosphere.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_path, mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Example endpoint (Vienna)
url = "https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min?parameters=TL,TLMAX&station_ids=11318&start=2025-09-17&end=2025-09-18"


logging.info("Fetching data from Geosphere Austria API...")

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Log full JSON response
    logging.info("Fetched data: %s", data)

    # Example: log just the current temperature
    if "features" in data and len(data["features"]) > 0:
        temp = data["features"][0]["properties"]["parameters"]["TL"]["data"]
        logging.info("Current temperature: %s °C", temp)

except Exception as e:
    logging.error("Failed to fetch data: %s", e)

logging.info("Script finished.")