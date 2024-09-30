from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestLeagueDetails(HTModel):
    """
    League Details - Request arguments
    """
    SOURCE_FILE = 'leaguedetails'
    LAST_VERSION = '1.6'

    _r_league_level_unit_id: Optional[int] = HTInitVar('leagueLevelUnitID',
                                                       init_arg='league_level_unit_id',
                                                       fill_with='league_level_unit_id',
                                                       )


class LeagueDetails(RequestLeagueDetails):
    """
    League Details
    """
    league: 'League' = HTField('.')
    league_level_unit_id: int = HTField('LeagueLevelUnitID')
    league_level_unit_name: str = HTField('LeagueLevelUnitName')
    current_match_round: int = HTField('CurrentMatchRound')
    rank: int = HTField('Rank')
    teams: List['TeamItem'] = HTField('.', items='Team')


class League(HTModel):
    """
    League Details -> League
    """
    id: int = HTField('LeagueID')
    name: str = HTField('LeagueName')
    level: int = HTField('LeagueLevel')
    max_level: int = HTField('MaxLevel')


class TeamItem(HTModel):
    """
    League Details -> Team item
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    user_id: int = HTField('UserId')
    position: int = HTField('Position')
    position_change: int = HTField('PositionChange')
    matches: int = HTField('Matches')
    goals_for: int = HTField('GoalsFor')
    goals_against: int = HTField('GoalsAgainst')
    points: int = HTField('Points')
    won: int = HTField('Won')
    draws: int = HTField('Draws')
    lost: int = HTField('Lost')
