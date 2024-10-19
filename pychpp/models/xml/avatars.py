from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestAvatars(HTModel):
    """
    Avatars - Request arguments
    """
    SOURCE_FILE = 'avatars'
    LAST_VERSION = '1.1'

    _r_action_type: Optional[str] = HTInitVar('actionType', init_arg='action_type')
    _r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')


class Avatars(RequestAvatars):
    """
    Avatars
    """
    team: 'Team' = HTField('Team')


class Team(HTModel):
    """
    Avatars -> Team
    """
    id: int = HTField('TeamId')
    players: List['PlayerItem'] = HTField('Players', items='Player')


class PlayerItem(HTModel):
    """
    Avatars -> Team -> Players -> Player item
    """
    id: int = HTField('PlayerID')
    avatar: 'Avatar' = HTField('Avatar')


class Avatar(HTModel):
    """
    Avatars -> Team -> Players -> Player item -> Avatar
    """
    background_image: str = HTField('BackgroundImage')
    layers: List['LayerItem'] = HTField('.', items='Layer')


class LayerItem(HTModel):
    """
    Avatars -> Team -> Players -> Player item -> Avatar -> Layer
    """
    x: int = HTField('.', attrib='x')
    y: int = HTField('.', attrib='y')
    image: str = HTField('Image')
