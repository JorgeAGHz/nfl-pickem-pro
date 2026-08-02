from datetime import datetime

from app.extensions import db


class LeagueWeekResult(db.Model):

    __tablename__ = "league_week_results"

    __table_args__ = (

        db.UniqueConstraint(
            "league_id",
            "user_id",
            "week",
            name="uq_week_result"
        ),
    )
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    league_id = db.Column(
        db.Integer,
        db.ForeignKey("leagues.id"),
        nullable=False,
        index=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    week = db.Column(
        db.Integer,
        nullable=False
    )

    points = db.Column(
        db.Integer,
        nullable=False
    )

    rank = db.Column(
        db.Integer,
        nullable=False
    )

    closed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    season_id = db.Column(
        db.Integer,
        db.ForeignKey("seasons.id"),
        nullable=False,
        index=True
    )
    correct_picks = db.Column(
        db.Integer,
        nullable=False
    )
    def __repr__(self):
        return (
            f"<LeagueWeekResult "
            f"league={self.league_id} "
            f"week={self.week}>"
        )