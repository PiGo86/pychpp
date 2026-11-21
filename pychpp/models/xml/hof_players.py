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
    LAST_VERSION = '1.3'

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
    country_id: int = HTField('CountryID', version='>=1.1')
    arrival_date: datetime = HTField('ArrivalDate')
    expert_type: int = HTField('ExpertType')
    hof_date: datetime = HTField('HofDate')
    hof_age: int = HTField('HofAge')
    matches_in_club: Optional[int] = HTField('MatchesInClub', version='>=1.3')
    best_performance_value: Optional[float] = HTField('BestPerformanceValue', version='>=1.3')
    no_of_times_training_match_hero: Optional[int] = HTField('NoOfTimesTrainingMatchHero',
                                                              version='>=1.3')
    faithful_to_the_club: Optional[int] = HTField('FaithfulToTheClub', version='>=1.3')
    no_of_clean_sheet: Optional[int] = HTField('NoOfCleanSheet', version='>=1.3')
