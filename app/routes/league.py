from flask import Blueprint, render_template, request, redirect, session
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import pytz
import secrets

from app import db
from app.models import League, Membership, Game, Pick, User, Invite
from app.services.live_service import build_live_context
from app.services.game_service import is_game_locked, game_started
from app.services.email_service import send_invite_email


league_bp = Blueprint("league", __name__)


# =========================
# DASHBOARD
# =========================

@league_bp.route("/")
@login_required
def dashboard():

    mexico = pytz.timezone("America/Mexico_City")

    memberships = Membership.query.filter_by(
        user_id=current_user.id
    ).all()

    leagues_data = []

    for m in memberships:

        league = League.query.get(m.league_id)

        # =========================
        # PLAYER COUNT
        # =========================

        player_count = Membership.query.filter_by(
            league_id=league.id
        ).count()

        # =========================
        # LIVE GAMES
        # =========================

        games = Game.query.filter_by(
            sport=league.sport
        ).all()

        live_games = 0

        for g in games:

            if not g.status:
                continue

            status = g.status.lower()

            if "final" in status:
                continue

            if "scheduled" in status:
                continue

            live_games += 1

        # =========================
        # RANKING
        # =========================

        members = Membership.query.filter_by(
            league_id=league.id
        ).all()

        scores = []

        for member in members:

            picks = Pick.query.filter_by(
                user_id=member.user_id,
                league_id=league.id
            ).all()

            pts = 0

            for pick in picks:

                game = Game.query.get(pick.game_id)

                if not game or not game.result:
                    continue

                if game.sport == "NBA":

                    if pick.choice == game.result:
                        pts += 1

                else:

                    diff = abs(
                        (game.home_score or 0) -
                        (game.away_score or 0)
                    )

                    if diff < 7 and pick.choice == "DIFFERENCE":
                        pts += 1

                    elif diff >= 7:

                        if game.home_score > game.away_score and pick.choice == "HOME7":
                            pts += 1

                        elif game.away_score > game.home_score and pick.choice == "AWAY7":
                            pts += 1

            scores.append({
                "user": member.user_id,
                "points": pts
            })

        scores.sort(key=lambda x: x["points"], reverse=True)

        rank = 1

        for s in scores:

            if s["user"] == current_user.id:
                break

            rank += 1

        top_players = []

        for i, s in enumerate(scores[:3]):

            user = User.query.get(s["user"])

            top_players.append({
                "rank": i + 1,
                "name": user.name,
                "points": s["points"]
            })

        leagues_data.append({
            "league": league,
            "players": player_count,
            "live_games": live_games,
            "rank": rank,
            "top": top_players
        })

    return render_template(
        "dashboard.html",
        leagues=leagues_data
    )


# =========================
# CREATE LEAGUE
# =========================

@league_bp.route("/create_league", methods=["POST"])
@login_required
def create_league():

    league_name = request.form.get("league_name")
    sport = request.form.get("sport")

    league = League(
        name=league_name,
        sport=sport,
        owner_id=current_user.id
    )

    db.session.add(league)
    db.session.commit()

    membership = Membership(
        user_id=current_user.id,
        league_id=league.id
    )

    db.session.add(membership)
    db.session.commit()

    return redirect("/")


# =========================
# VIEW LEAGUE (PICKS)
# =========================

@league_bp.route("/league/<int:league_id>")
@login_required
def view_league(league_id):

    mexico = pytz.timezone("America/Mexico_City")

    league = League.query.get_or_404(league_id)

    games = Game.query.filter_by(
        sport=league.sport
    ).all()

    games_grouped = {}
    active_week = None

    # =========================
    # NFL
    # =========================

    if league.sport == "NFL":

        weeks = sorted({g.week for g in games if g.week})

        selected_week = request.args.get("week")

        try:
            selected_week = int(selected_week) if selected_week else None
        except:
            selected_week = None

        if not selected_week:
            selected_week = weeks[0] if weeks else None

        week_games = [g for g in games if g.week == selected_week]

        temp = []

        for g in week_games:

            try:
                game_time = datetime.fromisoformat(
                    g.game_date.replace("Z","+00:00")
                ).astimezone(mexico)

                temp.append((g, game_time))

            except:
                continue

        temp.sort(key=lambda x: x[1])

        games_grouped[f"Semana {selected_week}"] = temp

        active_week = selected_week

    # =========================
    # NBA
    # =========================

    else:

        today = datetime.now(mexico).date()
        tomorrow = today + timedelta(days=1)

        temp = []

        for g in games:

            try:

                game_time = datetime.fromisoformat(
                    g.game_date.replace("Z","+00:00")
                ).astimezone(mexico)

                if game_time.date() in [today, tomorrow]:
                    temp.append((g, game_time))

            except:
                continue

        temp.sort(key=lambda x: x[1])

        for g, t in temp:

            day = t.strftime("%A %d %B")

            games_grouped.setdefault(day, []).append((g, t))

    my_picks = Pick.query.filter_by(
        user_id=current_user.id,
        league_id=league_id
    ).all()

    my_picks_map = {p.game_id: p.choice for p in my_picks}

    return render_template(
        "league_picks.html",
        league=league,
        games_grouped=games_grouped,
        my_picks=my_picks_map,
        is_game_locked=is_game_locked,
        active_week=active_week
    )


# =========================
# INVITE USER
# =========================

@league_bp.route("/invite/<int:league_id>", methods=["POST"])
@login_required
def invite_user(league_id):

    email = request.form.get("email")

    token = secrets.token_urlsafe(32)

    invite = Invite(
        email=email,
        league_id=league_id,
        token=token
    )

    db.session.add(invite)
    db.session.commit()

    invite_link = f"http://localhost:5000/join/{token}"

    send_invite_email(email, invite_link)

    return redirect(f"/league/{league_id}")


# =========================
# ACCEPT INVITE
# =========================

@league_bp.route("/join/<token>")
def join_league(token):

    invite = Invite.query.filter_by(token=token).first()

    if not invite or invite.used:
        return "Invite invalid"

    if current_user.is_authenticated:

        existing = Membership.query.filter_by(
            user_id=current_user.id,
            league_id=invite.league_id
        ).first()

        if not existing:

            membership = Membership(
                user_id=current_user.id,
                league_id=invite.league_id
            )

            db.session.add(membership)

        invite.used = True
        db.session.commit()

        return redirect(f"/league/{invite.league_id}")

    session["invite_token"] = token

    existing_user = User.query.filter_by(email=invite.email).first()

    if existing_user:
        return redirect("/login")

    return redirect("/register")


# =========================
# SAVE PICKS
# =========================

@league_bp.route("/submit_picks/<int:league_id>", methods=["POST"])
@login_required
def submit_picks(league_id):

    league = League.query.get_or_404(league_id)

    games = Game.query.filter_by(
        sport=league.sport
    ).all()

    for game in games:

        choice = request.form.get(f"game{game.id}")

        if choice:

            existing = Pick.query.filter_by(
                user_id=current_user.id,
                game_id=game.id,
                league_id=league_id
            ).first()

            if existing:
                existing.choice = choice
            else:

                pick = Pick(
                    user_id=current_user.id,
                    league_id=league_id,
                    game_id=game.id,
                    choice=choice
                )

                db.session.add(pick)

    db.session.commit()

    return {"status": "success"}


# =========================
# LIVE
# =========================

@league_bp.route("/league/<int:league_id>/live")
@login_required
def league_live(league_id):

    mexico = pytz.timezone("America/Mexico_City")

    league = League.query.get_or_404(league_id)

    if league.sport == "NFL":

        games = Game.query.filter_by(sport="NFL").all()

        weeks = sorted({g.week for g in games if g.week})

        selected_week = request.args.get("week")

        try:
            selected_week = int(selected_week) if selected_week else None
        except:
            selected_week = None

        if not selected_week:
            selected_week = weeks[-1] if weeks else None

        base_games = [g for g in games if g.week == selected_week]

        days = None
        selected_day = None

    else:

        games = Game.query.filter_by(sport="NBA").all()

        today = datetime.now(mexico).date()

        selected_day = request.args.get("day")

        if selected_day:

            try:
                selected_day = datetime.fromisoformat(selected_day).date()
            except:
                selected_day = today

        else:
            selected_day = today

        base_games = []

        for g in games:

            try:

                t = datetime.fromisoformat(
                    g.game_date.replace("Z","+00:00")
                ).astimezone(mexico)

                if t.date() == selected_day:
                    base_games.append(g)

            except:
                continue

        days = [(today + timedelta(days=i)) for i in range(-3,4)]
        weeks = None

    users, live_matrix, scores, pick_distribution, clutch_game = build_live_context(
        league_id,
        base_games,
        current_user.id
    )

    return render_template(
        "league_live.html",
        league=league,
        users=users,
        live_games=base_games,
        live_matrix=live_matrix,
        scores=scores,
        selected_day=selected_day,
        clutch_game=clutch_game,
        pick_distribution=pick_distribution,
        days=days,
        weeks=weeks,
        selected_week=selected_week if league.sport == "NFL" else None
    )


# =========================
# LIVE UPDATE
# =========================

@league_bp.route("/league/<int:league_id>/live_update")
@login_required
def live_update(league_id):

    mexico = pytz.timezone("America/Mexico_City")

    league = League.query.get_or_404(league_id)

    if league.sport == "NFL":

        games = Game.query.filter_by(sport="NFL").all()

        weeks = sorted({g.week for g in games if g.week})

        selected_week = request.args.get("week")

        try:
            selected_week = int(selected_week) if selected_week else None
        except:
            selected_week = None

        if not selected_week:
            selected_week = weeks[-1] if weeks else None

        base_games = [g for g in games if g.week == selected_week]

    else:

        games = Game.query.filter_by(sport="NBA").all()

        today = datetime.now(mexico).date()

        selected_day = request.args.get("day")

        if selected_day:

            try:
                selected_day = datetime.fromisoformat(selected_day).date()
            except:
                selected_day = today

        else:
            selected_day = today

        base_games = []

        for g in games:

            try:

                t = datetime.fromisoformat(
                    g.game_date.replace("Z","+00:00")
                ).astimezone(mexico)

                if t.date() == selected_day:
                    base_games.append(g)

            except:
                continue

    users, live_matrix, scores, pick_distribution, clutch_game = build_live_context(
        league_id,
        base_games,
        current_user.id
    )

    return render_template(
        "live_table.html",
        users=users,
        live_games=base_games,
        live_matrix=live_matrix,
        scores=scores,
        pick_distribution=pick_distribution,
        clutch_game=clutch_game
    )


# =========================
# LEADERBOARD
# =========================

@league_bp.route("/leaderboard/<int:league_id>")
@login_required
def leaderboard(league_id):

    league = League.query.get_or_404(league_id)

    memberships = Membership.query.filter_by(
        league_id=league_id
    ).all()

    scores = []

    for m in memberships:

        user = User.query.get(m.user_id)

        picks = Pick.query.filter_by(
            user_id=user.id,
            league_id=league_id
        ).all()

        points = 0

        for pick in picks:

            game = Game.query.get(pick.game_id)

            if not game or not game.result:
                continue

            if game.sport == "NBA":

                if pick.choice == game.result:
                    points += 1

            else:

                if game.home_score is None or game.away_score is None:
                    continue

                diff = abs(game.home_score - game.away_score)

                if diff < 7:

                    if pick.choice == "DIFFERENCE":
                        points += 1

                else:

                    if game.home_score > game.away_score:

                        if "HOME" in pick.choice:
                            points += 1

                    else:

                        if "AWAY" in pick.choice:
                            points += 1

        scores.append({
            "name": user.name,
            "points": points
        })

    scores.sort(
        key=lambda x: x["points"],
        reverse=True
    )

    return render_template(
        "leaderboard.html",
        scores=scores,
        league=league
    )