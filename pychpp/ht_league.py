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
