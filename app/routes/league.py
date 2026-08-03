from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort
)

from flask_login import (
    login_required,
    current_user
)

from app.models import (
    Season
)

from app.constants import (
    SEASON_ACTIVE,
    SEASON_UPCOMING,

    PICK_MODE_NFL_SPREAD,
    PICK_MODE_NFL_WINNER,
    PICK_MODE_NBA_WINNER,

    VISIBILITY_PRIVATE,
    VISIBILITY_PUBLIC
)

from app.services.dashboard_service import (
    get_user_dashboard
)

from app.services.league_service import (

    create_league,

    join_league,

    get_league_by_public_id,

    get_league_preview_by_invite,

    is_member

)


league_bp = Blueprint(
    "league",
    __name__
)


# =====================================================
# DASHBOARD
# =====================================================

@league_bp.route("/")
@league_bp.route("/dashboard")
@login_required
def dashboard():

    grouped_leagues = get_user_dashboard(
        current_user
    )

    return render_template(
        "dashboard.html",
        grouped_leagues=grouped_leagues
    )


# =====================================================
# CREATE LEAGUE
# =====================================================

@league_bp.route(
    "/league/create",
    methods=["GET", "POST"]
)
@login_required
def create_league_view():

    seasons = Season.query.filter(
        Season.status.in_(
            [
                SEASON_ACTIVE,
                SEASON_UPCOMING
            ]
        )
    ).order_by(
        Season.sport,
        Season.year
    ).all()

    if request.method == "POST":

        try:

            league_name = request.form.get(
                "name",
                ""
            ).strip()

            season_id = int(
                request.form.get(
                    "season_id"
                )
            )

            pick_mode = request.form.get(
                "pick_mode"
            )

            include_playoffs = (
                request.form.get(
                    "include_playoffs"
                ) == "on"
            )

            visibility = request.form.get(
                "visibility"
            )

            season = Season.query.get(
                season_id
            )

            if not season:

                raise ValueError(
                    "Season not found."
                )

            league = create_league(

                owner=current_user,

                season=season,

                name=league_name,

                pick_mode=pick_mode,

                include_playoffs=include_playoffs,

                visibility=visibility

            )

            flash(
                "League created.",
                "success"
            )

            return redirect(

                url_for(

                    "league.league_home",

                    public_id=league.public_id

                )

            )

        except Exception as exc:

            flash(
                str(exc),
                "danger"
            )

    return render_template(

        "create_league.html",

        seasons=seasons,

        pick_modes=[

            PICK_MODE_NFL_SPREAD,

            PICK_MODE_NFL_WINNER,

            PICK_MODE_NBA_WINNER

        ],

        visibility_options=[

            VISIBILITY_PRIVATE,

            VISIBILITY_PUBLIC

        ]

    )


# =====================================================
# JOIN LEAGUE
# =====================================================

@league_bp.route(
    "/league/join",
    methods=["GET", "POST"]
)
@login_required
def join_league_view():

    if request.method == "POST":

        try:

            invite_code = (
                request.form.get(
                    "invite_code",
                    ""
                )
                .strip()
                .upper()
            )

            league = join_league(
                user=current_user,
                invite_code=invite_code
            )

            flash(
                "Joined league.",
                "success"
            )

            return redirect(
                url_for(
                    "league.league_home",
                    public_id=league.public_id
                )
            )

        except Exception as exc:

            flash(
                str(exc),
                "danger"
            )

    code = request.args.get(
        "code",
        ""
    ).strip().upper()

    preview = None

    if code:

        preview = get_league_preview_by_invite(
            code
        )

    return render_template(
        "join_league.html",
        preview=preview
    )


# =====================================================
# LEAGUE HOME
# =====================================================

@league_bp.route(
    "/league/<public_id>"
)
@login_required
def league_home(public_id):

    league = get_league_by_public_id(
        public_id
    )

    if not league:
        abort(404)

    if not is_member(
        league.id,
        current_user.id
    ):
        abort(403)

    members = league.memberships

    return render_template(
        "league_home.html",
        league=league,
        members=members
    )