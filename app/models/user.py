from datetime import datetime

from flask_login import UserMixin

from app.extensions import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    email_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    verification_token = db.Column(
        db.String(255),
        nullable=True,
        unique=True
    )

    reset_token = db.Column(
        db.String(255),
        nullable=True,
        unique=True
    )

    reset_token_expires = db.Column(
        db.DateTime,
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

    memberships = db.relationship(
        "Membership",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    picks = db.relationship(
        "Pick",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    owned_leagues = db.relationship(
        "League",
        foreign_keys="League.owner_id",
        lazy=True
    )

    def __repr__(self):
        return f"<User {self.email}>"
    
