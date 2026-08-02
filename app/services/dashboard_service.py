from collections import defaultdict

from app.models import Membership


# =====================================================
# USER DASHBOARD
# =====================================================

def get_user_dashboard(user):

    memberships = Membership.query.filter_by(
        user_id=user.id
    ).all()

    grouped = defaultdict(list)

    for membership in memberships:

        league = membership.league

        if league.is_archived:
            continue

        season = league.season

        grouped[season.id].append({

            "season": season,

            "league": league,

            "membership": membership

        })

    return grouped