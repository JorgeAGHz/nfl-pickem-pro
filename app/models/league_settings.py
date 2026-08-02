from datetime import datetime

from app.extensions import db


class LeagueSettings(db.Model):

    __tablename__ = "league_settings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    league_id = db.Column(
        db.Integer,
        db.ForeignKey("leagues.id"),
        unique=True,
        nullable=False
    )

    pick_mode = db.Column(
        db.String(30),
        nullable=False
    )

    include_playoffs = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    visibility = db.Column(
        db.String(20),
        default="PRIVATE",
        nullable=False
    )

    max_players = db.Column(
        db.Integer,
        default=100,
        nullable=False
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

    def __repr__(self):
        return f"<LeagueSettings {self.league_id}>"