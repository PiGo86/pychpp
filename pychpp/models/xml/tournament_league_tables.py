from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestTournamentLeagueTables(HTModel):
    """
    Tournament League Tables - Request arguments
    """
    SOURCE_FILE = 'tournamentleaguetables'
    LAST_VERSION = '1.1'

    _r_tournament_id: int = HTInitVar('tournamentId', init_arg='tournament_id')
    _r_season: Optional[int] = HTInitVar('season', init_arg='season')
    _r_world_cup_round: Optional[int] = HTInitVar('worldCupRound', init_arg='world_cup_round')


class TournamentLeagueTables(RequestTournamentLeagueTables):
    """
    Tournament League Tables
    """
    id: int = HTField('TournamentId')
    season: int = HTField('Season')
    world_cup_round: Optional[int] = HTField('WorldCupRound')
    tournament_league_tables: List['TableItem'] = HTField('TournamentLeagueTables',
                                                          items='TournamentLeagueTable')


class TableItem(HTModel):
    """
    Tournament League Tables -> Tournament League Tables -> Tournament League Table item
    """
    group_id: int = HTField('GroupId')
    teams: List['TeamItem'] = HTField('Teams', items='Team')


class TeamItem(HTModel):
    """
    Tournament League Tables -> Tournament League Tables -> Tournament League Table item
    -> Teams -> Team item
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    position: int = HTField('Position')
    position_change: int = HTField('PositionChange')
    matches: int = HTField('Matches')
    goals_for: int = HTField('GoalsFor')
    goals_against: int = HTField('GoalsAgainst')
    points: int = HTField('Points')
    won: int = HTField('Won')
    draws: int = HTField('Draws')
    lost: int = HTField('Lost')
