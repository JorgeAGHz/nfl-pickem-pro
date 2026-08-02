import time
import requests


# =====================================================
# CACHE
# =====================================================

ESPN_CACHE = {}

CACHE_TTL = 20


# =====================================================
# INTERNAL
# =====================================================

def _get_json(url):

    now = time.time()

    cached = ESPN_CACHE.get(url)

    if cached:

        cached_time, data = cached

        if now - cached_time < CACHE_TTL:
            return data

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    ESPN_CACHE[url] = (
        now,
        data
    )

    return data


# =====================================================
# NFL SCOREBOARD
# =====================================================

def get_nfl_scoreboard(
    year,
    week
):

    url = (

        "https://site.api.espn.com/"
        "apis/site/v2/sports/"
        "football/nfl/scoreboard"
        f"?seasontype=2"
        f"&week={week}"
        f"&year={year}"

    )

    return _get_json(url)


# =====================================================
# NFL DAILY
# =====================================================

def get_nfl_daily(
    date
):

    url = (

        "https://site.api.espn.com/"
        "apis/site/v2/sports/"
        "football/nfl/scoreboard"
        f"?dates={date}"

    )

    return _get_json(url)


# =====================================================
# NBA DAILY
# =====================================================

def get_nba_daily(
    date
):

    url = (

        "https://site.api.espn.com/"
        "apis/site/v2/sports/"
        "basketball/nba/scoreboard"
        f"?dates={date}"

    )

    return _get_json(url)


# =====================================================
# EVENT SUMMARY
# =====================================================

def get_event_summary(
    sport_path,
    event_id
):

    url = (

        "https://site.api.espn.com/"
        "apis/site/v2/sports/"
        f"{sport_path}/summary"
        f"?event={event_id}"

    )

    return _get_json(url)

# =====================================================
# SCOREBOARDS
# =====================================================

def get_nba_scoreboard():

    url = (

        "https://site.api.espn.com/"
        "apis/site/v2/sports/"
        "basketball/nba/scoreboard"

    )

    return _get_json(url)

def get_nfl_scoreboard_today():

    url = (

        "https://site.api.espn.com/"
        "apis/site/v2/sports/"
        "football/nfl/scoreboard"

    )

    return _get_json(url)