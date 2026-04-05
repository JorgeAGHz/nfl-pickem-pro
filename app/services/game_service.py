from datetime import datetime, timezone


def is_game_locked(game):

    try:
        game_time = datetime.fromisoformat(
            game.game_date.replace("Z", "+00:00")
        )
    except:
        return False

    now = datetime.now(timezone.utc)

    return now >= game_time

from datetime import datetime
import pytz


def game_started(game):

    mexico = pytz.timezone("America/Mexico_City")

    try:

        game_time = datetime.fromisoformat(
            game.game_date.replace("Z", "+00:00")
        ).astimezone(mexico)

    except:
        return False

    now = datetime.now(mexico)

    # si ya empezó o está en vivo
    if game_time <= now:
        return True

    return False