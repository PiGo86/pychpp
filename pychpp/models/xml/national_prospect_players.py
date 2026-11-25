"""Models for the `nationalprospectplayers.xml` CHPP file."""

from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestNationalProspectPlayers(HTModel):
    """National Prospect Players - Request arguments."""
    SOURCE_FILE = 'nationalprospectplayers'
    LAST_VERSION = '1.0'

    _r_team_id: int = HTInitVar('teamID', init_arg='team_id')
    _r_player_category_id: Optional[int] = HTInitVar('playerCategoryId',
                                                     init_arg='player_category_id')


class NationalProspectPlayers(RequestNationalProspectPlayers):
    """National Prospect Players."""
    user_supporter_tier: str = HTField('UserSupporterTier')
    team_id: int = HTField('TeamID')
    team_name: str = HTField('TeamName')
    players: Optional[List['PlayerItem']] = HTField('Players', items='Player')


class PlayerItem(HTModel):
    """National Prospect Players -> Players -> Player item."""
    id: int = HTField('PlayerID')
    name: str = HTField('PlayerName')
    category_id: int = HTField('PlayerCategoryId')
    specialty: int = HTField('Specialty')
    avatar: 'Avatar' = HTField('Avatar')


class Avatar(HTModel):
    """National Prospect Players -> Players -> Player item -> Avatar."""
    background_image: str = HTField('BackgroundImage')
    layers: List['LayerItem'] = HTField('.', items='Layer')


class LayerItem(HTModel):
    """National Prospect Players -> Players -> Player item -> Avatar -> Layer."""
    x: int = HTField('.', attrib='x')
    y: int = HTField('.', attrib='y')
    image: str = HTField('Image')
