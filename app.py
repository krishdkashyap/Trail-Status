import os
from flask import Flask, render_template
from dotenv import load_dotenv
from weather import get_trail_weather, calculate_trail_status

# Load values from .env file into the environment (API keys, debug flags, etc.)
load_dotenv()

app = Flask(__name__)

# TRAILS is a list of dicts — each dict holds one trail's data.
# Phase 2 goal: move this into a database so trails can be added/edited without touching code.
TRAILS = [
    {
        "id": 1,
        "name": "Salem Lake Trail",
        "location": "Winston-Salem, NC",
        "difficulty": "Beginner",
        "length": "7.0 miles",
        "soil": "Hard-packed dirt",
        "drainage": "good",
        "bbox_north": 36.0600,
        "bbox_south": 36.0300,
        "bbox_east":  -80.1900,
        "bbox_west":  -80.2300,
        "description": (
            "A 7-mile loop on wide doubletrack following the perimeter of Salem Lake. "
            "Great for beginners and families. Shared with walkers and runners."
        ),
    },
    {
        "id": 2,
        "name": "Salem Lake North Side",
        "location": "Winston-Salem, NC",
        "difficulty": "Intermediate",
        "length": "3.8 miles",
        "soil": "Loam and dirt",
        "drainage": "moderate",
        # This trail uses exact 4-corner coords instead of a standard bbox.
        # get_center() handles both formats automatically.
        "nw_lat": 36.112, "nw_lon": -80.195,
        "ne_lat": 36.112, "ne_lon": -80.160,
        "sw_lat": 36.092, "sw_lon": -80.195,
        "se_lat": 36.102, "se_lon": -80.160,
        "description": (
            "Flowing singletrack with technical features, a mini jump park, and wooded sections. "
            "More challenging than the main lake loop."
        ),
    },
    {
        "id": 3,
        "name": "Hobby Park",
        "location": "Winston-Salem, NC",
        "difficulty": "Intermediate / Advanced",
        "length": "7.0 miles",
        "soil": "Clay, roots, sand",
        "drainage": "poor",
        "bbox_north": 36.0500,
        "bbox_south": 36.0200,
        "bbox_east":  -80.2850,
        "bbox_west":  -80.3200,
        "description": (
            "The local XC race course. Roots, rocks, creek crossings, berms, and open fields. "
            "Flowy and fast in places but punishing when wet."
        ),
    },
    {
        "id": 4,
        "name": "The Ridge Cycle Hub",
        "location": "Lexington, NC",
        "difficulty": "Intermediate / Advanced",
        "length": "6.7 miles",
        "soil": "Packed dirt, loam",
        "drainage": "good",
        "nw_lat": 35.877, "nw_lon": -80.218,
        "ne_lat": 35.877, "ne_lon": -80.200,
        "se_lat": 35.858, "se_lon": -80.195,
        "sw_lat": 35.858, "sw_lon": -80.225,
        "description": (
            "Rollercoaster drops and climbs with Pisgah-like terrain and City Lake views. "
            "Great flow, rewarding climbs, and well-built berms. One-way trail."
        ),
    },
    {
        "id": 5,
        "name": "Back Yard Trails (BYT)",
        "location": "Charlotte, NC",
        "difficulty": "Advanced / Expert",
        "length": "11.4 miles",
        "soil": "Clay, roots, rock",
        "drainage": "poor",
        "bbox_north": 35.1580,
        "bbox_south": 35.1460,
        "bbox_east":  -80.8510,
        "bbox_west":  -80.8640,
        "description": (
            "A technical gem in Charlotte with rock gardens, drops, jumps, and creek crossings. "
            "Exponentially harder when wet. Closes 24 hours after rain."
        ),
    },
]


def get_center(trail):
    """
    Calculate a single (lat, lon) center point for a trail.
    Handles two formats:
      - Standard bounding box: bbox_north, bbox_south, bbox_east, bbox_west
      - Exact 4 corners:       nw_lat/lon, ne_lat/lon, sw_lat/lon, se_lat/lon
    The center point is passed to the weather API.
    """
    if "nw_lat" in trail:
        lat = (trail["nw_lat"] + trail["ne_lat"] + trail["sw_lat"] + trail["se_lat"]) / 4
        lon = (trail["nw_lon"] + trail["ne_lon"] + trail["sw_lon"] + trail["se_lon"]) / 4
    else:
        lat = (trail["bbox_north"] + trail["bbox_south"]) / 2
        lon = (trail["bbox_east"]  + trail["bbox_west"])  / 2
    return round(lat, 4), round(lon, 4)


@app.route("/")
def home():
    """
    Homepage — fetch live weather for every trail and render the trail cards.
    For each trail: get center coords → call Open-Meteo → calculate status → pass to template.
    """
    trails_with_status = []

    for trail in TRAILS:
        lat, lon = get_center(trail)
        weather_data = get_trail_weather(lat, lon)
        status = calculate_trail_status(trail, weather_data)

        trails_with_status.append({
            **trail,    # original trail fields
            **status,   # label, color, icon, precip_24h, precip_72h, soil_moisture, freeze_thaw
            "lat": lat,
            "lon": lon,
        })

    return render_template("index.html", trails=trails_with_status)


# Starts the local dev server.
# debug=True auto-reloads when you save a file and shows detailed errors in the browser.
# Change to False before going live.
if __name__ == "__main__":
    app.run(debug=True)
