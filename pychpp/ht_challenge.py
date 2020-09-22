import xml.etree.ElementTree

from pychpp import chpp as _chpp
from pychpp import ht_xml


class HTChallengeManager:
    """
    Managing challenges on Hattrick
    """

    _SOURCE_FILE = "challenges"
    _SOURCE_FILE_VERSION = "1.6"
    _ACTION_TYPE = "view"

    def __init__(self, chpp, team_ht_id=None, match_period="week"):
        """
        Initialize a HTChallengeManager instance

        :param chpp: CHPP instance of connected user
        :param team_ht_id: Hattrick ID of team to manage challenges
        :param match_period: Period concerned, can be "week" or "weekend",
        defaults to "week"
        :type chpp: CHPP
        :type team_ht_id: int
        :type match_period: str
        """
        if not isinstance(chpp, _chpp.CHPP):
            raise ValueError("chpp must be a CHPP oject")
        elif team_ht_id is not None and not isinstance(team_ht_id, int):
            raise ValueError("team_ht_id must be an integer")
        elif match_period not in ("week", "weekend"):
            raise ValueError(
                "match_period must be equal to 'week' or 'weekend'")

        self._chpp = chpp

        self._REQUEST_ARGS = {
            "file": self._SOURCE_FILE,
            "version": self._SOURCE_FILE_VERSION,
            "teamId": str(team_ht_id) if team_ht_id is not None else "",
            "isWeekendFriendly": {"week": "0", "weekend": "1"}[match_period],
            }

    def _set_tm_ht_id(self, training_match_ht_id):
        if not isinstance(training_match_ht_id, int):
            raise ValueError("training_match_ht_id must be an integer")
        self._REQUEST_ARGS["trainingMatchId"] = str(training_match_ht_id)

    def is_challengeable(self, team_ht_id):
        """
        Check if one or more team are available to be challenged

        :param team_ht_id: team Hattrick ID or list of teams Hattrick ID
        to check availability
        :type team_ht_id: int or list
        :return: a dictionnary with keys equal to every tested team_ht_id
        and values equal to booleans
        :rtype: dict
        """

        self._REQUEST_ARGS["suggestedTeamIds"] = str()

        # Check team_ht_id integrity
        if isinstance(team_ht_id, int):
            self._REQUEST_ARGS["suggestedTeamIds"] = str(team_ht_id)
        elif (isinstance(team_ht_id, list)
              and all(isinstance(i, int) and type(i) != bool
                      for i in team_ht_id)):
            self._REQUEST_ARGS["suggestedTeamIds"] = (
                ",".join(str(ht_id) for ht_id in team_ht_id))
        else:
            raise ValueError("team_ht_id must be an int or a list of int")

        self._REQUEST_ARGS["actionType"] = "challengeable"
        data = self._chpp.request(**self._REQUEST_ARGS)\
                   .find("Team")\
                   .find("ChallengeableResult")

        result_dict = {
            int(i.find("TeamId").text):
            True if i.find('IsChallengeable').text == "True" else False
            for i in data}

        return result_dict

    def list(self, author="both", data=None):
        """
        List pending challenges for current team

        :param author: choose challenges to show :
            - only challenges launched by current team ("own_team") ;
            - only challenges launched by otehr teams ("other_teams") ;
            - all challenges ("both").
        :param data: ElementTree data (to avoid a new fetch to Hattrick)
        :type author: str
        :type data: xml.tree.ElementTree, optional
        :return: a list of Challenge instances
        :rtype: list
        """
        if author not in ("own_team", "other_teams", "both"):
            raise ValueError(
                "author must be equal to 'own_team', 'other_teams' or 'both'")

        if data is not None:
            if not isinstance(data, xml.etree.ElementTree.Element):
                raise ValueError(
                    "if set, data must be an ElementTree.Element object")
        else:
            self._REQUEST_ARGS["actionType"] = "view"
            data = self._chpp.request(**self._REQUEST_ARGS).find("Team")

        challenges = list()
        for child in data:
            if ((child.tag == "ChallengesByMe"
                 and author in ("own_team", "both"))
                    or (child.tag == "OffersByOthers"
                        and author in ("other_teams", "both"))):
                for c in child:
                    challenges.append(
                        HTChallenge(
                            author=("own_team"
                                    if child.tag == "ChallengesByMe"
                                    else "other_teams"),
                            training_match_id=int(c.find("TrainingMatchID")
                                                   .text),
                            match_date=ht_xml.HTXml.ht_datetime_from_text(
                                c.find("MatchTime").text),
                            match_type=c.find("FriendlyType").text,
                            opponent_team_ht_id=int(
                                c.find("Opponent").find("TeamID").text),
                            arena_ht_id=int(
                                c.find("Arena").find("ArenaID").text),
                            is_agreed=(True
                                       if c.find("IsAgreed").text == "True"
                                       else False),
                            ))

        return challenges

    def launch(self, opponent_team_ht_id, match_type="normal",
               match_place="home", arena_ht_id=0):
        """
        Challenge another team

        :param opponent_team_ht_id: Hattrick ID of team to challenge
        :param match_type: type of match : can be "normal" or "cup_rules",
        defaults to "normal"
        :param match_place: place of match : can be "home", "away",
        or "neutral", default to "home"
        :param arena_ht_id: if "match_place" is "neutral", Hattrick ID
        of Arena where playing match, default to 0
        :type opponent_team_ht_id: int
        :type match_type: str, optional
        :type match_place: str, optional
        :type arena_ht_id: int, optional
        :return: the launched challenge
        :rtype: HTChallenge
        """

        # Check parameters integrity
        if not isinstance(opponent_team_ht_id, int):
            raise ValueError(
                "opponent_team_ht_id must be an integer")
        elif match_type not in ("normal", "cup_rules"):
            raise ValueError(
                "match_type must be equal to 'normal' or 'cup_rules'")
        elif match_place not in ("home", "away", "neutral"):
            raise ValueError(
                "match_type must be equal to 'home', 'away' or 'neutral'")
        elif not isinstance(arena_ht_id, int):
            raise ValueError(
                "arena_ht_id must be an integer")

        # Defined request arguments according to method parameters
        self._REQUEST_ARGS["actionType"] = "challenge"
        self._REQUEST_ARGS["opponentTeamId"] = str(opponent_team_ht_id)
        self._REQUEST_ARGS["matchType"] = {
            "normal": "0", "cup_rules": "1"}[match_type]
        self._REQUEST_ARGS["matchPlace"] = {
            "home": "0", "away": "1", "neutral": "2"}[match_place]
        self._REQUEST_ARGS["neutralArenaId"] = str(arena_ht_id)

        # Send Hattrick request
        data = self._chpp.request(**self._REQUEST_ARGS)

        challenge = [c for c in self.list(data=data.find("Team"))
                     if c.opponent_team_ht_id == opponent_team_ht_id][0]

        return challenge

    def accept(self, training_match_ht_id):
        """
        Accept a challenge

        :param training_match_ht_id: Hattrick ID of challenge to accept
        :type training_match_ht_id: int
        :return: the accepted challenge
        :rtype: HTChallenge
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

        :param training_match_ht_id: Hattrick ID of challenge to decline
        :type training_match_ht_id: int
        """
        self._REQUEST_ARGS["actionType"] = "decline"
        self._set_tm_ht_id(training_match_ht_id)
        self._chpp.request(**self._REQUEST_ARGS)

    def withdraw(self, training_match_ht_id):
        """
        Withdraw a challenge

        :param training_match_ht_id: Hattrick ID of challenge to withdraw
        :type training_match_ht_id: int
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
        """
        Initialize HTChallenge instance

        :param author: author of challenge, can be "own_team" or "other_teams"
        :param training_match_id: challenge Hattrick ID
        :param match_date: challenge date
        :param match_type: challenge type : can be "normal" or "cup_rules"
        :param opponent_team_ht_id: opponent team Hattrick ID
        :param arena_ht_id: if "match_place" is "neutral",
        Hattrick ID of Arena where playing match, default to 0
        :type author: str
        :type training_match_id: int
        :type match_date: Union[datetime.datetime, ht_datetime.HTDatetime]
        :type match_type: str
        :type opponent_team_ht_id: int
        :type arena_ht_id: int
        """
        self.author = author
        self.training_match_id = training_match_id
        self.match_date = match_date
        self.match_type = match_type
        self.opponent_team_ht_id = opponent_team_ht_id
        self.arena_ht_id = arena_ht_id
        self.is_agreed = is_agreed
