from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestAllianceDetails(HTModel):
    """
    Alliance Details - Base request arguments
    """
    SOURCE_FILE = 'alliancedetails'
    LAST_VERSION = '1.5'

    _r_action_type: Optional[str] = HTInitVar('actionType', init_arg='action_type')
    _r_alliance_id: int = HTInitVar('allianceID', init_arg='alliance_id')
    _r_subset: Optional[int] = HTInitVar('subset', init_arg='subset')


class BaseAllianceDetails(RequestAllianceDetails):
    """
    Alliance Details
    """
    user_supporter_tier: str = HTField('UserSupporterTier')
    action_type: str = HTField('ActionType')


class AllianceDetailsView(BaseAllianceDetails):
    """
    Alliance Details - View
    """
    alliance: 'AllianceView' = HTField('Alliance')


class AllianceDetailsRoles(BaseAllianceDetails):
    """
    Alliance Details - Roles
    """
    alliance: 'AllianceRoles' = HTField('Alliance')


class BaseAlliance(HTModel):
    """
    Alliance Details -> Base Alliance
    """
    id: int = HTField('AllianceID')
    name: str = HTField('AllianceName')


class AllianceView(BaseAlliance):
    """
    Alliance Details - View -> Alliance
    """
    abbreviation: str = HTField('Abbreviation')
    description: str = HTField('Description')
    logo_url: str = HTField('LogoURL')
    top_role: str = HTField('TopRole')
    top_user_id: int = HTField('TopUserID')
    top_login_name: str = HTField('TopLoginname')
    creation_date: datetime = HTField('CreationDate')
    home_page_url: str = HTField('HomePageURL')
    number_of_members: int = HTField('NumberOfMembers')
    languages: List['AllianceLanguageItem'] = HTField('Languages', items='Language')
    message: Optional[str] = HTField('Message')
    rules: Optional[str] = HTField('Rules')
    user_role: Optional['AllianceUserRole'] = HTField('UserRole')


class AllianceLanguageItem(HTModel):
    """
    Alliance Details - View -> Alliance -> Languages -> Language item
    """
    id: int = HTField('LanguageID')
    name: str = HTField('LanguageName')


class AllianceUserRole(HTModel):
    """
    Alliance Details - View -> Alliance -> User Role
    """
    id: int = HTField('RoleId')
    name: str = HTField('RoleName')


class AllianceRoles(HTModel):
    """
    Alliance Details - Roles -> Alliance
    """
    roles: List['AllianceRoleItem'] = HTField('Roles', items='Role', xml_prefix='Role')


class AllianceRoleItem(HTModel):
    """
    Alliance Details - Roles -> Alliance -> Roles -> Role item
    """
    id: int = HTField('Id')
    name: str = HTField('Name')
    rank: int = HTField('Rank')
    member_count: int = HTField('MemberCount')
    max_members: int = HTField('MaxMembers')
    request_type: int = HTField('RequestType')
    description: str = HTField('RoleDescription')


class AllianceDetailsMembers(BaseAllianceDetails):
    """
    Alliance Details - Members
    """
    alliance: 'AllianceMembers' = HTField('Alliance')


class AllianceMembers(BaseAlliance):
    """
    Alliance Details - Members -> Alliance
    """
    members: List['AllianceMemberItem'] = HTField('Members', items='Member')


class AllianceDetailsMembersSubset(BaseAllianceDetails):
    """
    Alliance Details - Members Subset
    """
    list_subset: str = HTField('ListSubset')
    members: List['AllianceMemberItem']


class AllianceMemberItem(HTModel):
    """
    Alliance Details - Members/Members Subset -> Alliance -> Members -> Member item
    """
    user_id: int = HTField('UserID')
    login_name: str = HTField('Loginname')
    role_id: int = HTField('RoleId')
    role_name: str = HTField('RoleName')
    is_online: bool = HTField('IsOnline')
    membership_date: datetime = HTField('MembershipDate')
