from datetime import datetime

from app.extensions import db


class Invite(db.Model):

    __tablename__ = "invites"

    __table_args__ = (

        db.Index(
            "idx_invite_league_email",
            "league_id",
            "email"
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

    email = db.Column(
        db.String(120),
        nullable=False,
        index=True
    )

    token = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=True
    )

    accepted_at = db.Column(
        db.DateTime,
        nullable=True
    )

    used = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    def __repr__(self):
        return f"<Invite {self.email}>"