from datetime import datetime

from app.extensions import db


class League(db.Model):

    __tablename__ = "leagues"

    __table_args__ = (

        db.UniqueConstraint(
            "season_id",
            "name",
            name="uq_league_name_per_season"
        ),

        db.Index(
            "idx_league_archived",
            "is_archived"
        ),

    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    public_id = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        index=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    season_id = db.Column(
        db.Integer,
        db.ForeignKey("seasons.id"),
        nullable=False,
        index=True
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    invite_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True
    )

    rules_locked = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    is_archived = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    archived_at = db.Column(
        db.DateTime,
        nullable=True
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # ==========================================
    # RELATIONSHIPS
    # ==========================================

    settings = db.relationship(
        "LeagueSettings",
        backref="league",
        uselist=False,
        cascade="all, delete-orphan"
    )

    memberships = db.relationship(
        "Membership",
        backref="league",
        lazy=True,
        cascade="all, delete-orphan"
    )

    invites = db.relationship(
        "Invite",
        backref="league",
        lazy=True,
        cascade="all, delete-orphan"
    )

    picks = db.relationship(
        "Pick",
        backref="league",
        lazy=True,
        cascade="all, delete-orphan"
    )

    weekly_results = db.relationship(
        "LeagueWeekResult",
        backref="league",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):

        return (
            f"<League "
            f"id={self.id} "
            f"name='{self.name}' "
            f"season_id={self.season_id}>"
        )