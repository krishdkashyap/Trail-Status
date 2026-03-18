"""
seed.py — Populate the database with the initial trail data

Run this once to migrate the hardcoded trails into SQLite:
    python seed.py

Safe to re-run — it checks if trails already exist before inserting.
"""

from app import app
from models import db, Trail

# Pre-computed center coordinates for each trail
# (previously calculated by get_center() in app.py)
TRAILS = [
    {
        "name":        "Salem Lake Trail",
        "location":    "Winston-Salem, NC",
        "difficulty":  "Beginner",
        "length":      "7.0 miles",
        "soil":        "Hard-packed dirt",
        "drainage":    "good",
        "lat":         36.045,
        "lon":         -80.21,
        "description": (
            "A 7-mile loop on wide doubletrack following the perimeter of Salem Lake. "
            "Great for beginners and families. Shared with walkers and runners."
        ),
    },
    {
        "name":        "Salem Lake North Side",
        "location":    "Winston-Salem, NC",
        "difficulty":  "Intermediate",
        "length":      "3.8 miles",
        "soil":        "Loam and dirt",
        "drainage":    "moderate",
        "lat":         36.1045,
        "lon":         -80.1775,
        "description": (
            "Flowing singletrack with technical features, a mini jump park, and wooded sections. "
            "More challenging than the main lake loop."
        ),
    },
    {
        "name":        "Hobby Park",
        "location":    "Winston-Salem, NC",
        "difficulty":  "Intermediate / Advanced",
        "length":      "7.0 miles",
        "soil":        "Clay, roots, sand",
        "drainage":    "poor",
        "lat":         36.035,
        "lon":         -80.3025,
        "description": (
            "The local XC race course. Roots, rocks, creek crossings, berms, and open fields. "
            "Flowy and fast in places but punishing when wet."
        ),
    },
    {
        "name":        "The Ridge Cycle Hub",
        "location":    "Lexington, NC",
        "difficulty":  "Intermediate / Advanced",
        "length":      "6.7 miles",
        "soil":        "Packed dirt, loam",
        "drainage":    "good",
        "lat":         35.8675,
        "lon":         -80.2095,
        "description": (
            "Rollercoaster drops and climbs with Pisgah-like terrain and City Lake views. "
            "Great flow, rewarding climbs, and well-built berms. One-way trail."
        ),
    },
    {
        "name":        "Back Yard Trails (BYT)",
        "location":    "Charlotte, NC",
        "difficulty":  "Advanced / Expert",
        "length":      "11.4 miles",
        "soil":        "Clay, roots, rock",
        "drainage":    "poor",
        "lat":         35.152,
        "lon":         -80.8575,
        "description": (
            "A technical gem in Charlotte with rock gardens, drops, jumps, and creek crossings. "
            "Exponentially harder when wet. Closes 24 hours after rain."
        ),
    },
]


def seed():
    with app.app_context():
        db.create_all()  # creates the table if it doesn't exist yet

        added = 0
        for data in TRAILS:
            # Check if this trail already exists so we don't add duplicates
            exists = Trail.query.filter_by(name=data["name"]).first()
            if not exists:
                trail = Trail(**data)
                db.session.add(trail)
                added += 1

        db.session.commit()
        print(f"Done — {added} trail(s) added, {len(TRAILS) - added} already existed.")


if __name__ == "__main__":
    seed()
