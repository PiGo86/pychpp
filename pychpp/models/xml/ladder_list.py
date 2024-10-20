from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestLadderList(HTModel):
    """
    Ladder List - Request arguments
    """
    SOURCE_FILE = 'ladderlist'
    LAST_VERSION = '1.0'

    _r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')


class LadderList(RequestLadderList):
    """
    Ladder List
    """
    ladders: Optional[List['LadderItem']] = HTField('Ladders', items='Ladder')


class LadderItem(HTModel):
    """
    Ladder List -> Ladders -> Ladder item
    """
    id: int = HTField('LadderId')
    name: str = HTField('Name')
    position: int = HTField('Position')
    next_match_date: datetime = HTField('NextMatchDate')
    wins: int = HTField('Wins')
    lost: int = HTField('Lost')
