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

        super().__init__(**kwargs)

    def __repr__(self):
        return f"<HTMatchLineup object : " \
               f"{self.home_team_name} - {self.away_team_name} ({self.ht_id})>"

    @property
    def home_team(self):
        return ht_team.HTTeam(chpp=self._chpp, ht_id=self.home_team_id)

    @property
    def away_team(self):
        return ht_team.HTTeam(chpp=self._chpp, ht_id=self.away_team_id)

    @property
    def arena(self):
        return ht_arena.HTArena(chpp=self._chpp, ht_id=self.arena_id)

    @property
    def match(self):
        return ht_match.HTMatch(chpp=self._chpp, ht_id=self.ht_id)

    @property
    def lineup_players(self):
        return [ht_player.HTLineupPlayer(chpp=self._chpp,
                                         data=p_data,
                                         team_ht_id=self.team_id,
                                         is_youth=self.is_youth)
                for p_data
                in self._data.find("Team").find("Lineup").findall("Player")]
