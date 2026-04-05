from flask import Flask
from app.extensions import db, login_manager
import os


def create_app():

    app = Flask(__name__)

    # =========================
    # CONFIG
    # =========================

    app.config["SECRET_KEY"] = "secret123"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # =========================
    # EXTENSIONS
    # =========================

    db.init_app(app)
    login_manager.init_app(app)

    # =========================
    # IMPORT MODELS (IMPORTANT)
    # =========================

    from app.models import User, League, Membership, Game, Pick, Invite

    # =========================
    # USER LOADER
    # =========================

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # =========================
    # BLUEPRINTS
    # =========================

    from app.routes.auth import auth_bp
    from app.routes.league import league_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(league_bp)
    app.register_blueprint(admin_bp)

    # =========================
    # CREATE TABLES
    # =========================

    with app.app_context():
        db.create_all()

    # =========================
    # TEMPLATE FILTERS
    # =========================

    import pytz
    from datetime import datetime

    @app.template_filter("game_state")
    def game_state(game):

        mexico = pytz.timezone("America/Mexico_City")
        now = datetime.now(mexico)

        try:
            game_time = datetime.fromisoformat(
                game.game_date.replace("Z","+00:00")
            ).astimezone(mexico)
        except:
            return "Scheduled"

        if game.status == "Final":
            return "Final"

        if game_time > now:
            return "Scheduled"

        return game.status or "Live"

    @app.template_filter("to_local_time")
    def to_local_time(value):

        mexico = pytz.timezone("America/Mexico_City")

        dt = datetime.fromisoformat(value.replace("Z","+00:00"))

        return dt.astimezone(mexico).strftime("%H:%M")

    # =========================
    # SCHEDULER
    # =========================

    from apscheduler.schedulers.background import BackgroundScheduler
    from app.services.espn_service import update_results

    scheduler = BackgroundScheduler()

    def scheduled_update():

        with app.app_context():
            update_results()

    scheduler.add_job(
        func=scheduled_update,
        trigger="interval",
        seconds=30,
        max_instances=1,
        coalesce=True
    )

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        scheduler.start()

    return app