from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union, Iterable, Dict

from pychpp.models.custom import CustomModel
from pychpp.models.custom.base.ht_match import HTCommonLightMatch
from pychpp.models.custom.base.ht_player import HTCommonLightPlayer
from pychpp.models.ht_field import HTProxyField, HTField
from pychpp.models.xml import match_lineup as ml


class HTMatchLineup(CustomModel, ml.RequestMatchLineup):
    """
    Hattrick Match Lineup
    """
    URL_PATH = '/Club/Matches/Match.aspx'
    URL_SUFFIX = '#tab2'

    source_system: str = HTProxyField(ml.MatchLineup)
    match: 'HTMatchLineupMatch' = HTField('.', suppl_attrs={'source_system': 'source_system'})
    arena: 'HTMatchLineupArena' = HTProxyField(ml.MatchLineup)
    home_team: 'HTMatchLineupTeam' = HTProxyField(ml.MatchLineup)
    away_team: 'HTMatchLineupTeam' = HTProxyField(ml.MatchLineup)

    _match_id: int = HTProxyField(ml.MatchLineup, 'match_id')
    team_lineup: 'HTMatchLineupTeamLineup' = HTProxyField(
        ml.MatchLineup, 'team', suppl_attrs={'_match_id': '_match_id',
                                             'source_system': 'source_system',
                                             }
    )


class HTMatchLineupMatch(HTCommonLightMatch):
    """
    Hattrick Match Lineup -> Match
    """
    id: int = HTProxyField(ml.MatchLineup, 'match_id')
    type: int = HTProxyField(ml.MatchLineup, 'match_type')
    context_id: Optional[int] = HTProxyField(ml.MatchLineup, 'match_context_id')
    home_team_name: str = HTProxyField(ml.MatchLineup, 'home_team.name')
    away_team_name: str = HTProxyField(ml.MatchLineup, 'away_team.name')


class HTMatchLineupTeam(CustomModel, ml.Team):
    """
    Hattrick Match Lineup -> Home/Away Team
    """
    def details(self, **kwargs):
        return self._chpp.team(id_=self.id, **kwargs)


class HTMatchLineupArena(CustomModel, ml.Arena):
    """
    Hattrick Match Lineup -> Arena
    """
    def details(self, **kwargs):
        return self._chpp.arena(id_=self.id, **kwargs)


class HTMatchLineupTeamLineup(CustomModel):
    """
    Hattrick Match Lineup -> Team lineup
    """
    source_system: str

    id: int = HTProxyField(ml.TeamLineup)
    name: str = HTProxyField(ml.TeamLineup)
    experience_level: int = HTProxyField(ml.TeamLineup)
    style_of_play: int = HTProxyField(ml.TeamLineup)
    starting_lineup_players: List['HTMLStartingLineupPlayersItem'] = HTProxyField(
        ml.TeamLineup, 'starting_lineup', suppl_attrs={'source_system': 'source_system'},
    )
    substitutions: List['HTMLSubstitutionItem'] = HTProxyField(ml.TeamLineup)
    ending_lineup_players: List['HTMLEndingLineupPlayersItem'] = HTProxyField(
        ml.TeamLineup, 'lineup', suppl_attrs={'source_system': 'source_system'},
    )

    def __init__(self, **kwargs):
        self._starting_lineup: Optional[dict] = None
        self._ending_lineup: Optional[dict] = None
        self._starting_formation: Optional[str] = None
        self._ending_formation: Optional[str] = None
        self._formations: Optional[List[tuple]] = None
        self._match_id: Optional[int] = None
        super().__init__(**kwargs)

    def _base_lineup(self, start: bool):

        lineup_players = (self.starting_lineup_players if start
                          else self.ending_lineup_players)

        lineup: Dict[str,
                     Dict[int,
                          Optional[Union['HTMLStartingLineupPlayersItem',
                                         'HTMLEndingLineupPlayersItem',
                                         'GhostPlayer',
                                         ]]]]
        lineup = {a.name: {v: None for v in a.value} for a in LineupGlobalRoles}

        for p in lineup_players:
            lineup[LineupGlobalRoles.position_from_role_id(p.role_id)][p.role_id] = p

        return lineup

    def _base_formation(self, start: bool):
        lineup = self.starting_lineup if start else self.ending_lineup
        return LineupGlobalRoles.formation_from_lineup(lineup)

    @staticmethod
    def _player_from_lineup(
            id_: int,
            lineup: Dict[str, Dict[int, 'HTMLLineupPlayersItem']],
            included_positions: Optional[Iterable] = None):

        if included_positions is not None:
            new_lineup = dict()
            for p in included_positions:
                new_lineup[p] = lineup[p]
            lineup = new_lineup

        player_list = [p for d in lineup.values()
                       for p in d.values()
                       if p is not None and p.id == id_]

        if len(player_list):
            return player_list[0]

        else:
            return GhostPlayer(id=id_)

    @property
    def starting_lineup(self):
        if self._starting_lineup is None:
            self._starting_lineup = self._base_lineup(start=True)
        return self._starting_lineup

    @property
    def ending_lineup(self):
        if self._ending_lineup is None:
            self._ending_lineup = self._base_lineup(start=False)
        return self._ending_lineup

    @property
    def starting_formation(self):
        if self._starting_formation is None:
            self._starting_formation = self._base_formation(start=True)
        return self._starting_formation

    @property
    def ending_formation(self):
        if self._ending_formation is None:
            self._ending_formation = self._base_formation(start=False)
        return self._ending_formation

    @property
    def formations(self):

        if self._formations is None:
            lineup = deepcopy(self.starting_lineup)
            end_lineup = self.ending_lineup
            formations = [(0, LineupGlobalRoles.formation_from_lineup(lineup)), ]

            match = self._chpp.match(id_=self._match_id, events=True)

            events_list = [
                evt for evt in match.events
                if (evt.type_id in (LineupEventCodes.RED_CARD.value
                                    | LineupEventCodes.NO_REPLACED.value
                                    | LineupEventCodes.SUBSTITUTION.value)
                    and evt.subject_team_id == self.id)]

            changes_list = deepcopy(self.substitutions)

            for i, evt in enumerate(events_list):
                if evt.type_id in LineupEventCodes.RED_CARD.value:
                    changes_list.insert(i, evt)

            # update lineup copy at each substitution
            for change in changes_list:

                # if change is not a substitution, it is a red card
                # remove the corresponding player from lineup
                if not isinstance(change, HTMLSubstitutionItem):
                    player_1 = self._player_from_lineup(
                        id_=change.subject_player_id,
                        lineup=lineup,
                    )
                    pos_1_id = player_1.role_id
                    lineup[LineupGlobalRoles.position_from_role_id(pos_1_id)][pos_1_id] = None

                # if replacement or order change
                # remove old player from old position
                # and add new player to new position
                elif change.order_type == 1:

                    # get player_1 from current lineup
                    player_1 = self._player_from_lineup(
                        id_=change.subject_player_id,
                        lineup=lineup,
                    )

                    # get player_2 from end lineup (because substitute players
                    # are not available in starting lineup
                    # player_2 is None if no player replace player_1
                    player_2 = self._player_from_lineup(
                        id_=change.object_player_id,
                        lineup=end_lineup,
                    ) if change.object_player_id != 0 else None

                    # remove player_1 from lineup
                    pos_1_id = player_1.role_id
                    lineup[LineupGlobalRoles.position_from_role_id(pos_1_id)][pos_1_id] = None

                    # if player_2 exists in ending lineup
                    # update lineup and player_2 role_id
                    if player_2 is not None:

                        # if player_2 is found is current lineup
                        # (case when field player replaces goalkeeper)
                        # remove it from its current position before affecting it
                        if not isinstance(
                                self._player_from_lineup(
                                    id_=player_2.id,
                                    lineup=lineup,
                                    included_positions=[LineupGlobalRoles.DEFENDER.name,
                                                        LineupGlobalRoles.MIDFIELD.name,
                                                        LineupGlobalRoles.FORWARD.name,
                                                        ]
                                ),
                                GhostPlayer):
                            lineup[LineupGlobalRoles.position_from_role_id(
                                player_2.role_id)][player_2.role_id] = None

                        pos_2_id = change.new_position_id
                        player_2.role_id = pos_2_id
                        lineup[
                            LineupGlobalRoles.position_from_role_id(pos_2_id)
                        ][pos_2_id] = player_2

                # if position swap, swap players in lineup
                # and swap players role_id
                elif change.order_type == 3:

                    # get player_1 from current lineup
                    player_1 = self._player_from_lineup(
                        id_=change.subject_player_id,
                        lineup=lineup,
                    )
                    pos_1_id = player_1.role_id

                    # get player_2 from current lineup too
                    # (because player_2 is already in lineup as it is swap)
                    player_2 = self._player_from_lineup(
                        id_=change.object_player_id,
                        lineup=lineup,
                    ) if change.object_player_id != 0 else None
                    pos_2_id = player_2.role_id

                    (
                        lineup[LineupGlobalRoles.position_from_role_id(pos_1_id)][pos_1_id],
                        player_1.role_id,
                        lineup[LineupGlobalRoles.position_from_role_id(pos_2_id)][pos_2_id],
                        player_2.role_id,
                    ) = (
                        lineup[LineupGlobalRoles.position_from_role_id(pos_2_id)][pos_2_id],
                        player_2.role_id,
                        lineup[LineupGlobalRoles.position_from_role_id(pos_1_id)][pos_1_id],
                        player_1.role_id,
                    )

                # calculate formation according to new lineup
                new_formation = LineupGlobalRoles.formation_from_lineup(lineup)

                # add entry in formations list if formation change is detected
                if new_formation != formations[-1][1]:
                    formations.append((
                        (change.minute
                         if isinstance(change, HTMLSubstitutionItem)
                         else change.minute),
                        new_formation,
                    )
                    )

            self._formations = formations

        return self._formations


class HTMLLineupPlayersItem(HTCommonLightPlayer):
    """
    Hattrick Match Lineup -> Team lineup -> Starting/Ending lineup -> Player item
    """
    role_id: int
    source_system: str

    @property
    def is_youth(self):
        return self.source_system == 'Youth'

    @property
    def role_name(self):
        return LineupRoles(self.role_id).name


class HTMLStartingLineupPlayersItem(HTMLLineupPlayersItem, ml.TeamStartingLineupPlayerItem):
    """
    Hattrick Match Lineup -> Team lineup -> Starting lineup -> Player item
    """


class HTMLSubstitutionItem(CustomModel, ml.TeamSubstitutionItem):
    """
    Hattrick Match Lineup -> Team lineup -> Substitutions -> Substitution item
    """


class HTMLEndingLineupPlayersItem(HTMLLineupPlayersItem, ml.TeamStartingLineupPlayerItem):
    """
    Hattrick Match Lineup -> Team lineup -> Ending lineup -> -> Player item
    """


@dataclass
class GhostPlayer:
    id: int


class LineupRoles(Enum):
    SET_PIECES_TAKER = 17
    CAPTAIN = 18
    REPLACED_PLAYER_1 = 19
    REPLACED_PLAYER_2 = 20
    REPLACED_PLAYER_3 = 21
    PENALTY_TAKER_1 = 22
    PENALTY_TAKER_2 = 23
    PENALTY_TAKER_3 = 24
    PENALTY_TAKER_4 = 25
    PENALTY_TAKER_5 = 26
    PENALTY_TAKER_6 = 27
    PENALTY_TAKER_7 = 28
    PENALTY_TAKER_8 = 29
    PENALTY_TAKER_9 = 30
    PENALTY_TAKER_10 = 31
    PENALTY_TAKER_11 = 32
    RED_CARDED_PLAYER_1 = 33
    RED_CARDED_PLAYER_2 = 34
    RED_CARDED_PLAYER_3 = 35
    KEEPER = 100
    RIGHT_BACK_DEFENDER = 101
    RIGHT_CENTRAL_DEFENDER = 102
    MIDDLE_CENTRAL_DEFENDER = 103
    LEFT_CENTRAL_DEFENDER = 104
    LEFT_BACK_DEFENDER = 105
    RIGHT_WINGER = 106
    RIGHT_INNER_MIDFIELD = 107
    MIDDLE_INNER_MIDFIELD = 108
    LEFT_INNER_MIDFIELD = 109
    LEFT_WINGER = 110
    RIGHT_FORWARD = 111
    MIDDLE_FORWARD = 112
    LEFT_FORWARD = 113
    SUBSTITUTION_KEEPER = 114
    SUBSTITUTION_DEFENDER = 115
    SUBSTITUTION_INNER_MIDFIELD = 116
    SUBSTITUTION_WINGER = 117
    SUBSTITUTION_FORWARD = 118
    SUBSTITUTION_WING_BACK = 119
    SUBSTITUTION_EXTRA = 120
    SUBSTITUTION_KEEPER_2 = 200
    SUBSTITUTION_DEFENDER_2 = 201
    SUBSTITUTION_WING_BACK_2 = 202
    SUBSTITUTION_INNER_MIDFIELD_2 = 203
    SUBSTITUTION_FORWARD_2 = 204
    SUBSTITUTION_WINGER_2 = 205
    SUBSTITUTION_EXTRA_2 = 206
    BACKUP_KEEPER = 207
    BACKUP_CENTRAL_DEFENDER = 208
    BACKUP_WING_BACK = 209
    BACKUP_INNER_MIDFIELD = 210
    BACKUP_FORWARD = 211
    BACKUP_WINGER = 212
    BACKUP_EXTRA = 213


class LineupGlobalRoles(Enum):

    KEEPER = {LineupRoles.KEEPER.value}

    DEFENDER = {i.value for i in (LineupRoles.RIGHT_BACK_DEFENDER,
                                  LineupRoles.RIGHT_CENTRAL_DEFENDER,
                                  LineupRoles.MIDDLE_CENTRAL_DEFENDER,
                                  LineupRoles.LEFT_CENTRAL_DEFENDER,
                                  LineupRoles.LEFT_BACK_DEFENDER,
                                  )}

    MIDFIELD = {i.value for i in (LineupRoles.RIGHT_WINGER,
                                  LineupRoles.RIGHT_INNER_MIDFIELD,
                                  LineupRoles.MIDDLE_INNER_MIDFIELD,
                                  LineupRoles.LEFT_INNER_MIDFIELD,
                                  LineupRoles.LEFT_WINGER,
                                  )}

    FORWARD = {i.value for i in (LineupRoles.RIGHT_FORWARD,
                                 LineupRoles.MIDDLE_FORWARD,
                                 LineupRoles.LEFT_FORWARD,
                                 )}

    SUBSTITUTE = {i.value for i in (LineupRoles.SUBSTITUTION_KEEPER,
                                    LineupRoles.SUBSTITUTION_DEFENDER,
                                    LineupRoles.SUBSTITUTION_INNER_MIDFIELD,
                                    LineupRoles.SUBSTITUTION_WINGER,
                                    LineupRoles.SUBSTITUTION_FORWARD,
                                    LineupRoles.SUBSTITUTION_WING_BACK,
                                    LineupRoles.SUBSTITUTION_EXTRA,
                                    LineupRoles.SUBSTITUTION_KEEPER_2,
                                    LineupRoles.SUBSTITUTION_DEFENDER_2,
                                    LineupRoles.SUBSTITUTION_INNER_MIDFIELD_2,
                                    LineupRoles.SUBSTITUTION_WINGER_2,
                                    LineupRoles.SUBSTITUTION_FORWARD_2,
                                    LineupRoles.SUBSTITUTION_WING_BACK_2,
                                    LineupRoles.SUBSTITUTION_EXTRA_2,
                                    )}

    BACKUP = {i.value for i in (LineupRoles.BACKUP_KEEPER,
                                LineupRoles.BACKUP_CENTRAL_DEFENDER,
                                LineupRoles.BACKUP_INNER_MIDFIELD,
                                LineupRoles.BACKUP_WINGER,
                                LineupRoles.BACKUP_WINGER,
                                LineupRoles.BACKUP_WING_BACK,
                                LineupRoles.BACKUP_EXTRA,
                                )}

    SET_PIECES_TAKER = {LineupRoles.SET_PIECES_TAKER.value}

    CAPTAIN = {LineupRoles.CAPTAIN.value}

    REPLACED = {i.value for i in (LineupRoles.REPLACED_PLAYER_1,
                                  LineupRoles.REPLACED_PLAYER_2,
                                  LineupRoles.REPLACED_PLAYER_3,
                                  )}

    PENALTY_TAKER = {i.value for i in (LineupRoles.PENALTY_TAKER_1,
                                       LineupRoles.PENALTY_TAKER_2,
                                       LineupRoles.PENALTY_TAKER_3,
                                       LineupRoles.PENALTY_TAKER_4,
                                       LineupRoles.PENALTY_TAKER_5,
                                       LineupRoles.PENALTY_TAKER_6,
                                       LineupRoles.PENALTY_TAKER_7,
                                       LineupRoles.PENALTY_TAKER_8,
                                       LineupRoles.PENALTY_TAKER_9,
                                       LineupRoles.PENALTY_TAKER_10,
                                       LineupRoles.PENALTY_TAKER_11,
                                       )}

    RED_CARDED_PLAYER = {i.value for i in (LineupRoles.RED_CARDED_PLAYER_1,
                                           LineupRoles.RED_CARDED_PLAYER_2,
                                           LineupRoles.RED_CARDED_PLAYER_3,
                                           )}

    @classmethod
    def position_from_role_id(cls, role_id: int):

        for role in cls:
            if role_id in role.value:
                return role.name

        raise ValueError(f"role_id '{role_id}' not found in possible lineup roles")

    @classmethod
    def formation_from_lineup(cls, lineup):
        return (
            f"{len([i for i in lineup[cls.DEFENDER.name].values() if i is not None])}"
            f"{len([i for i in lineup[cls.MIDFIELD.name].values() if i is not None])}"
            f"{len([i for i in lineup[cls.FORWARD.name].values() if i is not None])}"
        )


class LineupEventCodes(Enum):
    RED_CARD = {512, 513, 514}
    NO_REPLACED = {93, 96, 97, 425, 426}
    SUBSTITUTION = {91, 92, 95,
                    350, 351, 352, 360, 361, 362, 370, 371, 372,
                    424,
                    }
