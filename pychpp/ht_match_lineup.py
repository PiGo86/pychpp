from pychpp import ht_model
from pychpp import ht_arena, ht_match, ht_player, ht_team, ht_xml

from copy import deepcopy


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

    _KEEPER_ROLE = {100, }
    _DEFENDERS_ROLES = {101, 102, 103, 104, 105, }
    _MIDFIELDS_ROLES = {106, 107, 108, 109, 110, }
    _FORWARDS_ROLES = {111, 112, 113, }
    _SUBSTITUTES_ROLES = {114, 115, 116, 117, 118, 119, 120,
                          200, 201, 202, 203, 204, 205, 206, }
    _BACKUPS_ROLES = {207, 208, 209, 210, 211, 212, 213, }
    _SET_PIECES_ROLES = {17, }
    _CAPTAIN_ROLE = {18, }
    _REPLACED_ROLES = {19, 20, 21, }
    _PENALTY_TAKERS_ROLES = {22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, }

    def __init__(self, ht_id, team_id=None, source="hattrick", **kwargs):
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
        if team_id is not None and not isinstance(team_id, int):
            raise ValueError("team_id must be an integer")
        elif source not in ("hattrick", "youth", "htointegrated"):
            raise ValueError("source must be equal "
                             "to 'hattrick, 'youth' or 'htointegrated'")

        self._REQUEST_ARGS = dict()
        self._REQUEST_ARGS["matchID"] = str(ht_id)
        self._REQUEST_ARGS["teamID"] = (str(team_id)
                                        if team_id is not None else "")
        self._REQUEST_ARGS["sourceSystem"] = source

        self.source = source

        super().__init__(**kwargs)

        self.substitutions = [HTSubstitution(chpp=self._chpp, data=s_data)
                              for s_data in self._data.find("Team")
                                                .find("Substitutions")
                                                .findall("Substitution")
                              ]

    def __repr__(self):
        return f"<HTMatchLineup object : " \
               f"{'<' if self.team_id == self.home_team_id else ''}" \
               f"{self.home_team_name}" \
               f"{'>' if self.team_id == self.home_team_id else ''}" \
               f" - " \
               f"{'<' if self.team_id == self.away_team_id else ''}" \
               f"{self.away_team_name}" \
               f"{'>' if self.team_id == self.away_team_id else ''}" \
               f" ({self.ht_id})>"

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

    @property
    def starting_lineup_players(self):
        return self._base_lineup_players(start=True)

    @property
    def lineup_players(self):
        return self._base_lineup_players(start=False)

    @property
    def starting_lineup(self):
        return self._base_lineup(start=True)

    @property
    def lineup(self):
        return self._base_lineup(start=False)

    @property
    def starting_formation(self):
        return self._base_formation(start=True)

    @property
    def formation(self):
        return self._base_formation(start=False)

    @property
    def formations(self):

        lineup = deepcopy(self.starting_lineup)
        end_lineup = self.lineup
        formations = [(0, self._formation_from_lineup(lineup)), ]

        # update lineup copy at each substitution
        for s in self.substitutions:

            player_1 = None
            player_2 = None

            # if replacement of order change
            # remove old player from old position
            # and add new player to new position
            if s.order_type == 1:

                # get player_1 from current lineup
                player_1 = self._player_from_lineup(
                    ht_id=s.subject_player_id,
                    lineup=lineup,
                )

                # get player_2 from end lineup (because substitute players
                # are not available in starting lineup
                # player_2 is None if no player replace player_1
                player_2 = self._player_from_lineup(
                    ht_id=s.object_player_id,
                    lineup=end_lineup,
                ) if s.object_player_id != 0 else None

                # remove player_1 from lineup
                pos_1_id = player_1.role_id
                lineup[self.position(pos_1_id)][pos_1_id] = None

                # if player_2 exists
                # update lineup and player_2 role_id
                if player_2 is not None:
                    pos_2_id = s.new_position_id
                    player_2.role_id = pos_2_id
                    lineup[self.position(pos_2_id)][pos_2_id] = player_2

            # if position swap, swap players in lineup
            # and swap players role_id
            elif s.order_type == 3:

                # get player_1 from current lineup
                player_1 = self._player_from_lineup(
                    ht_id=s.subject_player_id,
                    lineup=lineup,
                )
                pos_1_id = player_1.role_id

                # get player_2 from current lineup too
                # (because player_2 is already in lineup as it is swap)
                player_2 = self._player_from_lineup(
                    ht_id=s.object_player_id,
                    lineup=lineup,
                ) if s.object_player_id != 0 else None
                pos_2_id = player_2.role_id

                (
                    lineup[self.position(pos_1_id)][pos_1_id],
                    player_1.role_id,
                    lineup[self.position(pos_2_id)][pos_2_id],
                    player_2.role_id,
                ) = (
                    lineup[self.position(pos_2_id)][pos_2_id],
                    player_2.role_id,
                    lineup[self.position(pos_1_id)][pos_1_id],
                    player_1.role_id,
                )

            # calculate formation according to new lineup
            new_formation = self._formation_from_lineup(lineup)

            # add entry in formations list if formation change is detected
            if new_formation != formations[-1][1]:
                formations.append((s.match_minute, new_formation))

        return formations

    def position(self, role_id):

        if role_id in self._KEEPER_ROLE:
            pos = "keeper"
        elif role_id in self._DEFENDERS_ROLES:
            pos = "defender"
        elif role_id in self._MIDFIELDS_ROLES:
            pos = "midfield"
        elif role_id in self._FORWARDS_ROLES:
            pos = "forward"
        elif role_id in self._SUBSTITUTES_ROLES:
            pos = "substitute"
        elif role_id in self._BACKUPS_ROLES:
            pos = "backup"
        elif role_id in self._SET_PIECES_ROLES:
            pos = "set pieces"
        elif role_id in self._CAPTAIN_ROLE:
            pos = "captain"
        elif role_id in self._REPLACED_ROLES:
            pos = "replaced"
        elif role_id in self._PENALTY_TAKERS_ROLES:
            pos = "penalty taker"
        else:
            raise ValueError(f"unknown role id {role_id}")

        return pos

    @staticmethod
    def _formation_from_lineup(lineup):
        return (
            f"{len([i for i in lineup['defender'].values() if i is not None])}"
            f"{len([i for i in lineup['midfield'].values() if i is not None])}"
            f"{len([i for i in lineup['forward'].values() if i is not None])}"
        )

    def _base_lineup_players(self, start=False):

        lineup_key = "Lineup" if not start else "StartingLineup"

        return [ht_player.HTLineupPlayer(chpp=self._chpp,
                                         data=p_data,
                                         team_ht_id=self.team_id,
                                         is_youth=self.is_youth)
                for p_data
                in self._data.find("Team").find(lineup_key).findall("Player")]

    def _base_formation(self, start):
        lineup = self.starting_lineup if start else self.lineup
        return self._formation_from_lineup(lineup)

    def _player_from_lineup(self, ht_id, lineup):
        return [p for d in lineup.values()
                for p in d.values() if getattr(p, "ht_id", None) == ht_id][0]

    def _base_lineup(self, start):

        lineup_players = (self.starting_lineup_players if start
                          else self.lineup_players)

        lineup = {"keeper": {100: None
                             },
                  "defender": {101: None, 102: None, 103: None,
                               104: None, 105: None,
                               },
                  "midfield": {106: None, 107: None, 108: None,
                               109: None, 110: None,
                               },
                  "forward": {111: None, 112: None, 113: None,
                              },
                  "substitute": {114: None, 115: None, 117: None, 118: None,
                                 119: None, 200: None, 201: None, 202: None,
                                 203: None, 204: None, 205: None, 206: None,
                                 },
                  "backup": {207: None, 208: None, 209: None, 210: None,
                             211: None, 212: None, 213: None,
                             },
                  "set pieces": {17: None,
                                 },
                  "captain": {18: None,
                              },
                  "replaced": {19: None, 20: None, 21: None,
                               },
                  "penalty taker": {22: None, 23: None, 24: None, 25: None,
                                    26: None, 27: None, 28: None, 29: None,
                                    30: None, 31: None, 32: None,
                                    },
                  }

        for p in lineup_players:
            lineup[self.position(p.role_id)][p.role_id] = p

        return lineup


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
