from pychpp import ht_model, ht_xml, ht_team


class HTLeague(ht_model.HTModel):
    """
    Hattrick league
    """

    _SOURCE_FILE = "leaguedetails"
    _SOURCE_FILE_VERSION = "1.5"

    _URL_PATH = "/World/Series/?LeagueLevelUnitID="

    _ht_attributes = [("ht_id", "LeagueLevelUnitID", ht_xml.HTXml.ht_int),
                      # General information
                      ("level", "LeagueLevel", ht_xml.HTXml.ht_int),
                      ("name", "LeagueLevelUnitName", ht_xml.HTXml.ht_str),
                      ("current_match_round", "CurrentMatchRound",
                       ht_xml.HTXml.ht_str),
                      # Country name
                      ("country_id", "LeagueID", ht_xml.HTXml.ht_int),
                      ("country_name", "LeagueName", ht_xml.HTXml.ht_str),
                      ]

    def __init__(self, ht_id=None, **kwargs):
        """
        Initialization of a HTLeague instance

        :param ht_id: Hattrick ID of league
        :type ht_id: int
        :key chpp: CHPP instance of connected user
        :type chpp: chpp.CHPP
        """
        self._REQUEST_ARGS = dict()
        self._REQUEST_ARGS["leagueLevelUnitID"] = (
            ht_id if ht_id is not None else "")
        super().__init__(**kwargs)
        self.teams = [ht_team.HTTeamRank(chpp=self._chpp, data=team)
                      for team in self._data.findall("Team")]

    def __repr__(self):
        return f"<{self.__class__.__name__} object : " \
               f"{self.name} ({self.ht_id})>"


class HTLeagueFixtures(ht_model.HTModel):
    """
    Hattrick league fixtures
    """

    _SOURCE_FILE = "leaguefixtures"
    _SOURCE_FILE_VERSION = "1.2"

    _URL_PATH = "/World/Series/Fixtures.aspx?LeagueLevelUnitID="

    _ht_attributes = [("ht_id", "LeagueLevelUnitID", ht_xml.HTXml.ht_int),
                      # General information
                      ("name", "LeagueLevelUnitName", ht_xml.HTXml.ht_str),
                      ("season", "Season", ht_xml.HTXml.ht_int),
                      ]

    def __init__(self, ht_id=None, season=None, **kwargs):
        """
        Initialization of a HTLeague instance

        :param ht_id: Hattrick ID of league
        :param season: season to fetch
        :type ht_id: int
        :type season: int
        :key chpp: CHPP instance of connected user
        :type chpp: chpp.CHPP
        """

        # Check parameters integrity
        if not isinstance(ht_id, int) and ht_id is not None:
            raise ValueError("if set, ht_id must be an integer")
        elif not isinstance(season, int) and season is not None:
            raise ValueError("if set, season must be an integer")

        self._REQUEST_ARGS = dict()

        self._REQUEST_ARGS["leagueLevelUnitID"] = (
            ht_id if ht_id is not None else "")

        self._REQUEST_ARGS["season"] = (
            season if season is not None else "")

        super().__init__(**kwargs)

        self.matches = [HTLeagueFixturesMatch(chpp=self._chpp, data=match)
                        for match in self._data.findall("Match")]

    def __repr__(self):
        return f"<{self.__class__.__name__} object : " \
               f"{self.name} ({self.ht_id}) - Season {self.season}>"


class HTLeagueFixturesMatch(ht_model.HTModel):
    """
    HT League fixtures match item
    """

    _ht_attributes = [("ht_id", "MatchID", ht_xml.HTXml.ht_int),
                      # General information
                      ("round", "MatchRound", ht_xml.HTXml.ht_int),
                      ("home_team_ht_id", "HomeTeam/HomeTeamID",
                       ht_xml.HTXml.ht_int),
                      ("home_team_name", "HomeTeam/HomeTeamName",
                       ht_xml.HTXml.ht_str),
                      ("away_team_ht_id", "AwayTeam/AwayTeamID",
                       ht_xml.HTXml.ht_int),
                      ("away_team_name", "AwayTeam/AwayTeamName",
                       ht_xml.HTXml.ht_str),
                      ("datetime", "MatchDate",
                       ht_xml.HTXml.ht_datetime_from_text),
                      ("home_goals", "HomeGoals", ht_xml.HTXml.ht_int),
                      ("away_goals", "AwayGoals", ht_xml.HTXml.ht_int),
                      ]
