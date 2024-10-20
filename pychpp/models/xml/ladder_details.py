from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestLadderDetails(HTModel):
    """
    Ladder Details - Request arguments
    """
    SOURCE_FILE = 'ladderdetails'
    LAST_VERSION = '1.0'

    _r_ladder_id: int = HTInitVar('ladderid', init_arg='ladder_id')
    _r_team_id: Optional[int] = HTInitVar('teamid', init_arg='team_id')
    _r_page_size: Optional[int] = HTInitVar('pagesize', init_arg='page_size')
    _r_page_index: Optional[int] = HTInitVar('pageindex', init_arg='page_index')


class LadderDetails(RequestLadderDetails):
    """
    Ladder Details
    """
    ladder: 'Ladder' = HTField('Ladder')


class Ladder(HTModel):
    """
    Ladder Details -> Ladder
    """
    id: int = HTField('LadderId')
    name: str = HTField('Name')
    num_of_teams: int = HTField('NumOfTeams')
    page_size: int = HTField('PageSize')
    page_index: int = HTField('PageIndex')
    king_team_id: int = HTField('KingTeamId')
    king_team_name: str = HTField('KingTeamName')
    king_since: datetime = HTField('KingSince')
    teams: Optional[List['Team']] = HTField('.', items='Team')


class Team(HTModel):
    """
    Ladder Details -> Ladder -> Teams -> Team item
    """
    id: int = HTField('TeamId')
    name: str = HTField('TeamName')
    position: int = HTField('Position')
    wins: int = HTField('Wins')
    lost: int = HTField('Lost')
    wins_in_a_row: int = HTField('WinsInARow')
    lost_in_a_row: int = HTField('LostInARow')
