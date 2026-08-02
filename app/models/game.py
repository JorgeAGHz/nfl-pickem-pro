from datetime import datetime

from app.extensions import db


class Game(db.Model):

    __tablename__ = "games"

    __table_args__ = (

        db.UniqueConstraint(
            "season_id",
            "api_id",
            name="uq_game_api_season"
        ),

        db.Index(
            "idx_game_week",
            "season_id",
            "week"
        ),

        db.Index(
            "idx_game_status",
            "status"
        ),

        db.Index(
            "idx_game_date",
            "game_date"
        ),

    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    season_id = db.Column(
        db.Integer,
        db.ForeignKey("seasons.id"),
        nullable=False,
        index=True
    )

    api_id = db.Column(
        db.String(50),
        nullable=False
    )

    home_team = db.Column(
        db.String(100),
        nullable=False
    )

    away_team = db.Column(
        db.String(100),
        nullable=False
    )

    home_abbr = db.Column(
        db.String(10),
        nullable=False
    )

    away_abbr = db.Column(
        db.String(10),
        nullable=False
    )

    home_logo = db.Column(
        db.String(255)
    )

    away_logo = db.Column(
        db.String(255)
    )

    game_date = db.Column(
        db.DateTime,
        nullable=False
    )

    week = db.Column(
        db.Integer,
        nullable=True
    )

    spread = db.Column(
        db.Float,
        nullable=True
    )

    home_odds = db.Column(
        db.Integer,
        nullable=True
    )

    away_odds = db.Column(
        db.Integer,
        nullable=True
    )

    home_score = db.Column(
        db.Integer,
        nullable=True
    )

    away_score = db.Column(
        db.Integer,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="SCHEDULED"
    )

    clock = db.Column(
        db.String(20),
        nullable=True
    )

    period = db.Column(
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
    
    season_type = db.Column(
        db.String(20),
        nullable=False,
        default="REGULAR"
    )

    picks = db.relationship(
        "Pick",
        backref="game",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Game {self.away_abbr} @ {self.home_abbr}>"