"""
models.py — Database models for Trail Status

Flask-SQLAlchemy lets us define database tables as Python classes.
Each class = one table. Each attribute = one column.

Current models:
  - Trail       — a mountain bike trail
  - User        — an admin user (login required to access /admin)
  - TrailReport — a condition report posted by anyone (no login needed)
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# db is the database instance — imported in app.py, seed.py, create_admin.py
db = SQLAlchemy()


class Trail(db.Model):
    """
    Represents one trail in the database.
    Each Trail instance = one row in the 'trail' table.
    """

    __tablename__ = "trail"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    location    = db.Column(db.String(100), nullable=False)
    difficulty  = db.Column(db.String(50),  nullable=False)
    length      = db.Column(db.String(20),  nullable=False)
    soil        = db.Column(db.String(100), nullable=False)
    drainage    = db.Column(db.String(20),  nullable=False)  # good / moderate / poor
    description = db.Column(db.Text,        nullable=False)
    lat              = db.Column(db.Float, nullable=False)   # center lat for weather API
    lon              = db.Column(db.Float, nullable=False)   # center lon for weather API
    long_description = db.Column(db.Text,  nullable=True)    # full trail description

    # Admin can manually override the weather-based status
    # None = use weather logic   "open" / "caution" / "closed" = manual override
    status_override = db.Column(db.String(20), nullable=True, default=None)

    # One trail can have many reports
    reports     = db.relationship("TrailReport", backref="trail", lazy=True,
                                  order_by="TrailReport.created_at.desc()")

    def to_dict(self):
        """Convert a Trail row into a plain dictionary — used in app.py routes."""
        return {
            "id":          self.id,
            "name":        self.name,
            "location":    self.location,
            "difficulty":  self.difficulty,
            "length":      self.length,
            "soil":        self.soil,
            "drainage":    self.drainage,
            "description": self.description,
            "lat":         self.lat,
            "lon":         self.lon,
        }

    def __repr__(self):
        return f"<Trail {self.id}: {self.name}>"


class User(UserMixin, db.Model):
    """
    Admin user — only admins need accounts right now.
    UserMixin gives Flask-Login the methods it needs (is_authenticated, etc.)
    Passwords are hashed — we never store plain text passwords.
    """

    __tablename__ = "user"

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        """Hash and store a password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Return True if the given password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class TrailReport(db.Model):
    """
    A condition report posted by anyone — no login required.
    Linked to a specific trail via trail_id (foreign key).
    """

    __tablename__ = "trail_report"

    id         = db.Column(db.Integer, primary_key=True)
    trail_id   = db.Column(db.Integer, db.ForeignKey("trail.id"), nullable=False)
    author     = db.Column(db.String(50),  nullable=False, default="Anonymous")
    condition  = db.Column(db.String(20),  nullable=False)  # dry / muddy / wet / closed
    body       = db.Column(db.Text,        nullable=False)
    created_at = db.Column(db.DateTime,    nullable=False,
                           default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<TrailReport {self.id} — Trail {self.trail_id}>"
