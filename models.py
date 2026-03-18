"""
models.py — Database models for Trail Status

Flask-SQLAlchemy lets us define database tables as Python classes.
Each class = one table. Each attribute = one column.

SQLAlchemy is an ORM (Object Relational Mapper) — it translates between
Python objects and database rows so we never have to write raw SQL.
"""

from flask_sqlalchemy import SQLAlchemy

# db is the database instance — we import this in app.py and seed.py
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
    length      = db.Column(db.String(20),  nullable=False)   # e.g. "7.0 miles"
    soil        = db.Column(db.String(100), nullable=False)
    drainage    = db.Column(db.String(20),  nullable=False)   # good / moderate / poor
    description = db.Column(db.Text,        nullable=False)
    lat         = db.Column(db.Float,       nullable=False)   # center latitude for weather API
    lon         = db.Column(db.Float,       nullable=False)   # center longitude for weather API

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
        """How a Trail prints in the terminal — helpful for debugging."""
        return f"<Trail {self.id}: {self.name}>"
