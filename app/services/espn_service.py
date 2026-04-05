import requests
import time
from datetime import datetime, timedelta
import pytz

from app.extensions import db
from app.models import Game

mexico = pytz.timezone("America/Mexico_City")

# =====================================================
# CACHE
# =====================================================

ESPN_CACHE = {}
CACHE_TTL = 20


def get_espn_data(url):

    now = time.time()

    if url in ESPN_CACHE:

        cached_time, data = ESPN_CACHE[url]

        if now - cached_time < CACHE_TTL:
            return data

    data = requests.get(url, timeout=6).json()

    ESPN_CACHE[url] = (now, data)

    return data


# =====================================================
# LOAD GAMES
# =====================================================

def load_games():

    now = datetime.now(mexico)

    nba_start = (now - timedelta(days=7)).strftime("%Y%m%d")
    nba_end = (now + timedelta(days=7)).strftime("%Y%m%d")

    # =========================
    # NFL
    # =========================

    for week in range(1, 19):

        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype=2&week={week}&year=2025"

        data = get_espn_data(url)

        for event in data.get("events", []):

            api_id = event["id"]

            if Game.query.filter_by(api_id=api_id).first():
                continue

            comp = event["competitions"][0]
            teams = comp["competitors"]

            home = teams[0]
            away = teams[1]

            home_team = home["team"]["displayName"]
            away_team = away["team"]["displayName"]

            home_abbr = home["team"]["abbreviation"]
            away_abbr = away["team"]["abbreviation"]

            # spread + odds
            spread = None
            home_odds = None
            away_odds = None

            try:
                odds = comp.get("odds")

                if odds:

                    spread = odds[0].get("spread")
                    home_odds = odds[0].get("homeMoneyLine")
                    away_odds = odds[0].get("awayMoneyLine")

            except:
                pass

            home_logo = home["team"].get(
                "logos", [{}])[0].get(
                "href",
                f"https://a.espncdn.com/i/teamlogos/nfl/500/{home_abbr.lower()}.png"
            )

            away_logo = away["team"].get(
                "logos", [{}])[0].get(
                "href",
                f"https://a.espncdn.com/i/teamlogos/nfl/500/{away_abbr.lower()}.png"
            )

            date = event["date"]

            week_num = event.get("week", {}).get("number")

            game = Game(

                api_id=api_id,
                sport="NFL",

                home_team=home_team,
                away_team=away_team,

                home_abbr=home_abbr,
                away_abbr=away_abbr,

                home_logo=home_logo,
                away_logo=away_logo,

                game_date=date,
                week=week_num,

                spread=spread,
                home_odds=home_odds,
                away_odds=away_odds
            )

            db.session.add(game)

    # =========================
    # NBA
    # =========================

    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={nba_start}-{nba_end}"

    data = get_espn_data(url)

    for event in data.get("events", []):

        api_id = event["id"]

        if Game.query.filter_by(api_id=api_id).first():
            continue

        comp = event["competitions"][0]
        teams = comp["competitors"]

        home = teams[0]
        away = teams[1]

        home_team = home["team"]["displayName"]
        away_team = away["team"]["displayName"]

        home_abbr = home["team"]["abbreviation"]
        away_abbr = away["team"]["abbreviation"]

        spread = None
        home_odds = None
        away_odds = None

        try:
            odds = comp.get("odds")

            if odds:

                spread = odds[0].get("spread")
                home_odds = odds[0].get("homeMoneyLine")
                away_odds = odds[0].get("awayMoneyLine")

        except:
            pass

        home_logo = home["team"].get(
            "logos", [{}])[0].get(
            "href",
            f"https://a.espncdn.com/i/teamlogos/nba/500/{home_abbr.lower()}.png"
        )

        away_logo = away["team"].get(
            "logos", [{}])[0].get(
            "href",
            f"https://a.espncdn.com/i/teamlogos/nba/500/{away_abbr.lower()}.png"
        )

        date = event["date"]

        game = Game(

            api_id=api_id,
            sport="NBA",

            home_team=home_team,
            away_team=away_team,

            home_abbr=home_abbr,
            away_abbr=away_abbr,

            home_logo=home_logo,
            away_logo=away_logo,

            game_date=date,

            spread=spread,
            home_odds=home_odds,
            away_odds=away_odds
        )

        db.session.add(game)

    db.session.commit()


# =====================================================
# UPDATE RESULTS
# =====================================================

def update_results():

    today = datetime.now(mexico).strftime("%Y%m%d")

    urls = {

        "NFL": f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={today}",

        "NBA": f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={today}"

    }

    updated = 0

    for sport, url in urls.items():

        try:
            data = get_espn_data(url)
        except:
            continue

        for event in data.get("events", []):

            api_id = event["id"]

            game = Game.query.filter_by(api_id=api_id).first()

            if not game:
                continue

            comp = event["competitions"][0]
            teams = comp["competitors"]

            home = teams[0]
            away = teams[1]

            home_score = int(home.get("score", 0))
            away_score = int(away.get("score", 0))

            status = comp["status"]["type"]["description"]
            clock = comp["status"].get("displayClock")
            period = comp["status"].get("period")

            game.home_score = home_score
            game.away_score = away_score
            game.status = status
            game.clock = clock
            game.period = period

            if "final" in status.lower():

                if sport == "NBA":

                    game.result = (

                        game.home_team
                        if home_score > away_score
                        else game.away_team

                    )

                else:

                    diff = abs(home_score - away_score)

                    if diff < 7:
                        game.result = "DIFFERENCE"

                    elif home_score > away_score:
                        game.result = "HOME7"

                    else:
                        game.result = "AWAY7"

            updated += 1

    db.session.commit()

    print(f"Live update: {updated} games")

# =====================================================
# BOOTSTRAP HISTORICO
# =====================================================

def bootstrap_results():

    import requests
    from datetime import datetime
    import pytz

    mexico = pytz.timezone("America/Mexico_City")
    now = datetime.now(mexico)

    games = Game.query.all()

    sport_paths = {
        "NBA": "basketball/nba",
        "NFL": "football/nfl"
    }

    updated = 0

    for game in games:

        if game.home_score is not None:
            continue

        try:
            game_time = datetime.fromisoformat(
                game.game_date.replace("Z","+00:00")
            ).astimezone(mexico)

        except:
            continue

        if game_time > now:
            continue

        sport_path = sport_paths.get(game.sport)

        if not sport_path:
            continue

        summary_url = f"https://site.api.espn.com/apis/site/v2/sports/{sport_path}/summary?event={game.api_id}"

        try:

            data = requests.get(summary_url, timeout=4).json()

            comp = data["header"]["competitions"][0]
            teams = comp["competitors"]

            home_score = int(teams[0].get("score", 0))
            away_score = int(teams[1].get("score", 0))

            status = comp["status"]["type"]["description"]

        except:
            continue

        game.home_score = home_score
        game.away_score = away_score
        game.status = status

        if game.sport == "NBA":

            game.result = (
                game.home_team
                if home_score > away_score
                else game.away_team
            )

        else:

            diff = abs(home_score - away_score)

            if diff < 7:
                game.result = "DIFFERENCE"

            elif home_score > away_score:
                game.result = "HOME7"

            else:
                game.result = "AWAY7"

        updated += 1

    db.session.commit()

    print(f"Bootstrap updated {updated} games")