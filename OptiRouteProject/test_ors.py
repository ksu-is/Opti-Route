from dotenv import load_dotenv
import os
import openrouteservice

load_dotenv()

api_key = os.getenv("ORS_API_KEY")
print("Using key:", api_key)

client = openrouteservice.Client(key=api_key)

route = client.directions(
    coordinates=[[-122.084, 37.422], [-122.1430, 37.4419]],
    profile="driving-car",
    format="geojson"
)

print("SUCCESS! Route distance (meters):",
      route["features"][0]["properties"]["segments"][0]["distance"])
