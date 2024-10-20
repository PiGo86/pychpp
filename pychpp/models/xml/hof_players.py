from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestHallOfFamePlayers(HTModel):
    """
    Hall of Fame Players - Request arguments
    """
    SOURCE_FILE = 'hofplayers'
    LAST_VERSION = '1.2'

    _r_team_id: Optional[int] = HTInitVar('teamID', init_arg='team_id')


class HallOfFamePlayers(RequestHallOfFamePlayers):
    """
    Hall of Fame Players
    """
    players: Optional[List['PlayerItem']] = HTField('PlayerList', items='Player')


class PlayerItem(HTModel):
    """
    Hall of Fame Players -> Players -> Player item
    """
    id: int = HTField('PlayerId')
    first_name: str = HTField('FirstName')
    nick_name: Optional[str] = HTField('NickName')
    last_name: str = HTField('LastName')
    age: int = HTField('Age')
    next_birthday: datetime = HTField('NextBirthday')
    country_id: int = HTField('CountryID')
    arrival_date: datetime = HTField('ArrivalDate')
    expert_type: int = HTField('ExpertType')
    hof_date: datetime = HTField('HofDate')
    hof_age: int = HTField('HofAge')
