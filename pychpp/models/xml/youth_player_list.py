from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestYouthPlayerList(HTModel):
    """
    Youth Player List - Request arguments
    """
    SOURCE_FILE = 'youthplayerlist'
    LAST_VERSION = '1.2'

    _r_action_type: Optional[str] = HTInitVar('actionType', init_arg='action_type')
    _r_order_by: Optional[str] = HTInitVar('orderBy', init_arg='order_by')
    _r_youth_team_id: Optional[int] = HTInitVar('youthTeamID', init_arg='youth_team_id')
    _r_show_scout_call: Optional[bool] = HTInitVar('showScoutCall', init_arg='show_scout_call')
    _r_show_last_match: Optional[bool] = HTInitVar('showLastMatch', init_arg='show_last_match')


class YouthPlayerListList(RequestYouthPlayerList):
    """
    Youth Player List - List
    """
    list: List['YouthPlayerListListPlayerItem'] = HTField('PlayerList', items='YouthPlayer')


class YouthPlayerListDetails(RequestYouthPlayerList):
    """
    Youth Player List - Details/Unlock skills
    """
    list: List['YouthPlayerListDetailsPlayerItem'] = HTField('PlayerList', items='YouthPlayer')


class YouthPlayerListListPlayerItem(HTModel):
    """
    Youth Player List - List -> Youth player item
    """
    id: int = HTField('YouthPlayerID')
    first_name: str = HTField('FirstName')
    nick_name: str = HTField('NickName')
    last_name: str = HTField('LastName')


class YouthPlayerListDetailsPlayerItem(YouthPlayerListListPlayerItem):
    """
    Youth Player List - Details/Unlock skills -> Youth player item
    """
    age: int = HTField('Age')
    age_days: int = HTField('AgeDays')
    arrival_date: datetime = HTField('ArrivalDate')
    can_be_promoted_in: bool = HTField('CanBePromotedIn')
    number: int = HTField('PlayerNumber')
    statement: Optional[str] = HTField('Statement')
    native_country_id: int = HTField('NativeCountryID')
    native_country_name: str = HTField('NativeCountryName')
    owner_notes: Optional[str] = HTField('OwnerNotes')
    category_id: Optional[int] = HTField('PlayerCategoryID')
    cards: int = HTField('Cards')
    injury_level: int = HTField('InjuryLevel')
    specialty: int = HTField('Specialty')
    career_goals: int = HTField('CareerGoals')
    careerHattricks: int = HTField('CareerHattricks')
    league_goals: int = HTField('LeagueGoals')
    friendly_goals: int = HTField('FriendlyGoals')
    owning_youth_team: 'OwningYouthTeam' = HTField('OwningYouthTeam')
    skills: 'Skills' = HTField('PlayerSkills')
    scout_call: Optional['ScoutCall'] = HTField('ScoutCall')
    last_match: Optional['LastMatch'] = HTField('LastMatch')


class OwningYouthTeam(HTModel):
    """
    Youth Player List - Details/Unlock skills -> Owning youth team
    """
    id: int = HTField('YouthTeamID')
    name: str = HTField('YouthTeamName')
    league_id: int = HTField('YouthTeamLeagueID')
    senior_team: 'OwningYouthTeamSeniorTeam' = HTField('SeniorTeam')


class OwningYouthTeamSeniorTeam(HTModel):
    """
    Youth Player List - Details/Unlock skills -> Owning youth team -> Senior team
    """
    id: int = HTField('SeniorTeamID')
    name: str = HTField('SeniorTeamName')


class Skills(HTModel):
    """
    Youth Player List - Details/Unlock skills -> Skills
    """
    keeper: 'SkillsSkillItem' = HTField('.', xml_prefix='Keeper')
    defender: 'SkillsSkillItem' = HTField('.', xml_prefix='Defender')
    playmaker: 'SkillsSkillItem' = HTField('.', xml_prefix='Playmaker')
    winger: 'SkillsSkillItem' = HTField('.', xml_prefix='Winger')
    scorer: 'SkillsSkillItem' = HTField('.', xml_prefix='Scorer')
    passing: 'SkillsSkillItem' = HTField('.', xml_prefix='Passing')
    set_pieces: 'SkillsSkillItem' = HTField('.', xml_prefix='SetPieces')


class SkillsSkillItem(HTModel):
    """
    Youth Player List - Details/Unlock skills -> Skills -> Skill item
    """
    skill: 'SkillsSkillItemSkill' = HTField('Skill')
    skill_max: 'SkillsSkillItemSkillMax' = HTField('SkillMax')


class SkillsSkillItemSkill(HTModel):
    """
    Youth Player List - Details/Unlock skills -> Skills -> Skill item -> Skill
    """
    is_available: bool = HTField('.', attrib='IsAvailable')
    is_max_reached: bool = HTField('.', attrib='IsMaxReached')
    may_unlock: bool = HTField('.', attrib='MayUnlock')
    level: int = HTField('.')


class SkillsSkillItemSkillMax(HTModel):
    """
    Youth Player List - Details/Unlock skills -> Skills -> Skill item -> Skill
    """
    is_available: bool = HTField('.', attrib='IsAvailable')
    may_unlock: bool = HTField('.', attrib='MayUnlock')
    level: int = HTField('.')


class ScoutCall(HTModel):
    """
    Youth Player List - Details/Unlock skills -> Scout call
    """
    scout: 'ScoutCallScout' = HTField('Scout')
    scouting_region_id: int = HTField('ScoutingRegionID')
    comments: List['ScoutCallCommentItem'] = HTField('ScoutComments', items='ScoutComment')


class ScoutCallScout(HTModel):
    """
    Youth Player List - Details/Unlock skills -> Scout call -> Scout
    """
    id: int = HTField('ScoutId')
    name: str = HTField('ScoutName')


class ScoutCallCommentItem(HTModel):
    """
    Youth Player List - Details/Unlock skills -> Scout call -> Comments -> Comment item
    """
    text: str = HTField('CommentText')
    type: int = HTField('CommentType')
    variation: int = HTField('CommentVariation')
    skill_type: int = HTField('CommentSkillType')
    skill_level: int = HTField('CommentSkillLevel')


class LastMatch(HTModel):
    """
    Youth Player List - Details/Unlock skills -> Last match
    """
    date: Optional[datetime] = HTField('Date')
    youth_match_id: Optional[int] = HTField('YouthMatchID')
    position_code: Optional[int] = HTField('PositionCode')
    played_minutes: Optional[int] = HTField('PlayedMinutes')
    rating: Optional[float] = HTField('Rating')
