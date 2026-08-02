from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from app.services.espn_update_service import (
    update_live_games
)


scheduler = BackgroundScheduler()


# =====================================================
# JOBS
# =====================================================

def update_live_games_job():

    update_live_games()


# =====================================================
# START
# =====================================================

def start_scheduler(app):

    def wrapped_update():

        with app.app_context():

            update_live_games_job()

    scheduler.add_job(

        func=wrapped_update,

        trigger="interval",

        seconds=30,

        max_instances=1,

        coalesce=True,

        id="live_updates",

        replace_existing=True
    )

    scheduler.start()