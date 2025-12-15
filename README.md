# Opti-Route — Minimal Python Route Planner

This repository contains a minimal Flask-based route planner that uses OpenStreetMap data (via `osmnx`) and `networkx` to compute routes. It offers four route styles: `fastest`, `scenic`, `beginner-friendly`, and `fuel-efficient` using simple heuristics.

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the app:

```bash
python app.py
```

3. Open http://localhost:5000 in a browser. Provide origin/destination (address or `lat,lon`) and pick a route type.

Notes & Next steps
- This is a minimal prototype. For production and better routing, consider using an external routing engine (OSRM / GraphHopper) or enrich OSM edge data (speeds, turn penalties, elevation).
- The `scenic` and `beginner` heuristics are rough and can be tuned with real user feedback.
Opti-Route

A Python application that customizes driving routes based on user preferences. Users can choose routes that are fastest, most scenic, beginner-friendly, or fuel-efficient. This program makes commuting and traveling more engaging, enjoyable, and tailored to individual needs.

Programmer
Denzel Osei

Content

Input page for origin and destination

Options for route type: fastest, scenic, beginner-friendly, fuel-efficient

Visual display of the route (optional map integration)

Estimated travel times and directions

Routes adapt to user preferences for safety, fun, or efficiency

Goals

Ensure the program calculates routes correctly

Provide options tailored to different user types (older adults, new drivers, commuters)

Create a user-friendly interface

Test routes using Google Maps API

Inspiration

Python Route Planner by aram-ap

Route Planner by Lucassuryana

Route Optimization in Python - NeuronLab YouTube Tutorial
