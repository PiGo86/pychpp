from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestStaffList(HTModel):
    """
    Staff List - Request arguments
    """
    SOURCE_FILE = 'stafflist'
    LAST_VERSION = '1.2'

    _r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')


class StaffList(RequestStaffList):
    """
    Staff List
    """
    XML_PREFIX = 'StaffList/'

    trainer: 'Trainer' = HTField('Trainer')
    staff_members: List['StaffMemberItem'] = HTField('StaffMembers', items='Staff')
    total_staff_members: int = HTField('TotalStaffMembers')
    total_cost: int = HTField('TotalCost')


class Trainer(HTModel):
    """
    Staff List -> Trainer
    """
    id: int = HTField('TrainerId')
    name: str = HTField('Name')
    age: int = HTField('Age')
    age_days: int = HTField('AgeDays')
    contract_date: datetime = HTField('ContractDate')
    cost: int = HTField('Cost')
    country_id: int = HTField('CountryID')
    type: int = HTField('TrainerType')
    leadership: int = HTField('Leadership')
    skill_level: int = HTField('TrainerSkillLevel')
    status: int = HTField('TrainerStatus')


class StaffMemberItem(HTModel):
    """
    Staff List -> Staff members -> Staff member item
    """
    id: int = HTField('StaffId')
    name: str = HTField('Name')
    type: int = HTField('StaffType')
    level: int = HTField('StaffLevel')
    hired_date: datetime = HTField('HiredDate')
    cost: int = HTField('Cost')
    hof_player_id: int = HTField('HofPlayerId')
