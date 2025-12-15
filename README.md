🚀 Project Overview

Opti-Route is a Python-based route planner that allows users to calculate driving routes between locations using OpenRouteService. The app supports different route preferences:

Fastest — quickest driving route

Scenic — avoids highways, prefers scenic roads

Beginner — beginner-friendly routes avoiding highways and tolls

Fuel-efficient — shortest route to save fuel

It also visualizes routes on an interactive map using Plotly.

💻 Features

Input addresses or latitude/longitude coordinates

Geocodes addresses automatically

Shows route on interactive map

Supports multiple driving preferences

Secure API key handling (stored in .env)

Simple web interface using Flask

🛠 Setup Instructions

Clone the repository

git clone <repo_url>
cd Opti-Route/OptiRouteProject


Create a .env file in the project root
Add your OpenRouteService API key:

ORS_API_KEY=your_api_key_here


⚠️ The .env file is ignored by GitHub for security reasons. Your key is never shared publicly.

Install dependencies

pip install -r requirements.txt


Run the Flask app

python app.py


Open your browser
Navigate to http://127.0.0.1:5000
 to start using Opti-Route.

🗺 How to Use

Enter an origin (address or coordinates)

Enter a destination (address or coordinates)

Select your preferred route type

Click Plan Route

See your route visualized on the interactive map

🔑 API Key Management

Uses python-dotenv to load the API key from .env

No key is stored in the repository

Users must add their own API key in .env for the app to work