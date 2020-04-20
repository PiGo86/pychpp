class HTError(Exception):
    """Base Hattrick error"""


class HTNotOwnedTeamError(HTError):
    """Raise when the request concerns a team not owned by the connected user"""


class HTChallengeError(HTError):
    """Raise when error occurs on Hattrick with challenges"""


class HTTeamChallengingItself(HTChallengeError):
    """Raise when a team is challenging itself"""


class HTArenaNotAvailableError(HTChallengeError):
    """Raise when arena is busy"""


class HTTeamNotAvailableError(HTChallengeError):
    """Raise when opponent team is not available for a challenge"""


class HTOpponentTeamNotAvailableError(HTChallengeError):
    """Raise when opponent team is not available for a challenge"""


class HTTeamIsTravellingError(HTChallengeError):
    """Raise when own team is travelling and can't challenge someone else"""


class HTOpponentTeamIsTravellingError(HTChallengeError):
    """Raise when opponent team is travelling and can't be challenged"""


class HTChallengesNotOpenedError(HTChallengeError):
    """Raise when challenges can't be organized yet (to soon)"""


class HTUndefinedError(HTError):
    """Raise when error occurs with Hattrick request"""
