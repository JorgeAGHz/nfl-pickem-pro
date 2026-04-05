from app.extensions import db
from flask_login import UserMixin


# =========================
# USER
# =========================

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

    is_admin = db.Column(db.Boolean, default=False)


# =========================
# LEAGUE
# =========================

class League(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    sport = db.Column(db.String(20))

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    invite_code = db.Column(
        db.String(10),
        unique=True
    )


# =========================
# MEMBERSHIP
# =========================

class Membership(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    league_id = db.Column(
        db.Integer,
        db.ForeignKey("league.id")
    )


# =========================
# INVITES
# =========================

class Invite(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120))

    league_id = db.Column(
        db.Integer,
        db.ForeignKey("league.id")
    )

    token = db.Column(
        db.String(200),
        unique=True
    )

    used = db.Column(
        db.Boolean,
        default=False
    )


# =========================
# GAMES
# =========================

class Game(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    api_id = db.Column(db.String(50))

    sport = db.Column(db.String(10))

    home_team = db.Column(db.String(100))
    away_team = db.Column(db.String(100))

    home_abbr = db.Column(db.String(10))
    away_abbr = db.Column(db.String(10))

    home_logo = db.Column(db.String(255))
    away_logo = db.Column(db.String(255))

    game_date = db.Column(db.String(50))

    week = db.Column(db.Integer)

    spread = db.Column(db.Float)
    spread = db.Column(db.Float)
    home_odds = db.Column(db.Integer)
    away_odds = db.Column(db.Integer)

    result = db.Column(db.String(50))

    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)

    status = db.Column(db.String(50))
    clock = db.Column(db.String(20))
    period = db.Column(db.Integer)


# =========================
# PICKS
# =========================

class Pick(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    league_id = db.Column(
        db.Integer,
        db.ForeignKey("league.id")
    )

    game_id = db.Column(
        db.Integer,
        db.ForeignKey("game.id")
    )

    choice = db.Column(db.String(50))