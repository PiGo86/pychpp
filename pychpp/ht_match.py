from pychpp import ht_model
from pychpp import ht_team, ht_arena, ht_xml


class HTMatch(ht_model.HTModel):
    """
    Hattrick match
    """

    _SOURCE_FILE = "matchdetails"
    _SOURCE_FILE_VERSION = "3.0"

    _URL_PATH = "/Club/Matches/Match.aspx?matchID="

    _ht_attributes = [("ht_id", "Match/MatchID", ht_xml.HTXml.ht_int),

                      # General information
                      ("type", "Match/MatchType", ht_xml.HTXml.ht_str),
                      ("context", "Match/MatchContextId", ht_xml.HTXml.ht_str),
                      ("rule", "Match/MatchRuleId", ht_xml.HTXml.ht_str),
                      ("cup_level", "Match/CupLevel", ht_xml.HTXml.ht_int),
                      ("cup_level_index", "Match/CupLevelIndex",
                       ht_xml.HTXml.ht_int),
                      ("datetime", "Match/MatchDate",
                       ht_xml.HTXml.ht_datetime_from_text),
                      ("finished_date", "Match/FinishedDate",
                       ht_xml.HTXml.ht_datetime_from_text),
                      ("added_minutes", "Match/AddedMinutes",
                       ht_xml.HTXml.ht_int),

                      # Home team
                      ("home_team_id", "Match/HomeTeam/HomeTeamID",
                       ht_xml.HTXml.ht_int),
                      ("home_team_name", "Match/HomeTeam/HomeTeamName",
                       ht_xml.HTXml.ht_str),
                      ("home_team_dress_uri", "Match/HomeTeam/DressURI",
                       ht_xml.HTXml.ht_str),
                      ("home_team_formation", "Match/HomeTeam/Formation",
                       ht_xml.HTXml.ht_str),
                      ("home_team_goals", "Match/HomeTeam/HomeGoals",
                       ht_xml.HTXml.ht_int),
                      ("home_team_tactic_type", "Match/HomeTeam/TacticType",
                       ht_xml.HTXml.ht_str),
                      ("home_team_tactic_skill", "Match/HomeTeam/TacticSkill",
                       ht_xml.HTXml.ht_int),
                      ("home_team_rating_midfield",
                       "Match/HomeTeam/RatingMidfield",
                       ht_xml.HTXml.ht_int),
                      ("home_team_rating_right_def",
                       "Match/HomeTeam/RatingRightDef",
                       ht_xml.HTXml.ht_int),
                      ("home_team_rating_mid_def",
                       "Match/HomeTeam/RatingMidDef",
                       ht_xml.HTXml.ht_int),
                      ("home_team_rating_left_def",
                       "Match/HomeTeam/RatingLeftDef",
                       ht_xml.HTXml.ht_int),
                      ("home_team_rating_right_att",
                       "Match/HomeTeam/RatingRightAtt",
                       ht_xml.HTXml.ht_int),
                      ("home_team_rating_mid_att",
                       "Match/HomeTeam/RatingMidAtt",
                       ht_xml.HTXml.ht_int),
                      ("home_team_rating_left_att",
                       "Match/HomeTeam/RatingLeftAtt",
                       ht_xml.HTXml.ht_int),
                      ("home_team_attitude",
                       "Match/HomeTeam/TeamAttitude",
                       ht_xml.HTXml.ht_int),
                      ("home_team_rating_ind_set_pieces_def",
                       "Match/HomeTeam/RatingIndirectSetPiecesDef",
                       ht_xml.HTXml.ht_int,
                       ),
                      ("home_team_rating_ind_set_pieces_att",
                       "Match/HomeTeam/RatingIndirectSetPiecesAtt",
                       ht_xml.HTXml.ht_int,
                       ),

                      # Away team
                      ("away_team_id", "Match/AwayTeam/AwayTeamID",
                       ht_xml.HTXml.ht_int),
                      ("away_team_name", "Match/AwayTeam/AwayTeamName",
                       ht_xml.HTXml.ht_str),
                      ("away_team_dress_uri", "Match/AwayTeam/DressURI",
                       ht_xml.HTXml.ht_str),
                      ("away_team_formation", "Match/AwayTeam/Formation",
                       ht_xml.HTXml.ht_str),
                      ("away_team_goals", "Match/AwayTeam/AwayGoals",
                       ht_xml.HTXml.ht_int),
                      ("away_team_tactic_type", "Match/AwayTeam/TacticType",
                       ht_xml.HTXml.ht_str),
                      ("away_team_tactic_skill", "Match/AwayTeam/TacticSkill",
                       ht_xml.HTXml.ht_int),
                      ("away_team_rating_midfield",
                       "Match/AwayTeam/RatingMidfield",
                       ht_xml.HTXml.ht_int),
                      ("away_team_rating_right_def",
                       "Match/AwayTeam/RatingRightDef",
                       ht_xml.HTXml.ht_int),
                      ("away_team_rating_mid_def",
                       "Match/AwayTeam/RatingMidDef",
                       ht_xml.HTXml.ht_int),
                      ("away_team_rating_left_def",
                       "Match/AwayTeam/RatingLeftDef",
                       ht_xml.HTXml.ht_int),
                      ("away_team_rating_right_att",
                       "Match/AwayTeam/RatingRightAtt",
                       ht_xml.HTXml.ht_int),
                      ("away_team_rating_mid_att",
                       "Match/AwayTeam/RatingMidAtt",
                       ht_xml.HTXml.ht_int),
                      ("away_team_rating_left_att",
                       "Match/AwayTeam/RatingLeftAtt",
                       ht_xml.HTXml.ht_int),
                      ("away_team_attitude",
                       "Match/AwayTeam/TeamAttitude",
                       ht_xml.HTXml.ht_int),
                      ("away_team_rating_ind_set_pieces_def",
                       "Match/AwayTeam/RatingIndirectSetPiecesDef",
                       ht_xml.HTXml.ht_int,
                       ),
                      ("away_team_rating_ind_set_pieces_att",
                       "Match/AwayTeam/RatingIndirectSetPiecesAtt",
                       ht_xml.HTXml.ht_int,
                       ),

                      # Arena
                      ("arena_id", "Match/Arena/ArenaID", ht_xml.HTXml.ht_int),
                      ("arena_name", "Match/Arena/ArenaName",
                       ht_xml.HTXml.ht_str),
                      ("weather", "Match/Arena/WeatherID",
                       ht_xml.HTXml.ht_int),
                      ("spectators", "Match/Arena/SoldTotal",
                       ht_xml.HTXml.ht_int),
                      ("spectators_terraces", "Match/Arena/SoldTerraces",
                       ht_xml.HTXml.ht_int),
                      ("spectators_basic", "Match/Arena/SoldBasic",
                       ht_xml.HTXml.ht_int),
                      ("spectators_roof", "Match/Arena/SoldRoof",
                       ht_xml.HTXml.ht_int),
                      ("spectators_vip", "Match/Arena/SoldVIP",
                       ht_xml.HTXml.ht_int),

                      # Goals
                      ("goals", "Match/Scorers", ht_xml.HTXml.ht_goals),

                      # Events
                      ("events", "Match/EventList",
                       ht_xml.HTXml.ht_match_events),
                      ]

    def __init__(self, ht_id, events=False, source="hattrick", **kwargs):
        """
        Initialization of a HTArena instance

        :param ht_id: Hattrick ID of match
        :param events: define if match events have to be requested
        :param source: hattrick source to request
        ('hattrick', 'youth' or 'hto')
        :type ht_id: int
        :type events: bool
        :type source: str
        :key chpp: CHPP instance of connected user, must be a chpp.CHPP object
        """
        if not isinstance(ht_id, int):
            raise ValueError("ht_id must be an integer")
        elif not isinstance(events, bool):
            raise ValueError("events must be a boolean")
        elif source not in ("hattrick", "youth", "htointegrated"):
            raise ValueError(
                "source must be equal to 'hattrick, 'youth' "
                "or 'htointegrated'")

        self._REQUEST_ARGS = dict()
        self._REQUEST_ARGS["matchID"] = str(ht_id)
        self._REQUEST_ARGS["matchEvents"] = (
            "true" if events is True else "false")
        self._REQUEST_ARGS["sourceSystem"] = source

        super().__init__(**kwargs)

    def __repr__(self):
        return f"<HTMatch object : " \
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
