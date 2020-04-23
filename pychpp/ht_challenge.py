import xml

from pychpp import chpp as _chpp
from pychpp import ht_date


class HTChallengeManager:
    """
    Managing challenges on Hattrick
    """

    _SOURCE_FILE = "challenges"
    _SOURCE_FILE_VERSION = "1.6"
    _ACTION_TYPE = "view"

    _REQUEST_ARGS = {"file": _SOURCE_FILE,
                     "version": _SOURCE_FILE_VERSION,
                     "action_type": _ACTION_TYPE,
                     }

    def __init__(self, chpp, team_ht_id, match_period="week"):

        if not isinstance(chpp, _chpp.CHPP):
            raise ValueError("chpp must be a CHPP oject")
        elif not isinstance(team_ht_id, int):
            raise ValueError("team_ht_id must be an integer")
        elif match_period not in ("week", "weekend"):
            raise ValueError("match_period must be equal to 'week' or 'weekend'")

        self._chpp = chpp
        self._REQUEST_ARGS["teamId"] = str(team_ht_id)
        self._REQUEST_ARGS["isWeekendFriendly"] = {"week": "0", "weekend": "1"}[match_period]

    def _set_tm_ht_id(self, training_match_ht_id):
        if not isinstance(training_match_ht_id, int):
            raise ValueError("training_match_ht_id must be an integer")
        self._REQUEST_ARGS["trainingMatchId"] = str(training_match_ht_id)

    def list(self, author="both", data=None):
        """
        List pending challenges for current team
        """
        if author not in ("own_team", "other_teams", "both"):
            raise ValueError("author must be equal to 'own_team', 'other_teams' or 'both'")

        if data is not None:
            if not isinstance(data, xml.etree.ElementTree.Element):
                raise ValueError("if set, data must be an ElementTree.Element object")
        else:
            self._REQUEST_ARGS["actionType"] = "view"
            data = self._chpp.request(**self._REQUEST_ARGS).find("Team")

        challenges = list()
        for child in data:
            if ((child.tag == "ChallengesByMe" and author in ("own_team", "both"))
                    or child.tag == "OffersByOthers" and author in ("other_teams", "both")):
                for c in child:
                    challenges.append(
                        HTChallenge(author="own_team" if child.tag == "ChallengesByMe" else "other_teams",
                                    training_match_id=int(c.find("TrainingMatchID").text),
                                    match_date=ht_date.HTDate.from_ht(c.find("MatchTime").text),
                                    match_type=int(c.find("FriendlyType").text),
                                    opponent_team_ht_id=int(c.find("Opponent").find("TeamID").text),
                                    arena_ht_id=int(c.find("Arena").find("ArenaID").text),
                                    is_agreed=True if c.find("IsAgreed").text == "True" else False,
                                    ))

        return challenges

    def launch(self, opponent_team_ht_id, match_type="normal",
               match_place="home", arena_ht_id=0, match_period="week"):
        """
        Challenge another team
        """

        # Check parameters integrity
        if not isinstance(opponent_team_ht_id, int):
            raise ValueError("opponent_team_ht_id must be an integer")
        elif match_type not in ("normal", "cup_rules"):
            raise ValueError("match_type must be equal to 'normal' or 'cup_rules'")
        elif match_place not in ("home", "away", "neutral"):
            raise ValueError("match_type must be equal to 'home', 'away' or 'neutral'")
        elif not isinstance(arena_ht_id, int):
            raise ValueError("arena_ht_id must be an integer")

        # Defined request arguments according to method parameters
        self._REQUEST_ARGS["actionType"] = "challenge"
        self._REQUEST_ARGS["opponentTeamId"] = str(opponent_team_ht_id)
        self._REQUEST_ARGS["matchType"] = {"normal": "0", "cup_rules": "1"}[match_type]
        self._REQUEST_ARGS["matchPlace"] = {"home": "0", "away": "1", "neutral": "2"}[match_place]
        self._REQUEST_ARGS["neutralArenaId"] = str(arena_ht_id)

        # Send Hattrick request
        data = self._chpp.request(**self._REQUEST_ARGS)

        challenge = [c for c in self.list(data=data.find("Team"))
                     if c.opponent_team_ht_id == opponent_team_ht_id][0]

        return challenge

    def accept(self, training_match_ht_id):
        """
        Accept a challenge
        """
        self._REQUEST_ARGS["actionType"] = "accept"
        self._set_tm_ht_id(training_match_ht_id)
        data = self._chpp.request(**self._REQUEST_ARGS)
        challenge = [c for c in self.list(data=data.find("Team"))
                     if c.is_agreed is True][0]
        return challenge

    def decline(self, training_match_ht_id):
        """
        Decline a challenge
        """
        self._REQUEST_ARGS["actionType"] = "decline"
        self._set_tm_ht_id(training_match_ht_id)
        self._chpp.request(**self._REQUEST_ARGS)

    def withdraw(self, training_match_ht_id):
        """
        Withdraw a challenge
        """
        self._REQUEST_ARGS["actionType"] = "withdraw"
        self._set_tm_ht_id(training_match_ht_id)
        self._chpp.request(**self._REQUEST_ARGS)


class HTChallenge:
    """
    Hattrick challenge
    """

    def __init__(self, author, training_match_id, match_date, match_type,
                 opponent_team_ht_id, arena_ht_id, is_agreed):

        self.author = author
        self.training_match_id = training_match_id
        self.match_date = match_date
        self.match_type = match_type
        self.opponent_team_ht_id = opponent_team_ht_id
        self.arena_ht_id = arena_ht_id
        self.is_agreed = is_agreed
