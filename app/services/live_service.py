from datetime import datetime
import pytz

from app.models import User, Membership, Pick
from app.services.game_service import game_started


def build_live_context(league_id, games, viewer_id):

    mexico = pytz.timezone("America/Mexico_City")

    memberships = Membership.query.filter_by(
        league_id=league_id
    ).all()

    users = [User.query.get(m.user_id) for m in memberships]

    all_picks = Pick.query.filter_by(
        league_id=league_id
    ).all()

    picks_map = {
        (p.user_id, p.game_id): p.choice
        for p in all_picks
    }

    live_matrix = {}
    scores = {}

    # =========================
    # PICK DISTRIBUTION
    # =========================

    pick_distribution = {}

    for g in games:

        counts = {
            "home":0,
            "away":0,
            "diff":0
        }

        for p in all_picks:

            if p.game_id != g.id:
                continue

            if p.choice == g.home_team:
                counts["home"] += 1

            elif p.choice == g.away_team:
                counts["away"] += 1

            elif g.sport == "NFL" and p.choice == "DIFFERENCE":
                counts["diff"] += 1

        pick_distribution[g.id] = counts

    # =========================
    # CLUTCH GAME
    # =========================

    clutch_game = None
    max_picks = 0

    for g in games:

        counts = pick_distribution.get(g.id)

        total = counts["home"] + counts["away"] + counts["diff"]

        if total > max_picks:

            max_picks = total
            clutch_game = g.id

    for u in users:

        live_matrix[u.id] = {}
        pts = 0

        for g in games:

            pick = picks_map.get((u.id, g.id))

            # =========================
            # GAME NOT STARTED
            # =========================

            if not game_started(g):

                if u.id == viewer_id:

                    if pick == g.home_team:
                        display = g.home_logo

                    elif pick == g.away_team:
                        display = g.away_logo

                    elif pick == "DIFFERENCE":
                        display = "D"

                    else:
                        display = "-"

                else:
                    display = "-"

                live_matrix[u.id][g.id] = {
                    "display": display,
                    "correct": None
                }

                continue

            # =========================
            # GAME STARTED BUT NOT FINAL
            # =========================

            if not g.status or "final" not in g.status.lower():

                if pick == g.home_team:
                    display = g.home_logo

                elif pick == g.away_team:
                    display = g.away_logo

                elif pick == "DIFFERENCE":
                    display = "D"

                else:
                    display = "-"

                live_matrix[u.id][g.id] = {
                    "display": display,
                    "correct": None
                }

                continue

            # =========================
            # FINAL RESULT
            # =========================

            if not pick:

                live_matrix[u.id][g.id] = {
                    "display": "-",
                    "correct": None
                }

                continue

            if g.sport == "NBA":

                correct = (pick == g.result)

                display = g.home_logo if pick == g.home_team else g.away_logo

            else:

                diff = abs((g.home_score or 0) - (g.away_score or 0))

                if pick == "DIFFERENCE":
                    display = "D"

                elif pick == "HOME7":
                    display = g.home_logo

                elif pick == "AWAY7":
                    display = g.away_logo

                else:
                    display = "-"

                if diff < 7:
                    correct = (pick == "DIFFERENCE")

                elif g.home_score > g.away_score:
                    correct = (pick == "HOME7")

                else:
                    correct = (pick == "AWAY7")

            live_matrix[u.id][g.id] = {
                "display": display,
                "correct": correct
            }

            if correct:
                pts += 1

        scores[u.id] = pts

    return users, live_matrix, scores, pick_distribution, clutch_game