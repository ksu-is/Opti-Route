from dotenv import load_dotenv
import os

# Get your OpenRouteService API key from the environment variable
load_dotenv()
api_key = os.getenv("ORS_API_KEY")
client = openrouteservice.Client(key=api_key)

from flask import Flask, render_template, request
import pandas as pd
import openrouteservice
import plotly.graph_objs as go
import plotly.express as px
import time


import os  # <-- add this

app = Flask(__name__)




app = Flask(__name__)

def visualize_route(df,api_key):
     # Assign colors to each ZoneID
    unique_zones = df['ZoneID'].unique()
    zone_colors = {zone: px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)]
                   for i, zone in enumerate(unique_zones)}


    def get_route(client, start, end):
        return client.directions(
            coordinates=[start, end],
            profile='driving-car',  # or mode from user
            format='geojson'
        )

    fig = go.Figure()

    for i in range(len(df) - 1):
        start = (df.iloc[i]['Longitude'], df.iloc[i]['Latitude'])
        end = (df.iloc[i + 1]['Longitude'], df.iloc[i + 1]['Latitude'])
        route = get_route(client, start, end)
        coords = route['features'][0]['geometry']['coordinates']
        lons, lats = zip(*coords)

        color = zone_colors[df.iloc[i]['ZoneID']] if df.iloc[i]['ZoneID'] == df.iloc[i+1]['ZoneID'] else 'black'

        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=lons,
            lat=lats,
            line=dict(width=4, color=color),
            showlegend=False
        ))

    fig.add_trace(go.Scattermapbox(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='markers+text',
        marker=dict(size=12, color=[zone_colors[z] for z in df['ZoneID']]),
        text=df['Sequence'].astype(str),
        textposition='top center'
    ))

    fig.update_layout(
        mapbox=dict(style="open-street-map",
                    center=dict(lon=df['Longitude'].mean(), lat=df['Latitude'].mean()),
                    zoom=14),
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    # Save HTML so Flask can render it
    filename = "templates/route_map.html"
    fig.write_html(filename)


@app.route('/route', methods=['POST'])
def route():
    origin = request.form['origin']    # format: "lat,lon"
    dest = request.form['destination'] # format: "lat,lon"
    mode = request.form['mode']

    # Parse the input coordinates
    origin_lat, origin_lon = map(float, origin.split(","))
    dest_lat, dest_lon = map(float, dest.split(","))

    # Map your dropdown to OpenRouteService options
    ors_options = {
        "fastest": {"profile": "driving-car"},
        "scenic": {"profile": "driving-car"},
        "beginner": {"profile": "driving-car"},
        "fuel": {"profile": "driving-car"}
    }
    profile = ors_options[mode]["profile"]

    client = openrouteservice.Client(key=api_key)

    # Get the route from OpenRouteService
    route = client.directions(
        coordinates=[[origin_lon, origin_lat], [dest_lon, dest_lat]],
        profile=profile,
        format="geojson"
    )

    # Extract coordinates for plotting
    coords = route['features'][0]['geometry']['coordinates']
    lons, lats = zip(*coords)

    # Build DataFrame for visualize_route
    df = pd.DataFrame({
        "Sequence": list(range(len(coords))),
        "Latitude": lats,
        "Longitude": lons,
        "ZoneID": ["Route"] * len(coords)  # Single zone for now
    })

    visualize_route(df, api_key)

    return render_template("route_map.html")
