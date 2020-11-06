from pychpp import ht_model, ht_xml
from pychpp import ht_user, ht_player, ht_arena
from werkzeug.utils import cached_property


class HTCoreTeam(ht_model.HTModel):
    """
    Core Hattrick team
    Used to create HTTeam and HTYouthTeam classes
    """

    def __init__(self, ht_id=None, **kwargs):
        """
        Initialize HTCoreTeam instance

        :param ht_id: team Hattrick ID
        (if none, fetch the primary club of connected user), defaults to None
        :key chpp: CHPP instance of connected user
        :type ht_id: int, optional
        :type chpp: CHPP
        """
        # If set, check ht_id integrity and add to request arguments
        # If not set, request will fetch team of current user
        if not isinstance(ht_id, int) and ht_id is not None:
            raise ValueError("ht_id must be an integer")

        super().__init__(**kwargs)

    def __repr__(self):
        return f"<{str(self.__class__.__name__)} object : " \
               f"{self.name} ({self.ht_id}) >"


class HTTeam(HTCoreTeam):
    """
    Hattrick team
    """

    _SOURCE_FILE = "teamdetails"
    _SOURCE_FILE_VERSION = "3.4"

    _URL_PATH = "/Club/?TeamID="

    @property
    def _ht_attributes(self):

        ht_filter = f"[TeamID='{self._REQUEST_ARGS.get('teamID', '')}']" if (
            self._REQUEST_ARGS.get("teamID", "")) else ""

        return [("ht_id",
                 f"Teams/Team{ht_filter}/TeamID",
                 ht_xml.HTXml.ht_int),
                # General team information
                ("name",
                 f"Teams/Team{ht_filter}/TeamName",
                 ht_xml.HTXml.ht_str),
                ("short_name",
                 f"Teams/Team{ht_filter}/ShortTeamName",
                 ht_xml.HTXml.ht_str),
                ("is_primary_club",
                 f"Teams/Team{ht_filter}/IsPrimaryClub",
                 ht_xml.HTXml.ht_bool),
                ("founded_date",
                 f"Teams/Team{ht_filter}/FoundedDate",
                 ht_xml.HTXml.ht_datetime_from_text),
                ("is_bot",
                 f"Teams/Team{ht_filter}/BotStatus/IsBot",
                 ht_xml.HTXml.ht_bool),
                # Arena
                ("arena_ht_id",
                 f"Teams/Team{ht_filter}/Arena/ArenaID",
                 ht_xml.HTXml.ht_int),
                ("arena_name",
                 f"Teams/Team{ht_filter}/Arena/ArenaName",
                 ht_xml.HTXml.ht_str),
                # Country
                ("country_ht_id",
                 f"Teams/Team{ht_filter}/Country/CountryID",
                 ht_xml.HTXml.ht_int),
                ("country_name",
                 f"Teams/Team{ht_filter}/Country/CountryName",
                 ht_xml.HTXml.ht_str),
                # Region
                ("region_ht_id",
                 f"Teams/Team{ht_filter}/Region/RegionID",
                 ht_xml.HTXml.ht_int),
                ("region_name",
                 f"Teams/Team{ht_filter}/Region/RegionID",
                 ht_xml.HTXml.ht_str),
                # Trainer
                ("trainer_ht_id",
                 f"Teams/Team{ht_filter}/Trainer/PlayerID",
                 ht_xml.HTXml.ht_int),
                # Homepage
                ("homepage",
                 f"Teams/Team{ht_filter}/HomePage",
                 ht_xml.HTXml.ht_str),
                # Cup
                ("still_in_cup",
                 f"Teams/Team{ht_filter}/Cup/StillinCup",
                 ht_xml.HTXml.ht_bool),
                ("cup_ht_id",
                 f"Teams/Team{ht_filter}/Cup/CupID",
                 ht_xml.HTXml.ht_int),
                ("cup_name",
                 f"Teams/Team{ht_filter}/Cup/CupName",
                 ht_xml.HTXml.ht_str),
                ("cup_league_level",
                 f"Teams/Team{ht_filter}/Cup/CupLeagueLevel",
                 ht_xml.HTXml.ht_int),
                ("cup_level",
                 f"Teams/Team{ht_filter}/Cup/CupLevel",
                 ht_xml.HTXml.ht_int),
                ("cup_level_index",
                 f"Teams/Team{ht_filter}/Cup/CupLevelIndex",
                 ht_xml.HTXml.ht_int),
                ("cup_match_round",
                 f"Teams/Team{ht_filter}/Cup/MatchRound",
                 ht_xml.HTXml.ht_int),
                ("cup_match_rounds_left",
                 f"Teams/Team{ht_filter}/Cup/MatchRoundsLeft",
                 ht_xml.HTXml.ht_int),
                # PowerRating
                ("power_rating_global_ranking",
                 f"Teams/Team{ht_filter}/PowerRating/GlobalRanking",
                 ht_xml.HTXml.ht_int),
                ("power_rating_league_ranking",
                 f"Teams/Team{ht_filter}/PowerRating/LeagueRanking",
                 ht_xml.HTXml.ht_int),
                ("power_rating_region_ranking",
                 f"Teams/Team{ht_filter}/PowerRating/RegionRanking",
                 ht_xml.HTXml.ht_int),
                ("power_rating",
                 f"Teams/Team{ht_filter}/PowerRating/PowerRating",
                 ht_xml.HTXml.ht_int),

                # User
                ("user_ht_id",
                 "User/UserID",
                 ht_xml.HTXml.ht_int),
                ("supporter_tier",
                 "User/SupporterTier",
                 ht_xml.HTXml.ht_str),
                ("user_login",
                 "User/Loginname",
                 ht_xml.HTXml.ht_str),
                ("user_fullname",
                 "User/Name",
                 ht_xml.HTXml.ht_str),
                ("user_icq",
                 "User/ICQ",
                 ht_xml.HTXml.ht_str),
                ("user_signup_date",
                 "User/SignupDate",
                 ht_xml.HTXml.opt_ht_datetime_from_text),
                ("user_activation_date",
                 "User/ActivationDate",
                 ht_xml.HTXml.ht_datetime_from_text),
                ("user_last_login_date",
                 "User/LastLoginDate",
                 ht_xml.HTXml.opt_ht_datetime_from_text),
                ("user_has_manager_license",
                 "User/HasManagerLicese",
                 ht_xml.HTXml.ht_bool),
                # Youth team
                ("youth_team_ht_id",
                 f"Teams/Team{ht_filter}/YouthTeamID",
                 ht_xml.HTXml.ht_int),
                ("youth_team_name",
                 f"Teams/Team{ht_filter}/YouthTeamName",
                 ht_xml.HTXml.ht_str),
                ]

    def __init__(self, **kwargs):
        """
        Initialize HTTeam instance

        :key ht_id: team Hattrick ID
        (if none, fetch the primary club of connected user), defaults to None
        :key chpp: CHPP instance of connected user
        :type ht_id: int, optional
        :type chpp: CHPP
        """
        self._REQUEST_ARGS = dict()

        if kwargs.get("ht_id", None) is not None:
            self._REQUEST_ARGS["teamID"] = kwargs["ht_id"]

        super().__init__(**kwargs)

    @property
    def user(self):
        """Owner of the current team"""
        return ht_user.HTUser(chpp=self._chpp, ht_id=self.user_ht_id)

    @property
    def players(self):
        """Players list of current team"""
        data = self._chpp.request(
            file="players",
            version="2.4",
            actionType="view",
            teamID=self.ht_id).find("Team").find("PlayerList")

        return [ht_player.HTPlayer(chpp=self._chpp,
                                   data=p_data,
                                   team_ht_id=self.ht_id)
                for p_data in data.findall("Player")]

    @property
    def youth_team(self):
        """Youth team of current team"""
        return HTYouthTeam(chpp=self._chpp,
                           ht_id=self.youth_team_ht_id,
                           ) if self.youth_team_ht_id != 0 else None

    @property
    def arena(self):
        """Team arena"""
        return ht_arena.HTArena(chpp=self._chpp, ht_id=self.arena_ht_id)


class HTYouthTeam(HTCoreTeam):
    """
    Hattrick youth team
    """

    _SOURCE_FILE = "youthteamdetails"
    _SOURCE_FILE_VERSION = "1.1"

    _URL_PATH = "/Club/Youth/?YouthTeamID="

    _ht_attributes = [("ht_id", "YouthTeam/YouthTeamID",
                       ht_xml.HTXml.ht_int,),
                      # General information
                      ("name", "YouthTeam/YouthTeamName",
                       ht_xml.HTXml.ht_str,),
                      ("short_name", "YouthTeam/ShortTeamName",
                       ht_xml.HTXml.ht_str,),
                      ("created_date", "YouthTeam/CreatedDate",
                       ht_xml.HTXml.ht_datetime_from_text,),
                      # Country
                      ("country_id", "YouthTeam/Country/CountryID",
                       ht_xml.HTXml.ht_int,),
                      ("country_name", "YouthTeam/Country/CountryName",
                       ht_xml.HTXml.ht_str,),
                      # Region
                      ("region_id", "YouthTeam/Region/RegionID",
                       ht_xml.HTXml.ht_int,),
                      ("region_name", "YouthTeam/Region/RegionName",
                       ht_xml.HTXml.ht_str,),
                      # Arena
                      ("arena_id", "YouthTeam/YouthArena/YouthArenaID",
                       ht_xml.HTXml.ht_int,),
                      ("arena_name", "YouthTeam/YouthArena/YouthArenaName",
                       ht_xml.HTXml.ht_str,),
                      # League
                      ("league_id", "YouthTeam/YouthLeague/YouthLeagueID",
                       ht_xml.HTXml.ht_int,),
                      ("league_name", "YouthTeam/YouthLeague/YouthLeagueName",
                       ht_xml.HTXml.ht_str,),
                      ("league_status",
                       "YouthTeam/YouthLeague/YouthLeagueStatus",
                       ht_xml.HTXml.ht_int,),
                      # Senior team
                      ("senior_team_id",
                       "YouthTeam/OwningTeam/MotherTeamID",
                       ht_xml.HTXml.ht_int,),
                      ("senior_team_name",
                       "YouthTeam/OwningTeam/MotherTeamName",
                       ht_xml.HTXml.ht_str,),
                      # Trainer
                      ("trainer_id",
                       "YouthTeam/YouthTrainer/YouthPlayerID",
                       ht_xml.HTXml.ht_int,),
                      # Next training match date
                      ("next_training_match_date",
                       "YouthTeam/NextTrainingMatchDate",
                       ht_xml.HTXml.ht_datetime_from_text,),
                      ]

    def __init__(self, **kwargs):
        """
        Initialize HTYouthTeam instance

        :key chpp: CHPP instance of connected user
        :key ht_id: team Hattrick ID
        (if none, fetch the primary club of connected user), defaults to None
        :type chpp: CHPP
        :type ht_id: int, optional
        """
        self._REQUEST_ARGS = dict()

        if kwargs.get("ht_id", None) is not None:
            self._REQUEST_ARGS["youthTeamId"] = kwargs["ht_id"]

        super().__init__(**kwargs)

    @property
    def players(self):
        """Players list of current team"""
        data = self._chpp.request(file="youthplayerlist",
                                  version="2.4",
                                  actionType="details",
                                  youthTeamID=self.ht_id).find("PlayerList")

        # Force fetch if ht_id is None
        if self._data is None:
            self._fetch()

        return [ht_player.HTYouthPlayer(chpp=self._chpp,
                                        data=p_data,
                                        team_ht_id=self.ht_id)
                for p_data in data.findall("YouthPlayer")]


class HTTeamRank(HTCoreTeam):

    _URL_PATH = "/Club/?TeamID="

    _ht_attributes = [
        ("user_ht_id", "UserId", ht_xml.HTXml.ht_int,),
        ("team_ht_id", "TeamID", ht_xml.HTXml.ht_int,),
        ("team_name", "TeamName", ht_xml.HTXml.ht_str,),
        ("position", "Position", ht_xml.HTXml.ht_int,),
        ("position_change", "PositionChange", ht_xml.HTXml.ht_int,),
        ("matches", "Matches", ht_xml.HTXml.ht_int,),
        ("goals_for", "GoalsFor", ht_xml.HTXml.ht_int,),
        ("goals_against", "GoalsAgainst", ht_xml.HTXml.ht_int,),
        ("points", "Points", ht_xml.HTXml.ht_int,),
        ("won", "Won", ht_xml.HTXml.ht_int,),
        ("draws", "Draws", ht_xml.HTXml.ht_int,),
        ("lost", "Lost", ht_xml.HTXml.ht_int,),
    ]

    @cached_property
    def details(self):
        return self._chpp.team(ht_id=self.team_ht_id)

    def __repr__(self):
        return f"<{str(self.__class__.__name__)} object : " \
               f"#{self.position} {self.team_name} ({self.team_ht_id}) >"
