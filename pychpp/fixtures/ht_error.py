"""Exceptions raised when the CHPP API returns an error."""

class HTError(Exception):
    """Base Hattrick error."""


class HTUnknownMatchIdError(HTError):
    """Raised when the requested match ID is unknown."""


class HTUnknownTeamIdError(HTError):
    """Raised when the requested team ID is unknown."""


class HTUnknownYouthTeamIdError(HTError):
    """Raised when the requested youth team ID is unknown."""


class HTUnknownPlayerIdError(HTError):
    """Raised when the requested player ID is unknown."""


class HTUnknownYouthPlayerIdError(HTError):
    """Raised when the requested youth player ID is unknown."""


class HTUnknownActionTypeError(HTError):
    """Raised when the requested action type is unknown."""


class HTNotOwnedTeamError(HTError):
    """Raised when the request concerns a team not owned by the connected user."""


class HTChallengeError(HTError):
    """Raised when error occurs on Hattrick with challenges."""


class HTTeamChallengingItself(HTChallengeError):
    """Raised when a team is challenging itself."""


class HTArenaNotAvailableError(HTChallengeError):
    """Raised when arena is busy."""


class HTTeamNotAvailableError(HTChallengeError):
    """Raised when the own team is not available for a challenge.

    For example when a friendly is already booked or the team is still in cup.

    """


class HTOpponentTeamNotAvailableError(HTChallengeError):
    """Raised when opponent team is not available for a challenge."""


class HTTeamIsTravellingError(HTChallengeError):
    """Raised when own team is travelling and can't challenge someone else."""


class HTOpponentTeamIsTravellingError(HTChallengeError):
    """Raised when opponent team is travelling and can't be challenged."""


class HTChallengesNotOpenedError(HTChallengeError):
    """Raised when challenges can't be organized yet (too soon)."""


class HTUnauthorizedAction(HTError):
    """Raised when CHPP request returns a 401 error code."""


class HTAccessDeniedError(HTError):
    """Raised when Hattrick denies access to a parameter or file (error code 1)."""


class HTUndefinedError(HTError):
    """Raised when error occurs with Hattrick request."""


class HTSkillError(HTError):
    """Raised when skill can't be well-defined."""


class HTAgeError(HTError):
    """Raised when age can't be well-defined."""


class UnknownLeagueError(HTError):
    """Raised when world league doesn't exist in the list."""
