from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestYouthLeagueDetails(HTModel):
    """
    Youth League Details - Request arguments
    """
    SOURCE_FILE = 'youthleaguedetails'
    LAST_VERSION = '1.0'

    _r_youth_league_id: Optional[int] = HTInitVar('youthLeagueId', init_arg='youth_league_id')


class YouthLeagueDetails(RequestYouthLeagueDetails):
    """
    Youth League Details
    """
    id: int = HTField('YouthLeagueID')
    name: str = HTField('YouthLeagueName')
    type: int = HTField('YouthLeagueType')
    season: int = HTField('Season')
    last_match_round: int = HTField('LastMatchRound')
    nr_of_teams_in_league: int = HTField('NrOfTeamsInLeague')
    teams: List['TeamItem'] = HTField('Teams', items='Team')


class TeamItem(HTModel):
    """
    Youth League Details -> Teams -> Team item
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
