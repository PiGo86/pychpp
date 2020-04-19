class HTUndefinedError(Exception):
    """Raise when error occurs with Hattrick request"""


class HTChallengeError(Exception):
    """Raise when error occurs on Hattrick with challenges"""


class HTArenaNotAvailableError(HTChallengeError):
    """Raise when arena is busy"""


class HTOpponentNotAvailableError(HTChallengeError):
    """Raise when opponent team is not available for a challenge"""


class HTTeamIsTravellingError(HTChallengeError):
    """Raise when own team is travelling and can't challenge someone else"""


class HTOpponentTeamIsTravellingError(HTChallengeError):
    """Raise when opponent team is travelling and can't be challenged"""


class HTChallengesNotOpenedError(HTChallengeError):
    """Raise when challenges can't be organized yet (to soon)"""
