from pychpp import ht_model
from pychpp import ht_xml


class HTNationalTeam(ht_model.HTModel):
    """
    Hattrick National Team details
    """

    _SOURCE_FILE = "nationalteamdetails"
    _SOURCE_FILE_VERSION = "1.9"

    _URL_PATH = "/Club/NationalTeam/NationalTeam.aspx?teamId="

    _ht_attributes = [
        ("is_playing", "IsPlayingMatch",
         ht_xml.HTXml.ht_bool,),
        ("ht_id", "Team/TeamID",
         ht_xml.HTXml.ht_int,),
        ("team_name", "Team/TeamName",
         ht_xml.HTXml.ht_str,),
        ("nt_coach_id", "Team/NationalCoach/NationalCoachUserID",
         ht_xml.HTXml.ht_int,),
        ("nt_coach_name", "Team/NationalCoach/NationalCoachLoginname",
         ht_xml.HTXml.ht_str,),
        ("league_id", "Team/League/LeagueID",
         ht_xml.HTXml.ht_int,),
        ("league_name", "Team/League/LeagueName",
         ht_xml.HTXml.ht_str,),
        ("xp_442", "Team/Experience442",
         ht_xml.HTXml.ht_int,),
        ("xp_433", "Team/Experience433",
         ht_xml.HTXml.ht_int,),
        ("xp_451", "Team/Experience451",
         ht_xml.HTXml.ht_int,),
        ("xp_352", "Team/Experience352",
         ht_xml.HTXml.ht_int,),
        ("xp_532", "Team/Experience532",
         ht_xml.HTXml.ht_int,),
        ("xp_343", "Team/Experience343",
         ht_xml.HTXml.ht_int,),
        ("xp_541", "Team/Experience541",
         ht_xml.HTXml.ht_int,),
        ("xp_523", "Team/Experience523",
         ht_xml.HTXml.ht_int,),
        ("xp_550", "Team/Experience550",
         ht_xml.HTXml.ht_int,),
        ("xp_253", "Team/Experience253",
         ht_xml.HTXml.ht_int,),
        ("morale", "Team/Morale",
         ht_xml.HTXml.ht_int,),
        ("supporters_popularity", "Team/SupportersPopularity",
         ht_xml.HTXml.ht_int,),
        ("confidence", "Team/SelfConfidence",
         ht_xml.HTXml.ht_int,),
        ("rating_score", "Team/RatingScore",
         ht_xml.HTXml.ht_int,),
        ("fan_club_size", "Team/FanClubSize",
         ht_xml.HTXml.ht_int,),
        ("rank", "Team/Rank",
         ht_xml.HTXml.ht_int,),
    ]

    def __init__(self, ht_id, **kwargs):
        """
        Initialize HTNationalCoreTeam instance

        :param ht_id: national team Hattrick ID
        :key chpp: CHPP instance of connected user
        :type ht_id: int
        :type chpp: CHPP
        """
        # If set, check ht_id integrity and add to request arguments
        if not isinstance(ht_id, int):
            raise ValueError("ht_id must be an integer")
        self._REQUEST_ARGS = dict()
        self._REQUEST_ARGS["teamID"] = ht_id

        super().__init__(**kwargs)

    def __repr__(self):
        return f"<{str(self.__class__.__name__)} object : " \
               f"{self.team_name} ({self.ht_id}) >"


class HTNationalTeams(ht_model.HTModel):
    """
    Hattrick National Teams list
    """

    _SOURCE_FILE = "nationalteams"
    _SOURCE_FILE_VERSION = "1.6"

    _URL_PATH = "/World/NationalTeams/NationalTeams.aspx?" + \
                "viewType=1&leagueOfficeTypeId="

    _ht_attributes = []

    def __init__(self, ht_id=2, **kwargs):
        """
        Initialization of a HTNationalTeam instance

        :param ht_id: ID of NT type teams to get
                      (2 = National teams, 4 = U-20 Teams)
        :type ht_id: int
        :key chpp: CHPP instance of connected user, must be a chpp.CHPP object
        """
        if ht_id is not None and not isinstance(ht_id, int):
            raise ValueError("ht_id must be an integer")

        self._REQUEST_ARGS = dict()
        self._REQUEST_ARGS["LeagueOfficeTypeID"] = ht_id
        self.ht_id = ht_id

        super().__init__(**kwargs)

        self.teams = [HTNationalTeamEntry(chpp=self._chpp, data=team)
                      for team in self._data
                                      .find("NationalTeams")
                                      .findall("NationalTeam")]


class HTNationalTeamEntry(ht_model.HTModel):
    """
    Hattrick National Team entry
    """

    _URL_PATH = "/Club/NationalTeam/NationalTeam.aspx?teamId="

    @property
    def _ht_attributes(self):
        return [
            ("ht_id", "NationalTeamID",
             ht_xml.HTXml.ht_int,),
            ("team_name", "NationalTeamName",
             ht_xml.HTXml.ht_str,),
            ("dress", "Dress",
             ht_xml.HTXml.ht_str,),
            ("rating_score", "RatingScores",
             ht_xml.HTXml.ht_int,)
        ]

    def __repr__(self):
        return f"<{str(self.__class__.__name__)} object : " \
               f"{self.team_name} ({self.ht_id}) >"
