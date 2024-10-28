from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestYouthAvatars(HTModel):
    """
    Youth Avatars - Request arguments
    """
    SOURCE_FILE = 'youthavatars'
    LAST_VERSION = '1.2'

    _r_youth_team_id: Optional[int] = HTInitVar('youthTeamId', init_arg='youth_team_id')


class YouthAvatars(RequestYouthAvatars):
    """
    Youth Avatars
    """
    XML_PREFIX = 'YouthTeam/'

    youth_team_id: int = HTField('YouthTeamId')
    youth_players: List['YouthPlayerItem'] = HTField('YouthPlayers', items='YouthPlayer')


class YouthPlayerItem(HTModel):
    """
    Youth Avatars -> Youth Players -> Youth player item
    """
    id: int = HTField('YouthPlayerID')
    avatar: 'Avatar' = HTField('Avatar')


class Avatar(HTModel):
    """
    Youth Avatars -> Youth Players -> Youth player item -> Avatar
    """
    background_image: str = HTField('BackgroundImage')
    layers: List['LayerItem'] = HTField('.', items='Layer')


class LayerItem(HTModel):
    """
    Youth Avatars -> Youth Players -> Youth player item -> Avatar -> Layer
    """
    x: int = HTField('.', attrib='x')
    y: int = HTField('.', attrib='y')
    image: str = HTField('Image')
