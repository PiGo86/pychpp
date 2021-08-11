from pychpp import ht_model
from pychpp import ht_arena, ht_match, ht_player, ht_team, ht_xml


class HTMatchLineup(ht_model.HTModel):
    """
    Hattrick match lineup
    """

    _SOURCE_FILE = "matchlineup"
    _SOURCE_FILE_VERSION = "2.0"

    _URL_PATH = "/Club/Matches/Match.aspx?matchID="

    _ht_attributes = [("ht_id", "MatchID", ht_xml.HTXml.ht_int),

                      # General information
                      ("game_type", "MatchType", ht_xml.HTXml.ht_int),
                      ("is_youth", "IsYouth", ht_xml.HTXml.ht_bool),

                      # Home team
                      ("home_team_id", "HomeTeam/HomeTeamID",
                       ht_xml.HTXml.ht_int),
                      ("home_team_name", "HomeTeam/HomeTeamName",
                       ht_xml.HTXml.ht_str),

                      # Away team
                      ("away_team_id", "AwayTeam/AwayTeamID",
                       ht_xml.HTXml.ht_int),
                      ("away_team_name", "AwayTeam/AwayTeamName",
                       ht_xml.HTXml.ht_str),

                      # Arena
                      ("arena_id", "Arena/ArenaID", ht_xml.HTXml.ht_int),
                      ("arena_name", "Arena/ArenaName", ht_xml.HTXml.ht_str),

                      # Team
                      ("team_id", "Team/TeamID", ht_xml.HTXml.ht_int),
                      ("team_name", "Team/TeamName", ht_xml.HTXml.ht_str),
                      ("team_xp", "Team/ExperienceLevel", ht_xml.HTXml.ht_int),
                      ("team_play_style", "Team/StyleOfPlay",
                       ht_xml.HTXml.ht_int),
                      ]

    _DEFENDERS_ROLES = {101, 102, 103, 104, 105}
    _MIDFIELDS_ROLES = {106, 107, 108, 109, 110}
    _FORWARDS_ROLES = {111, 112, 113}

    def __init__(self, ht_id, team_id, source="hattrick", **kwargs):
        """
        Initialization of a HTMatchLineup instance

        :param ht_id: Hattrick ID of match
        :param team_id: Hattrick ID of team
        :param source: hattrick source to request
                       ('hattrick', 'youth' or 'hto')
        :type ht_id: int
        :type team_id: int
        :type source: str
        :key chpp: CHPP instance of connected user, must be a chpp.CHPP object
        """
        if not isinstance(ht_id, int):
            raise ValueError("ht_id must be an integer")
        if not isinstance(team_id, int):
            raise ValueError("team_id must be an integer")
        elif source not in ("hattrick", "youth", "htointegrated"):
            raise ValueError("source must be equal "
                             "to 'hattrick, 'youth' or 'htointegrated'")

        self._REQUEST_ARGS = dict()
        self._REQUEST_ARGS["matchID"] = str(ht_id)
        self._REQUEST_ARGS["teamID"] = str(team_id)
        self._REQUEST_ARGS["sourceSystem"] = source

        self.source = source

        super().__init__(**kwargs)

    def __repr__(self):
        return f"<HTMatchLineup object : " \
               f"{self.home_team_name} - {self.away_team_name} ({self.ht_id})>"

    @property
    def home_team(self):
        team_cls = ht_team.HTTeam if not self.is_youth else ht_team.HTYouthTeam
        return team_cls(chpp=self._chpp, ht_id=self.home_team_id)

    @property
    def away_team(self):
        team_cls = ht_team.HTTeam if not self.is_youth else ht_team.HTYouthTeam
        return team_cls(chpp=self._chpp, ht_id=self.away_team_id)

    @property
    def arena(self):
        return ht_arena.HTArena(chpp=self._chpp, ht_id=self.arena_id)

    @property
    def match(self):
        return ht_match.HTMatch(chpp=self._chpp, ht_id=self.ht_id,
                                source=self.source)

    def _base_lineup_players(self, start=False):

        lineup_key = "Lineup" if not start else "StartingLineup"

        return [ht_player.HTLineupPlayer(chpp=self._chpp,
                                         data=p_data,
                                         team_ht_id=self.team_id,
                                         is_youth=self.is_youth)
                for p_data
                in self._data.find("Team").find(lineup_key).findall("Player")]

    @property
    def lineup_players(self):
        return self._base_lineup_players(start=False)

    @property
    def starting_lineup_players(self):
        return self._base_lineup_players(start=True)

    @property
    def substitutions(self):
        return [HTSubstitution(chpp=self._chpp,
                               data=s_data,
                               )
                for s_data
                in self._data.find("Team")
                             .find("Substitutions")
                             .findall("Substitution")
                ]


class HTSubstitution(ht_model.HTModel):
    """
    Player substitution
    """

    _ht_attributes = [("team_id", "TeamID", ht_xml.HTXml.ht_int),
                      ("subject_player_id", "SubjectPlayerID",
                       ht_xml.HTXml.ht_int),
                      ("object_player_id", "ObjectPlayerID",
                       ht_xml.HTXml.ht_int),
                      ("order_type", "OrderType",
                       ht_xml.HTXml.ht_int),
                      ("new_position_id", "NewPositionId",
                       ht_xml.HTXml.ht_int),
                      ("new_position_behaviour", "NewPositionBehaviour",
                       ht_xml.HTXml.ht_int),
                      ("match_minute", "MatchMinute",
                       ht_xml.HTXml.ht_int),
                      ("match_part", "MatchPart", ht_xml.HTXml.ht_int),
                      ]

    @property
    def subject_player(self):
        return ht_player.HTPlayer(chpp=self._chpp,
                                  ht_id=self.subject_player_id,
                                  )

    @property
    def object_player(self):
        return ht_player.HTPlayer(chpp=self._chpp,
                                  ht_id=self.object_player_id,
                                  )
