from pychpp import ht_model
from pychpp import ht_error, ht_region, ht_xml


class HTWorld(ht_model.HTModel):
    """
    Hattrick world details
    """

    _SOURCE_FILE = "worlddetails"
    _SOURCE_FILE_VERSION = "1.8"

    _ht_attributes = []

    def __init__(self, ht_id=None, include_regions=False,
                 source="hattrick", **kwargs):
        """
        Initialization of a HTWorld instance

        :param ht_id: Hattrick ID of league
        :param include_regions: Boolean to indicate
        if regions need to be fetched for the countries
        :param source: hattrick source to request
        ('hattrick', 'youth' or 'hto')
        :type ht_id: int
        :type include_regions: bool
        :type source: str
        :key chpp: CHPP instance of connected user, must be a chpp.CHPP object
        """
        if ht_id is not None and not isinstance(ht_id, int):
            raise ValueError("ht_id must be an integer")
        elif source not in ("hattrick", "youth", "htointegrated"):
            raise ValueError(
                "source must be equal to 'hattrick, "
                "'youth' or 'htointegrated'")

        self._REQUEST_ARGS = dict()
        if ht_id is not None:
            self.ht_id = ht_id
            self._REQUEST_ARGS["leagueID"] = str(ht_id)
        self._REQUEST_ARGS["includeRegions"] = include_regions
        self._REQUEST_ARGS["sourceSystem"] = source

        super().__init__(**kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__} object>"

    @property
    def leagues(self):
        return [HTCountryLeague(chpp=self._chpp, data=p_data)
                for p_data in self._data.find("LeagueList").findall("League")]

    def league(self, ht_id=None, name=None):
        if ht_id is None and name is None:
            raise ValueError("ht_id or name must be set")

        if ht_id is not None:
            try:
                return list(filter(lambda k: k.ht_id == ht_id,
                                   self.leagues))[0]
            except IndexError:
                raise ht_error.UnknownLeagueError(
                    f"League with ID={ht_id} does not exist")
        else:
            try:
                return list(
                    filter(lambda k: k.english_name.lower() == name.lower(),
                           self.leagues))[0]
            except IndexError:
                raise ht_error.UnknownLeagueError(
                    f"League with name={name} does not exist")


class HTCountryLeague(ht_model.HTModel):
    """
    Hattrick country league
    """

    _URL_PATH = "/World/Leagues/League.aspx?LeagueID="

    _ht_attributes = [("ht_id", ".//LeagueID",
                       ht_xml.HTXml.ht_int,),
                      ("league_name", ".//LeagueName",
                       ht_xml.HTXml.ht_str,),
                      ("season", ".//Season",
                       ht_xml.HTXml.ht_int,),
                      ("season_offset", ".//SeasonOffset",
                       ht_xml.HTXml.ht_int,),
                      ("match_round", ".//MatchRound",
                       ht_xml.HTXml.ht_int,),
                      ("short_name", ".//ShortName",
                       ht_xml.HTXml.ht_str,),
                      ("continent", ".//Continent",
                       ht_xml.HTXml.ht_str,),
                      ("zone_name", ".//ZoneName",
                       ht_xml.HTXml.ht_str,),
                      ("english_name", ".//EnglishName",
                       ht_xml.HTXml.ht_str,),
                      ("national_team_id", ".//NationalTeamId",
                       ht_xml.HTXml.ht_int,),
                      ("u20_team_id", ".//U20teamId",
                       ht_xml.HTXml.ht_int,),
                      ("active_teams", ".//ActiveTeams",
                       ht_xml.HTXml.ht_int,),
                      ("active_users", ".//ActiveUsers",
                       ht_xml.HTXml.ht_int,),
                      ("waiting_users", ".//WaitingUsers",
                       ht_xml.HTXml.ht_int,),
                      ("training_date", ".//TrainingDate",
                       ht_xml.HTXml.ht_datetime_from_text,),
                      ("cup_match_date", ".//CupMatchDate",
                       ht_xml.HTXml.ht_datetime_from_text,),
                      ("series_match_date", ".//SeriesMatchDate",
                       ht_xml.HTXml.ht_datetime_from_text,),
                      ("number_of_levels", ".//NumberOfLevels",
                       ht_xml.HTXml.ht_int,)
                      ]

    def __init__(self, **kwargs):
        """
        Initialize HTCountryLeague instance

        :key chpp: CHPP instance of connected user
        :key data: ElementTree data to serialize
        (have to be defined if ht_id is None), defaults to None
        :type chpp: CHPP
        :type data: xml.ElementTree.Element, optional
        """
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__} object : " \
               f"{self.league_name} ({self.ht_id})>"

    @property
    def country(self):
        return HTCountry(chpp=self._chpp, data=self._data.find("Country"))

    @property
    def cups(self):
        return [HTCup(chpp=self._chpp, data=p_data)
                for p_data in self._data.find("Cups").findall("Cup")]


class HTCountry(ht_model.HTModel):
    """
    Hattrick country
    """

    _ht_attributes = [("ht_id", ".//CountryID",
                       ht_xml.HTXml.ht_int,),
                      ("country_name", ".//CountryName",
                       ht_xml.HTXml.ht_str,),
                      ("currency_name", ".//CurrencyName",
                       ht_xml.HTXml.ht_str,),
                      ("currency_rate", ".//CurrencyRate",
                       ht_xml.HTXml.ht_float,),
                      ("country_code", ".//CountryCode",
                       ht_xml.HTXml.ht_str,),
                      ]

    def __init__(self, **kwargs):
        """
        Initialize HTCountryLeague instance

        :key chpp: CHPP instance of connected user
        :key data: ElementTree data to serialize
        (have to be defined if ht_id is None), defaults to None
        :type chpp: CHPP
        :type data: xml.ElementTree.Element, optional
        """
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__} object : " \
               f"{self.country_name} ({self.ht_id})>"

    @property
    def regions(self):
        if self._data.find("RegionList") is not None:
            return [
                HTRegionItem(
                    chpp=self._chpp,
                    ht_id=p_data.find("RegionID").text,
                    name=p_data.find("RegionName").text
                )
                for p_data in self._data.find("RegionList").findall("Region")
            ]


class HTCup(ht_model.HTModel):
    """
    Hattrick country cup
    """

    _URL_PATH = "/World/Cup/Cup.aspx?CupID="

    _ht_attributes = [("ht_id", ".//CupID",
                       ht_xml.HTXml.ht_int,),
                      ("cup_name", ".//CupName",
                       ht_xml.HTXml.ht_str,),
                      ("cup_league_level", ".//CupLeagueLevel",
                       ht_xml.HTXml.ht_int,),
                      ("cup_level", ".//CupLevel",
                       ht_xml.HTXml.ht_int,),
                      ("cup_level_index", ".//CupLevelIndex",
                       ht_xml.HTXml.ht_int,),
                      ("match_round", ".//MatchRound",
                       ht_xml.HTXml.ht_int,),
                      ("match_rounds_left", ".//MatchRoundsLeft",
                       ht_xml.HTXml.ht_int,)
                      ]

    def __init__(self, **kwargs):
        """
        Initialize HTCup instance

        :key chpp: CHPP instance of connected user
        :key data: ElementTree data to serialize
        (have to be defined if ht_id is None), defaults to None
        :type chpp: CHPP
        :type data: xml.ElementTree.Element, optional
        """
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__} object : " \
               f"{self.cup_name} ({self.ht_id})>"

    @property
    def cup_league_level_name(self):
        if self.cup_league_level == 0:
            return "National"
        return "Divisional"

    @property
    def cup_level_name(self):
        if self.cup_level == 1:
            return "National/Divisional"
        elif self.cup_level == 2:
            return "Challenger"
        else:
            return "Consolation"

    @property
    def cup_level_index_name(self):
        if self.cup_level in [1, 3]:
            return "National/Consolation"
        else:
            if self.cup_level_index == 1:
                return "Emerald"
            elif self.cup_level_index == 2:
                return "Ruby"
            else:
                return "Sapphire"


class HTRegionItem:
    """
    Hattrick country region item
    """

    def __init__(self, chpp, ht_id, name, **kwargs):
        """
        Initialize HTRegionItem instance

        :key chpp: CHPP instance of connected user
        :key ht_id: Hattrick ID of the region
        :key name: Hattrick name of the region
        :type chpp: CHPP
        :type ht_id: int
        :type name: str
        """
        self.chpp = chpp
        self.ht_id = ht_id
        self.name = name

    def __repr__(self):
        return f"<{self.__class__.__name__} object : " \
               f"{self.name} ({self.ht_id})>"

    @property
    def region(self):
        return ht_region.HTRegion(chpp=self.chpp, ht_id=self.ht_id)
