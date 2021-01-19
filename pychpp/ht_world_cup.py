from pychpp import ht_model
from pychpp import ht_xml


class HTWorldCupCore(ht_model.HTModel):
    """
    Core Hattrick world cup
    Used to create HTWorldCupGroups and HTWorldCupMatches classes
    """

    _SOURCE_FILE = "worldcup"
    _SOURCE_FILE_VERSION = "1.1"

    def __init__(self, season, cup_id=137, **kwargs):
        """
        Initialize HTWorldCupCore instance

        :param season: global Hattrick season
        :param cup_id: unique cup ID
                       (137 = World Cup, 149 = U-20 World Cup)
        :key chpp: CHPP instance of connected user
        :type season: int
        :type cup_id: int
        :key chpp: CHPP instance of connected user, must be a chpp.CHPP object
        """

        if not isinstance(season, int):
            raise ValueError("season must be an integer")
        if not isinstance(cup_id, int) or cup_id not in [137, 149]:
            raise ValueError("cup_id must be an integer",
                             "(137 = World Cup, 149 = U-20 World Cup)")

        self._REQUEST_ARGS["season"] = season
        self._REQUEST_ARGS["cupId"] = cup_id

        super().__init__(**kwargs)

        self.cup_name = "World Cup" if cup_id == 137 else "U-20 World Cup"

    def __repr__(self):
        return f"<{str(self.__class__.__name__)} object : " \
                f"{self.cup_name} ({self.season}) >"


class HTWorldCupGroups(HTWorldCupCore):
    """
    Hattrick World Cup groups details
    """

    _ht_attributes = [
        ("cup_id", "CupID",
         ht_xml.HTXml.ht_int,),
        ("season", "Season",
         ht_xml.HTXml.ht_int,),
    ]

    def __init__(self, **kwargs):
        """
        Initialization of a HTWorldCupGroups instance

        :param season: global Hattrick season
        :param cup_id: unique cup ID
                       (137 = World Cup, 149 = U-20 World Cup)
        :param chpp: CHPP instance of connected user
        :type season: int
        :type cup_id: int
        :key chpp: CHPP instance of connected user, must be a chpp.CHPP object
        """

        self._REQUEST_ARGS = dict()
        self._REQUEST_ARGS["actionType"] = "viewGroups"

        super().__init__(**kwargs)

        self.scores = [HTWorldCupScore(chpp=self._chpp, data=score)
                       for score in self._data
                                        .find("WorldCupScores")
                                        .findall("Team")]

        self.rounds = [HTWorldCupRound(chpp=self._chpp, data=wc_round)
                       for wc_round in self._data
                                           .find("Rounds")
                                           .findall("Round")]


class HTWorldCupMatches(HTWorldCupCore):
    """
    Hattrick World Cup matches details
    """

    _ht_attributes = [
        ("cup_id", "CupID",
         ht_xml.HTXml.ht_int,),
        ("season", "Season",
         ht_xml.HTXml.ht_int,),
        ("match_round", "MatchRound",
         ht_xml.HTXml.ht_int,),
        ("cup_series_unit_id", "CupSeriesUnitID",
         ht_xml.HTXml.ht_int,),
    ]

    def __init__(self, cup_series_unit_id, match_round=1, **kwargs):
        """
        Initialization of a HTWorldCupGroups instance

        :param season: global Hattrick season
        :param cup_id: unique cup ID
                       (137 = World Cup, 149 = U-20 World Cup)
        :param cup_series_unit_id: global ID of a World Cup group
        :param match_round: key that indicates a certain round
                            (1 = qualification round, 15 = round II,
                             18 = round III, 21 = round IV,
                             24 = semi-finals, 25 = final)
        :param chpp: CHPP instance of connected user
        :type season: int
        :type cup_id: int
        :type cup_series_unit_id: int
        :type match_round: int
        :key chpp: CHPP instance of connected user, must be a chpp.CHPP object
        """

        self._REQUEST_ARGS = dict()
        self._REQUEST_ARGS["actionType"] = "viewMatches"
        self._REQUEST_ARGS["cupSeriesUnitID"] = cup_series_unit_id

        if not isinstance(match_round, int) or \
           match_round not in [1, 15, 18, 21, 24, 25]:
            raise ValueError("match_round must be an integer",
                             "(1 = qualification round, 15 = round II,",
                             "18 = round III, 21 = round IV,",
                             "24 = semi-finals, 25 = final)")
        self._REQUEST_ARGS["matchRound"] = match_round

        super().__init__(**kwargs)

        self.matches = [HTWorldCupMatch(chpp=self._chpp, data=match)
                        for match in self._data
                                         .find("Matches")
                                         .findall("Match")]

        self.rounds = [HTWorldCupRound(chpp=self._chpp, data=wc_round)
                       for wc_round in self._data
                                           .find("Rounds")
                                           .findall("Round")]


class HTWorldCupScore(ht_model.HTModel):
    """
    Hattrick World Cup score entry
    """

    _ht_attributes = [
        ("ht_id", "TeamID",
         ht_xml.HTXml.ht_int,),
        ("team_name", "TeamName",
         ht_xml.HTXml.ht_str,),
        ("place", "Place",
         ht_xml.HTXml.ht_int,),
        ("cup_series_unit_id", "CupSeriesUnitID",
         ht_xml.HTXml.ht_int,),
        ("cup_series_unit_name", "CupSeriesUnitName",
         ht_xml.HTXml.ht_str,),
        ("matches_played", "MatchesPlayed",
         ht_xml.HTXml.ht_int,),
        ("goals_for", "GoalsFor",
         ht_xml.HTXml.ht_int,),
        ("goals_against", "GoalsAgainst",
         ht_xml.HTXml.ht_int,),
        ("points", "Points",
         ht_xml.HTXml.ht_int,)
    ]

    def __repr__(self):
        return f"<{str(self.__class__.__name__)} object : " \
                f"{self.team_name} ({self.ht_id}) >"


class HTWorldCupRound(ht_model.HTModel):
    """
    Hattrick World Cup round entry
    """

    _ht_attributes = [
        ("match_round", "MatchRound",
         ht_xml.HTXml.ht_int,),
        ("start_date", "StartDate",
         ht_xml.HTXml.ht_datetime_from_text,)
    ]

    def __repr__(self):
        return f"<{str(self.__class__.__name__)} object : " \
                f"Round {self.match_round} >"


class HTWorldCupMatch(ht_model.HTModel):
    """
    Hattrick World Cup match entry
    """

    _ht_attributes = [
        ("match_id", "MatchID",
         ht_xml.HTXml.ht_int,),
        ("home_team_id", "HomeTeam/TeamID",
         ht_xml.HTXml.ht_int,),
        ("home_team_name", "HomeTeam/TeamName",
         ht_xml.HTXml.ht_str,),
        ("away_team_id", "AwayTeam/TeamID",
         ht_xml.HTXml.ht_int,),
        ("away_team_name", "AwayTeam/TeamName",
         ht_xml.HTXml.ht_str,),
        ("match_date", "MatchDate",
         ht_xml.HTXml.ht_datetime_from_text,),
        ("finished_date", "FinishedDate",
         ht_xml.HTXml.opt_ht_datetime_from_text,),
        ("home_goals", "HomeGoals",
         ht_xml.HTXml.ht_int,),
        ("away_goals", "AwayGoals",
         ht_xml.HTXml.ht_int,)
    ]

    def __repr__(self):
        return f"<{str(self.__class__.__name__)} object : " \
                f"{self.home_team_name} - {self.away_team_name} " \
                f"({self.match_id}) >"
