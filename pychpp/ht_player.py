from pychpp import ht_model, ht_xml
from pychpp import ht_team
from pychpp import ht_transfer


class HTCorePlayer(ht_model.HTModel):
    """
    Core Hattrick player
    Used to create HTPlayer and HTYouthPlayer classes
    """

    def __init__(self, ht_id=None, team_ht_id=None, **kwargs):
        """
        Initialize HTCorePlayer instance

        :param ht_id: player Hattrick ID (have to be defined if data is None),
        defaults to None
        :param team_ht_id: team Hattrick ID of player's team
        (have to be defined if ht_id is None), defaults to None
        :type ht_id: int, optional
        :type team_ht_id: int, optional
        :key chpp: CHPP instance of connected user, must be a chpp.CHPP object
        :key data: xml data to serialize (have to be defined if ht_id is None),
        defaults to None
        """

        # Init depends on given parameters
        # If data is not defined, ht_id has to be defined
        if kwargs.get("data", None) is None:
            # Check ht_id integrity as data is not defined
            if ht_id is None:
                raise ValueError(
                    "ht_id have to be defined when data is not defined")
            elif not isinstance(ht_id, int):
                raise ValueError("ht_id parameter have to be a integer")
            else:
                self.ht_id = ht_id

        elif kwargs["data"].tag not in ("Player", "YouthPlayer"):
            raise ValueError(
                "data's root tag must be equal to 'Player' or 'YouthPlayer'")

        elif team_ht_id is None:
            raise ValueError("team_ht_id must be defined as data is defined")

        self.team_ht_id = team_ht_id

        super().__init__(**kwargs)

    def __str__(self):
        """
        Pretty print with :
          - First name, last name
          - Age
          - Skills
        """
        lines = [f"{self.first_name} {self.last_name} ({self.ht_id})",
                 self.age.__str__(),
                 "\n".join([self.skills[i].__str__()
                            for i in self._PRETTY_PRINT_ORDER])
                 ]
        return "\n".join(lines)

    def __repr__(self):
        return f"<{self.__class__.__name__} object : " \
               f"{self.first_name} {self.last_name} ({self.ht_id})>"


class HTPlayer(HTCorePlayer):
    """
    Hattrick senior player
    """

    _SOURCE_FILE = "playerdetails"
    _SOURCE_FILE_VERSION = "2.8"
    _PRETTY_PRINT_ORDER = ["stamina", "keeper", "defender", "playmaker",
                           "winger", "passing", "scorer", "set_pieces"]

    _URL_PATH = "/Club/Players/Player.aspx?playerId="

    _ht_attributes = [("ht_id", ".//PlayerID", ht_xml.HTXml.ht_int,),
                      ("first_name", ".//FirstName", ht_xml.HTXml.ht_str,),
                      ("nick_name", ".//NickName", ht_xml.HTXml.ht_str,),
                      ("last_name", ".//LastName", ht_xml.HTXml.ht_str,),
                      ("number", ".//PlayerNumber", ht_xml.HTXml.ht_int,),
                      ("category_id", ".//PlayerCategoryID",
                       ht_xml.HTXml.ht_int,),
                      ("owner_notes", ".//OwnerNotes", ht_xml.HTXml.ht_str,),
                      ("age_years", ".//Age", ht_xml.HTXml.ht_int,),
                      ("age_days", ".//AgeDays", ht_xml.HTXml.ht_int,),
                      ("age", ".//Age/..", ht_xml.HTXml.ht_age,),
                      ("next_birthday", ".//NextBirthDay",
                       ht_xml.HTXml.ht_datetime_from_text,),
                      ("arrival_date", ".//ArrivalDate",
                       ht_xml.HTXml.ht_datetime_from_text,),
                      ("form", ".//PlayerForm", ht_xml.HTXml.ht_int,),
                      ("cards", ".//Cards", ht_xml.HTXml.ht_int,),
                      ("injury_level", ".//InjuryLevel", ht_xml.HTXml.ht_int,),
                      ("statement", ".//Statement", ht_xml.HTXml.ht_str,),
                      ("language", ".//PlayerLanguage", ht_xml.HTXml.ht_str,),
                      ("language_id", ".//PlayerLanguageID",
                       ht_xml.HTXml.ht_int,),

                      # Trainer
                      ("trainer_type", ".//TrainerData/TrainerType",
                       ht_xml.HTXml.ht_int,),
                      ("trainer_skill", ".//TrainerData/TrainerSkill",
                       ht_xml.HTXml.ht_int,),

                      ("agreeability", ".//Agreeability",
                       ht_xml.HTXml.ht_int,),
                      ("aggressiveness", ".//Aggressiveness",
                       ht_xml.HTXml.ht_int,),
                      ("honesty", ".//Honesty", ht_xml.HTXml.ht_int,),
                      ("experience", ".//Experience", ht_xml.HTXml.ht_int,),
                      ("loyalty", ".//Loyalty", ht_xml.HTXml.ht_int,),
                      ("mother_club_bonus", ".//MotherClubBonus",
                       ht_xml.HTXml.ht_bool,),
                      ("leadership", ".//Leadership", ht_xml.HTXml.ht_int,),
                      ("specialty", ".//Specialty", ht_xml.HTXml.ht_int,),
                      ("native_country_id", ".//NativeCountryID",
                       ht_xml.HTXml.ht_int,),
                      ("native_league_id", ".//NativeLeagueID",
                       ht_xml.HTXml.ht_int,),
                      ("native_league_name", ".//NativeLeagueName",
                       ht_xml.HTXml.ht_str,),
                      ("tsi", ".//TSI", ht_xml.HTXml.ht_int,),
                      ("salary", ".//Salary", ht_xml.HTXml.ht_int,),
                      ("is_abroad", ".//IsAbroad", ht_xml.HTXml.ht_bool,),
                      ("skills", ".//StaminaSkill/..",
                       ht_xml.HTXml.ht_skills,),
                      ("caps", ".//Caps", ht_xml.HTXml.ht_int,),
                      ("caps_u20", ".//CapsU20", ht_xml.HTXml.ht_int,),
                      ("career_goals", ".//CareerGoals", ht_xml.HTXml.ht_int,),
                      ("career_hattricks", ".//CareerHattricks",
                       ht_xml.HTXml.ht_int,),
                      ("league_goals", ".//LeagueGoals", ht_xml.HTXml.ht_int,),
                      ("cup_goals", ".//CupGoals", ht_xml.HTXml.ht_int,),
                      ("friendly_goals", ".//FriendliesGoals",
                       ht_xml.HTXml.ht_int,),
                      ("current_team_matches", ".//MatchesCurrentTeam",
                       ht_xml.HTXml.ht_int,),
                      ("current_team_goals", ".//GoalsCurrentTeam",
                       ht_xml.HTXml.ht_int,),
                      ("national_team_id", ".//NationalTeamID",
                       ht_xml.HTXml.ht_int,),
                      ("national_team_name", ".//NationalTeamName",
                       ht_xml.HTXml.ht_str,),
                      ("is_transfer_listed", ".//TransferListed",
                       ht_xml.HTXml.ht_bool,),
                      ("team_ht_id", ".//OwningTeam/TeamID",
                       ht_xml.HTXml.ht_int,),
                      ]

    def __init__(self, **kwargs):
        """
        Initialize HTPlayer instance

        :key chpp: CHPP instance of connected user
        :key ht_id: player Hattrick ID (have to be defined if data is None),
        defaults to None
        :key data: ElementTree data to serialize
        (have to be defined if ht_id is None), defaults to None
        :key team_ht_id: team Hattrick ID of player's team
        (have to be defined if ht_id is None), defaults to None
        :type chpp: CHPP
        :type ht_id: int, optional
        :type data: xml.ElementTree.Element, optional
        :type team_ht_id: int, optional
        """
        self._REQUEST_ARGS = dict()
        if kwargs.get("ht_id", None) is not None:
            self._REQUEST_ARGS["playerID"] = kwargs["ht_id"]

        super().__init__(**kwargs)

        # Add transfer_details attribute
        # By default, set it to None
        # Filled if player is transfer listed
        self.transfer_details = None

        if self.is_transfer_listed is True:
            self.transfer_details = (
                ht_transfer.HTTransferDetails(chpp=self._chpp,
                                              data=self._data,
                                              ))

            # If HTTransfertDetails.asking_price is None,
            # it means that transfer details is not available
            # In this, set transfer_details attribute to None
            if self.transfer_details.asking_price is None:
                self.transfer_details = None

    @property
    def team(self):
        return ht_team.HTTeam(chpp=self._chpp, ht_id=self.team_ht_id)


class HTYouthPlayer(HTCorePlayer):
    """
    Hattrick youth player
    """

    _SOURCE_FILE = "youthplayerdetails"
    _SOURCE_FILE_VERSION = "1.1"
    _PRETTY_PRINT_ORDER = ["keeper", "defender", "playmaker", "winger",
                           "passing", "scorer", "set_pieces"]

    _URL_PATH = "/Club/Players/YouthPlayer.aspx?YouthPlayerID="

    _ht_attributes = [("ht_id", ".//YouthPlayerID", ht_xml.HTXml.ht_int,),
                      ("first_name", ".//FirstName", ht_xml.HTXml.ht_str,),
                      ("nick_name", ".//NickName", ht_xml.HTXml.ht_str,),
                      ("last_name", ".//LastName", ht_xml.HTXml.ht_str,),
                      ("number", ".//PlayerNumber", ht_xml.HTXml.ht_int,),
                      ("category_id", ".//PlayerCategoryID",
                       ht_xml.HTXml.ht_int,),
                      ("owner_notes", ".//OwnerNotes", ht_xml.HTXml.ht_str,),
                      ("age_years", ".//Age", ht_xml.HTXml.ht_int,),
                      ("age_days", ".//AgeDays", ht_xml.HTXml.ht_int,),
                      ("age", ".//Age/..", ht_xml.HTXml.ht_age,),
                      ("arrival_date", ".//ArrivalDate",
                       ht_xml.HTXml.ht_datetime_from_text,),
                      ("can_be_promoted_in", ".//CanBePromotedIn",
                       ht_xml.HTXml.ht_int,),
                      ("cards", ".//Cards", ht_xml.HTXml.ht_int,),
                      ("injury_level", ".//InjuryLevel", ht_xml.HTXml.ht_int,),
                      ("statement", ".//Statement", ht_xml.HTXml.ht_str,),
                      ("specialty", ".//Specialty", ht_xml.HTXml.ht_int,),
                      ("career_goals", ".//CareerGoals", ht_xml.HTXml.ht_int,),
                      ("career_hattricks", ".//CareerHattricks",
                       ht_xml.HTXml.ht_int,),
                      ("league_goals", ".//LeagueGoals", ht_xml.HTXml.ht_int,),
                      ("friendly_goals", ".//FriendliesGoals",
                       ht_xml.HTXml.ht_int,),
                      ("team_id", ".//OwningYouthTeam/YouthTeamID",
                       ht_xml.HTXml.ht_int,),
                      ("skills", ".//KeeperSkill/..",
                       ht_xml.HTXml.ht_youth_skills,)
                      ]

    def __init__(self, **kwargs):
        """
        Initialize HTYouthPlayer instance

        :key chpp: CHPP instance of connected user
        :key ht_id: player Hattrick ID (have to be defined if data is None),
        defaults to None
        :key data: ElementTree data to serialize
        (have to be defined if ht_id is None), defaults to None
        :key team_ht_id: team Hattrick ID of player's team
        (have to be defined if ht_id is None), defaults to None
        :type chpp: CHPP
        :type ht_id: int, optional
        :type data: xml.ElementTree.Element, optional
        :type team_ht_id: int, optional
        """

        self._REQUEST_ARGS = dict()

        if kwargs.get("ht_id", None) is not None:
            self._REQUEST_ARGS["youthPlayerId"] = kwargs["ht_id"]

        # team_ht_id is defined by arguments or inside xml data
        if kwargs.get("data", None) is not None:
            self.team_ht_id = kwargs["team_ht_id"]

        super().__init__(**kwargs)


class HTLineupPlayer(HTCorePlayer):
    """
    Hattrick lineup player
    """

    _ht_attributes = [("ht_id", ".//PlayerID", ht_xml.HTXml.ht_int,),
                      ("role_id", ".//RoleID", ht_xml.HTXml.ht_int,),
                      ("first_name", ".//FirstName", ht_xml.HTXml.ht_str,),
                      ("nick_name", ".//NickName", ht_xml.HTXml.ht_str,),
                      ("last_name", ".//LastName", ht_xml.HTXml.ht_str,),
                      ("rating_stars", ".//RatingStars",
                       ht_xml.HTXml.ht_float,),
                      ("rating_stars_eom", ".//RatingStarsEndOfMatch",
                       ht_xml.HTXml.ht_float,),
                      ("behaviour", ".//Behaviour", ht_xml.HTXml.ht_int,)
                      ]

    def __init__(self, is_youth: bool = False, **kwargs):
        """
        Initialize HTLineupPlayer instance

        :key chpp: CHPP instance of connected user
        :key ht_id: player Hattrick ID (have to be defined if data is None),
        defaults to None
        :key data: ElementTree data to serialize
        (have to be defined if ht_id is None), defaults to None
        :key team_ht_id: team Hattrick ID of player's team
        (have to be defined if ht_id is None), defaults to None
        :type chpp: CHPP
        :type ht_id: int, optional
        :type data: xml.ElementTree.Element, optional
        :type team_ht_id: int, optional
        """
        super().__init__(**kwargs)
        self.is_youth = is_youth

    @property
    def role_name(self):
        role_names = {100: 'Keeper', 101: 'Right back',
                      102: 'Right central defender',
                      103: 'Middle central defender',
                      104: 'Left central defender', 105: 'Left back',
                      106: 'Right winger', 107: 'Right inner midfield',
                      108: 'Middle inner midfield', 109: 'Left inner midfield',
                      110: 'Left winger', 111: 'Right forward',
                      112: 'Middle forward', 113: 'Left forward',
                      114: 'Substitution (Keeper)',
                      115: 'Substitution (Defender)',
                      116: 'Substitution (Inner midfield)',
                      117: 'Substitution (Winger)',
                      118: 'Substitution (Forward)',
                      200: 'Substitution (Keeper)',
                      201: 'Substitution (Central defender)',
                      202: 'Substitution (Wing back)',
                      203: 'Substitution (Inner midfielder)',
                      204: 'Substitution (Forward)',
                      205: 'Substitution (Winger)',
                      206: 'Substitution (Extra)',
                      207: 'Backup (Keeper)',
                      208: 'Backup (Central defender)',
                      209: 'Backup (Wing back)',
                      210: 'Backup (Inner midfielder)',
                      211: 'Backup (Forward)', 212: 'Backup (Winger)',
                      213: 'Backup (Extra)', 17: 'Set pieces',
                      18: 'Captain', 19: 'Replaced Player #1',
                      20: 'Replaced Player #2', 21: 'Replaced Player #3',
                      22: 'Penalty taker (1)', 23: 'Penalty taker (2)',
                      24: 'Penalty taker (3)', 25: 'Penalty taker (4)',
                      26: 'Penalty taker (5)', 27: 'Penalty taker (6)',
                      28: 'Penalty taker (7)', 29: 'Penalty taker (8)',
                      30: 'Penalty taker (9)', 31: 'Penalty taker (10)',
                      32: 'Penalty taker (11)'}
        return role_names.get(self.role_id, "Unknown role")

    @property
    def player(self):
        return (HTYouthPlayer(chpp=self._chpp, ht_id=self.ht_id)
                if self.is_youth
                else HTPlayer(chpp=self._chpp, ht_id=self.ht_id))

    @property
    def url(self):
        return self.player.url
