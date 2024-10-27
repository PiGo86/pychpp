from typing import List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestTrainingEvents(HTModel):
    """
    Training Events - Request arguments
    """
    SOURCE_FILE = 'trainingevents'
    LAST_VERSION = '1.3'

    _r_player_id: int = HTInitVar('playerID', init_arg='player_id')


class TrainingEvents(RequestTrainingEvents):
    """
    Training Events
    """
    user_supporter_tier: str = HTField('UserSupporterTier')
    player: 'Player' = HTField('Player')


class Player(HTModel):
    """
    Training Events -> Player
    """
    id: int = HTField('PlayerID')
    training_events_available: bool = HTField('TrainingEvents', attrib='Available')
    training_events: List['TrainingEventItem'] = HTField('TrainingEvents',
                                                         items='TrainingEvent')


class TrainingEventItem(HTModel):
    """
    Training Events -> Player -> Training Events -> Training event item
    """
    index: int = HTField('.', attrib='Index')
    skill_id: int = HTField('SkillID')
    old_level: int = HTField('OldLevel')
    new_level: int = HTField('NewLevel')
    season: int = HTField('Season')
    match_round: int = HTField('MatchRound')
    day_number: int = HTField('DayNumber')
