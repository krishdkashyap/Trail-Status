import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from models import db, Trail
from weather import get_trail_weather, calculate_trail_status

load_dotenv()

app = Flask(__name__)

# SQLite database file lives at instance/trails.db (auto-created by Flask)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trails.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # suppresses a noisy warning

db.init_app(app)


@app.route("/")
def home():
    """
    Homepage — fetch every trail from the database, get live weather for each,
    and render the trail cards.
    """
    trails = Trail.query.all()
    trails_with_status = []

    for trail in trails:
        trail_dict = trail.to_dict()
        weather_data = get_trail_weather(trail_dict["lat"], trail_dict["lon"])
        status = calculate_trail_status(trail_dict, weather_data)

        trails_with_status.append({**trail_dict, **status})

    return render_template("index.html", trails=trails_with_status)


@app.route("/admin")
def admin():
    """Admin page — view all trails in the database."""
    trails = Trail.query.all()
    return render_template("admin.html", trails=trails)


@app.route("/admin/add", methods=["GET", "POST"])
def add_trail():
    """
    GET  — show the add trail form
    POST — save the new trail to the database
    """
    if request.method == "POST":
        trail = Trail(
            name        = request.form["name"],
            location    = request.form["location"],
            difficulty  = request.form["difficulty"],
            length      = request.form["length"],
            soil        = request.form["soil"],
            drainage    = request.form["drainage"],
            lat         = float(request.form["lat"]),
            lon         = float(request.form["lon"]),
            description = request.form["description"],
        )
        db.session.add(trail)
        db.session.commit()
        return redirect(url_for("admin"))

    return render_template("add_trail.html")


@app.route("/admin/delete/<int:trail_id>", methods=["POST"])
def delete_trail(trail_id):
    """Delete a trail by ID."""
    trail = Trail.query.get_or_404(trail_id)
    db.session.delete(trail)
    db.session.commit()
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)
