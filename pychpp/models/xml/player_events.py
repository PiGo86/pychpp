from datetime import datetime
from typing import List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestPlayerEvents(HTModel):
    """
    Player Events - Request arguments
    """
    SOURCE_FILE = 'playerevents'
    LAST_VERSION = '1.3'

    _r_player_id: int = HTInitVar('playerID', init_arg='player_id')


class PlayerEvents(RequestPlayerEvents):
    """
    Player Events
    """
    user_supporter_tier: str = HTField('UserSupporterTier')
    player: 'Player' = HTField('Player')


class Player(HTModel):
    """
    Player Events -> Player
    """
    id: int = HTField('PlayerID')
    events: List['EventItem'] = HTField('PlayerEvents', items='PlayerEvent')


class EventItem(HTModel):
    """
    Player Events -> Player -> Events -> Event item
    """
    date: datetime = HTField('EventDate')
    type_id: int = HTField('PlayerEventTypeID')
    text: str = HTField('EventText')
