# ==========================================
# SPORTS
# ==========================================

SPORT_NFL = "NFL"
SPORT_NBA = "NBA"

ALL_SPORTS = {
    SPORT_NFL,
    SPORT_NBA
}


# ==========================================
# SEASON STATUS
# ==========================================

SEASON_UPCOMING = "UPCOMING"
SEASON_ACTIVE = "ACTIVE"
SEASON_CLOSED = "CLOSED"

ALL_SEASON_STATUSES = {
    SEASON_UPCOMING,
    SEASON_ACTIVE,
    SEASON_CLOSED
}


# ==========================================
# SEASON TYPES
# ==========================================

SEASON_TYPE_REGULAR = "REGULAR"
SEASON_TYPE_PLAYOFF = "PLAYOFF"

ALL_SEASON_TYPES = {
    SEASON_TYPE_REGULAR,
    SEASON_TYPE_PLAYOFF
}


# ==========================================
# PICK MODES
# ==========================================

PICK_MODE_NFL_SPREAD = "NFL_SPREAD"
PICK_MODE_NFL_WINNER = "NFL_WINNER"
PICK_MODE_NBA_WINNER = "NBA_WINNER"

ALL_PICK_MODES = {
    PICK_MODE_NFL_SPREAD,
    PICK_MODE_NFL_WINNER,
    PICK_MODE_NBA_WINNER
}


# ==========================================
# VISIBILITY
# ==========================================

VISIBILITY_PRIVATE = "PRIVATE"
VISIBILITY_PUBLIC = "PUBLIC"

ALL_VISIBILITY_TYPES = {
    VISIBILITY_PRIVATE,
    VISIBILITY_PUBLIC
}


# ==========================================
# MEMBERSHIP ROLES
# ==========================================

ROLE_OWNER = "OWNER"
ROLE_MEMBER = "MEMBER"

ALL_ROLES = {
    ROLE_OWNER,
    ROLE_MEMBER
}


# ==========================================
# GAME STATUS
# ==========================================

GAME_STATUS_SCHEDULED = "SCHEDULED"
GAME_STATUS_IN_PROGRESS = "IN_PROGRESS"
GAME_STATUS_FINAL = "FINAL"

ALL_GAME_STATUSES = {
    GAME_STATUS_SCHEDULED,
    GAME_STATUS_IN_PROGRESS,
    GAME_STATUS_FINAL
}


# ==========================================
# NFL CALENDAR
# ==========================================

NFL_REGULAR_SEASON_END = 18

NFL_WILD_CARD_WEEK = 19
NFL_DIVISIONAL_WEEK = 20
NFL_CONFERENCE_WEEK = 21
NFL_SUPER_BOWL_WEEK = 22

NFL_FINAL_WEEK = 22

NFL_PLAYOFF_WEEKS = {
    NFL_WILD_CARD_WEEK,
    NFL_DIVISIONAL_WEEK,
    NFL_CONFERENCE_WEEK,
    NFL_SUPER_BOWL_WEEK
}


# ==========================================
# PICK SELECTIONS
# ==========================================

SELECTION_HOME = "HOME"
SELECTION_AWAY = "AWAY"
SELECTION_DIFFERENCE = "DIFFERENCE"

ALL_SELECTIONS = {
    SELECTION_HOME,
    SELECTION_AWAY,
    SELECTION_DIFFERENCE
}


# ==========================================
# VALID SELECTIONS BY MODE
# ==========================================

VALID_SELECTIONS_BY_MODE = {

    PICK_MODE_NFL_SPREAD: {

        SELECTION_HOME,
        SELECTION_AWAY,
        SELECTION_DIFFERENCE

    },

    PICK_MODE_NFL_WINNER: {

        SELECTION_HOME,
        SELECTION_AWAY

    },

    PICK_MODE_NBA_WINNER: {

        SELECTION_HOME,
        SELECTION_AWAY

    }

}