from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestStaffAvatars(HTModel):
    """
    Staff Avatars - Request arguments
    """
    SOURCE_FILE = 'staffavatars'
    LAST_VERSION = '1.1'

    _r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')


class StaffAvatars(RequestStaffAvatars):
    """
    Staff Avatars
    """
    trainer: 'Trainer' = HTField('Trainer')
    staff_members: List['StaffMemberItem'] = HTField('StaffMembers', items='Staff')


class CommonTrainerStaffMemberItem(HTModel):
    """
    Staff Avatars -> Trainer / Staff member item
    """
    avatar: 'Avatar' = HTField('Avatar')


class Avatar(HTModel):
    """
    Staff Avatars -> Trainer / Staff member item -> Avatar
    """
    background_image: str = HTField('BackgroundImage')
    layers: List['LayerItem'] = HTField('.', items='Layer')


class LayerItem(HTModel):
    """
    Staff Avatars -> Trainer / Staff member item -> Avatar -> Layer
    """
    x: int = HTField('.', attrib='x')
    y: int = HTField('.', attrib='y')
    image: str = HTField('Image')


class Trainer(CommonTrainerStaffMemberItem):
    """
    Staff Avatars -> Trainer
    """
    id: int = HTField('TrainerId')


class StaffMemberItem(CommonTrainerStaffMemberItem):
    """
    Staff Avatars -> Staff members -> Staff member item
    """
    id: int = HTField('StaffId')
