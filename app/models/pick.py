from datetime import datetime

from app.extensions import db


class Pick(db.Model):

    __tablename__ = "picks"


    __table_args__ = (

        db.UniqueConstraint(
            "user_id",
            "league_id",
            "game_id",
            name="uq_pick_user_league_game"
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    league_id = db.Column(
        db.Integer,
        db.ForeignKey("leagues.id"),
        nullable=False,
        index=True
    )

    game_id = db.Column(
        db.Integer,
        db.ForeignKey("games.id"),
        nullable=False,
        index=True
    )

    selection = db.Column(
        db.String(20),
        nullable=False
    )

    is_correct = db.Column(
        db.Boolean,
        nullable=True
    )

    submitted_at = db.Column(
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
        return (
            f"<Pick user={self.user_id} "
            f"game={self.game_id}>"
        )