> Note: The `.env` file is ignored by GitHub for security reasons.

from dotenv import load_dotenv
import os
import pandas as pd
import openrouteservice

from flask import Flask, render_template, request

import plotly.graph_objs as go
import plotly.express as px

# --------------------------------------------------
# ENV + API SETUP
# --------------------------------------------------

from dotenv import load_dotenv
import os

load_dotenv()  # 👈 load .env file here

api_key = os.getenv("ORS_API_KEY")

import pandas as pd
import openrouteservice

client = openrouteservice.Client(key=api_key)  # uses api_key, must be after loading


# --------------------------------------------------
# FLASK APP
# --------------------------------------------------

app = Flask(__name__)

# --------------------------------------------------
# ROUTE MODES
# --------------------------------------------------

ROUTE_MODES = {
    "fastest": {
        "profile": "driving-car",
        "preference": "fastest"
    },
    "scenic": {
        "profile": "driving-car",
        "preference": "shortest",
        "avoid_features": ["highways"]
    },
    "beginner": {
        "profile": "driving-car",
        "preference": "shortest",
        "avoid_features": ["highways", "tollways"]
    },
    "fuel": {
        "profile": "driving-car",
        "preference": "shortest"
    }
}

# --------------------------------------------------
# VISUALIZATION FUNCTION
# --------------------------------------------------

def visualize_route(df):
    unique_zones = df['ZoneID'].unique()

    zone_colors = {
        zone: px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)]
        for i, zone in enumerate(unique_zones)
    }

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='lines+markers',
        line=dict(width=4),
        marker=dict(size=8),
        showlegend=False
    ))

    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(
                lon=df['Longitude'].mean(),
                lat=df['Latitude'].mean()
            ),
            zoom=13
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    map_html = fig.to_html(full_html=False)
    return render_template("route_map.html", map_html=map_html)

       
# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.route('/')
def index():
    return render_template("index.html")



@app.route('/route', methods=['POST'])
def route():
    origin_input = request.form['origin']
    dest_input = request.form['destination']
    mode = request.form['mode']

    # Use OpenRouteService geocode to get coordinates if input is an address
    def get_coords(location):
        try:
            # Try splitting as decimal coordinates first
            lat, lon = map(float, location.split(","))
            return [lon, lat]  # ORS uses [lon, lat]
        except:
            # Treat as address
            result = client.pelias_search(text=location)
            coords = result['features'][0]['geometry']['coordinates']
            return coords  # [lon, lat]

    start = get_coords(origin_input)
    end = get_coords(dest_input)

    config = ROUTE_MODES.get(mode, ROUTE_MODES["fastest"])

    route_data = client.directions(
        coordinates=[start, end],
        profile=config["profile"],
        preference=config["preference"],
        options={
            "avoid_features": config.get("avoid_features", [])
        },
        format="geojson"
    )

    coords = route_data['features'][0]['geometry']['coordinates']
    lons, lats = zip(*coords)

    df = pd.DataFrame({
        "Sequence": list(range(len(coords))),
        "Latitude": lats,
        "Longitude": lons,
        "ZoneID": ["Route"] * len(coords)
    })

    return visualize_route(df)


# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
