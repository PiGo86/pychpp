class HTError(Exception):
    """Base Hattrick error"""


class HTUnknownMatchIdError(HTError):
    """Raise when the requested match id is unknown"""


class HTUnknownTeamIdError(HTError):
    """Raise when the requested team id is unknown"""


class HTUnknownYouthTeamIdError(HTError):
    """Raise when the requested youth team id is unknown"""


class HTUnknownPlayerIdError(HTError):
    """Raise when the requested player id is unknown"""


class HTUnknownYouthPlayerIdError(HTError):
    """Raise when the requested youth player id is unknown"""


class HTUnknownActionTypeError(HTError):
    """Raise when the requested action type is unknown"""


class HTNotOwnedTeamError(HTError):
    """Raise when the request concerns a team
    not owned by the connected user"""


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


class HTUnauthorizedAction(HTError):
    """Raise when CHPP request returns a 401 error code"""


class HTUndefinedError(HTError):
    """Raise when error occurs with Hattrick request"""


class HTSkillError(HTError):
    """Raise when skill can't be well defined"""


class HTAgeError(HTError):
    """Raise when age can't be well defined"""


class UnknownLeagueError(Exception):
    """Raise when world league doesn't exist in the list"""
