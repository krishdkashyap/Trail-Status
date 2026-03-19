import os
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from models import db, Trail, User, TrailReport
from weather import get_trail_weather, calculate_trail_status

load_dotenv()

app = Flask(__name__)

# Secret key is required for sessions and flash messages
# In production this should be a long random string stored in .env
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trails.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
csrf = CSRFProtect(app)  # automatically protects all POST forms

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = "login"          # redirect here if @login_required fails
login_manager.login_message = "Please log in to access the admin panel."


@login_manager.user_loader
def load_user(user_id):
    """Tells Flask-Login how to find a user by ID (stored in the session cookie)."""
    return db.session.get(User, int(user_id))


# ================================================================
#  Public routes — no login needed
# ================================================================

@app.route("/")
def home():
    """Homepage — live weather status for every trail + recent reports."""
    trails = Trail.query.all()
    trails_with_status = []

    OVERRIDE_STATUS = {
        "open":    {"label": "Open",    "color": "green",  "icon": "🟢",
                    "precip_24h": None, "precip_72h": None, "soil_moisture": None, "freeze_thaw": None},
        "caution": {"label": "Caution", "color": "orange", "icon": "🟡",
                    "precip_24h": None, "precip_72h": None, "soil_moisture": None, "freeze_thaw": None},
        "closed":  {"label": "Closed",  "color": "red",    "icon": "🔴",
                    "precip_24h": None, "precip_72h": None, "soil_moisture": None, "freeze_thaw": None},
    }

    for trail in trails:
        trail_dict = trail.to_dict()

        # If admin has set a manual override, use it — skip the weather API
        if trail.status_override and trail.status_override in OVERRIDE_STATUS:
            status = {**OVERRIDE_STATUS[trail.status_override], "override": True}
        else:
            weather_data = get_trail_weather(trail_dict["lat"], trail_dict["lon"])
            status = {**calculate_trail_status(trail_dict, weather_data), "override": False}

        recent_reports = trail.reports[:3]

        trails_with_status.append({
            **trail_dict,
            **status,
            "status_override": trail.status_override,
            "reports": recent_reports,
        })

    return render_template("index.html", trails=trails_with_status)


@app.route("/trail/<int:trail_id>")
def trail_detail(trail_id):
    """Detail page for a single trail — full description, weather, and all reports."""
    trail = Trail.query.get_or_404(trail_id)
    trail_dict = trail.to_dict()
    trail_dict["long_description"] = trail.long_description
    trail_dict["status_override"] = trail.status_override

    OVERRIDE_STATUS = {
        "open":    {"label": "Open",    "color": "green",  "icon": "🟢",
                    "precip_24h": None, "precip_72h": None, "soil_moisture": None, "freeze_thaw": None},
        "caution": {"label": "Caution", "color": "orange", "icon": "🟡",
                    "precip_24h": None, "precip_72h": None, "soil_moisture": None, "freeze_thaw": None},
        "closed":  {"label": "Closed",  "color": "red",    "icon": "🔴",
                    "precip_24h": None, "precip_72h": None, "soil_moisture": None, "freeze_thaw": None},
    }

    if trail.status_override and trail.status_override in OVERRIDE_STATUS:
        status = {**OVERRIDE_STATUS[trail.status_override], "override": True}
    else:
        weather_data = get_trail_weather(trail_dict["lat"], trail_dict["lon"])
        status = {**calculate_trail_status(trail_dict, weather_data), "override": False}

    return render_template("trail_detail.html",
                           trail={**trail_dict, **status},
                           reports=trail.reports)


@app.route("/report", methods=["POST"])
def post_report():
    """Anyone can post a trail condition report — no login needed."""
    trail_id  = request.form.get("trail_id")
    author    = request.form.get("author", "").strip() or "Anonymous"
    condition = request.form.get("condition")
    body      = request.form.get("body", "").strip()

    if not trail_id or not condition or not body:
        flash("Please fill out all fields.", "error")
        return redirect(url_for("home"))

    report = TrailReport(
        trail_id  = int(trail_id),
        author    = author,
        condition = condition,
        body      = body,
    )
    db.session.add(report)
    db.session.commit()
    flash("Report submitted — thanks for the update!", "success")
    return redirect(url_for("home"))


# ================================================================
#  Auth routes — login / logout
# ================================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    """Admin login page."""
    if current_user.is_authenticated:
        return redirect(url_for("admin"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("admin"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


# ================================================================
#  Admin routes — login required
# ================================================================

@app.route("/admin")
@login_required
def admin():
    """Admin dashboard — view all trails and recent reports."""
    trails = Trail.query.all()
    reports = TrailReport.query.order_by(TrailReport.created_at.desc()).limit(20).all()
    return render_template("admin.html", trails=trails, reports=reports)


@app.route("/admin/add", methods=["GET", "POST"])
@login_required
def add_trail():
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
        flash(f"Trail '{trail.name}' added.", "success")
        return redirect(url_for("admin"))

    return render_template("add_trail.html")


@app.route("/admin/edit/<int:trail_id>", methods=["GET", "POST"])
@login_required
def edit_trail(trail_id):
    trail = Trail.query.get_or_404(trail_id)

    if request.method == "POST":
        trail.name             = request.form["name"]
        trail.location         = request.form["location"]
        trail.difficulty       = request.form["difficulty"]
        trail.length           = request.form["length"]
        trail.soil             = request.form["soil"]
        trail.drainage         = request.form["drainage"]
        trail.lat              = float(request.form["lat"])
        trail.lon              = float(request.form["lon"])
        trail.description      = request.form["description"]
        trail.long_description = request.form.get("long_description", "").strip() or None
        db.session.commit()
        flash(f"Trail '{trail.name}' updated.", "success")
        return redirect(url_for("admin"))

    return render_template("edit_trail.html", trail=trail)


@app.route("/admin/delete/<int:trail_id>", methods=["POST"])
@login_required
def delete_trail(trail_id):
    trail = Trail.query.get_or_404(trail_id)
    db.session.delete(trail)
    db.session.commit()
    flash(f"Trail '{trail.name}' deleted.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/trail/<int:trail_id>/override", methods=["POST"])
@login_required
def set_override(trail_id):
    """Set or clear a manual status override for a trail."""
    trail = Trail.query.get_or_404(trail_id)
    override = request.form.get("status_override") or None  # empty string → None
    trail.status_override = override
    db.session.commit()
    label = override.capitalize() if override else "cleared"
    flash(f"{trail.name} status override {label}.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/report/delete/<int:report_id>", methods=["POST"])
@login_required
def delete_report(report_id):
    """Admin can delete any report."""
    report = TrailReport.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash("Report deleted.", "success")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)
