from datetime import datetime

from app.extensions import db


class Season(db.Model):

    __tablename__ = "seasons"

    __table_args__ = (

        db.UniqueConstraint(
            "sport",
            "year",
            name="uq_season_sport_year"
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sport = db.Column(
        db.String(20),
        nullable=False,
        index=True
    )

    year = db.Column(
        db.Integer,
        nullable=False,
        index=True
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )

    current_week = db.Column(
        db.Integer,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    leagues = db.relationship(
        "League",
        backref="season",
        lazy=True
    )

    games = db.relationship(
        "Game",
        backref="season",
        lazy=True
    )

    def __repr__(self):
        return f"<Season {self.sport} {self.year}>"
    
