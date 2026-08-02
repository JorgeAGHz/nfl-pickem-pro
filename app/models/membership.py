from datetime import datetime

from app.extensions import db
from app.constants import ROLE_MEMBER

class Membership(db.Model):

    __tablename__ = "memberships"
    
    __table_args__ = (

        db.UniqueConstraint(
            "user_id",
            "league_id",
            name="uq_membership_user_league"
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

    role = db.Column(
        db.String(20),
        nullable=False,
        default=ROLE_MEMBER
    )

    joined_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f"<Membership user={self.user_id} league={self.league_id}>"