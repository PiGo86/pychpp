from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestSupporters(HTModel):
    """
    Supporters - Request arguments
    """
    SOURCE_FILE = 'supporters'
    LAST_VERSION = '1.0'

    _r_action_type: Optional[str] = HTInitVar('actionType', init_arg='action_type')
    _r_user_id: Optional[int] = HTInitVar('userId', init_arg='user_id')
    _r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')
    _r_page_index: Optional[int] = HTInitVar('pageIndex', init_arg='page_index')
    _r_page_size: Optional[int] = HTInitVar('pageSize', init_arg='page_size')


class SupportersSupportedTeams(RequestSupporters):
    """
    Supporters - Supported teams
    """
    total_supported_teams: int = HTField('SupportedTeams', attrib='TotalItems')
    supported_teams: List['SupportedTeamItem'] = HTField('SupportedTeams', items='SupportedTeam')


class SupportersMySupporters(RequestSupporters):
    """
    Supporters - My supporters
    """
    total_supporters: int = HTField('MySupporters', attrib='TotalItems')
    my_supporters: List['MySupportersTeamItem'] = HTField('MySupporters', items='SupporterTeam')


class CommonTeamItem(HTModel):
    """
    Supporters - Supported teams/My Supporters -> Supported teams/My Supporters -> Team item
    """
    user_id: int = HTField('UserId')
    login_name: str = HTField('LoginName')
    team_id: int = HTField('TeamId')
    team_name: str = HTField('TeamName')
    league_id: int = HTField('LeagueID')
    league_name: str = HTField('LeagueName')
    league_level_unit_id: int = HTField('LeagueLevelUnitID')
    league_level_unit_name: str = HTField('LeagueLevelUnitName')


class SupportedTeamItem(CommonTeamItem):
    """
    Supporters - Supported teams -> Supported teams -> Team item
    """
    last_match: 'LastMatch' = HTField('LastMatch')
    next_match: 'NextMatch' = HTField('NextMatch')
    press_announcement: Optional['PressAnnouncement'] = HTField('PressAnnouncement')


class MySupportersTeamItem(CommonTeamItem):
    """
    Supporters - Supported teams -> My Supporters -> Team item
    """


class CommonLastNextMatch(HTModel):
    """
    Supporters - Supported teams -> Supported teams -> Team item -> Last/Next match
    """
    id: int = HTField('Id')
    date: datetime = HTField('Date')
    home_team_id: int = HTField('HomeTeamId')
    home_team_name: str = HTField('HomeTeamName')
    away_team_id: int = HTField('AwayTeamId')
    away_team_name: str = HTField('AwayTeamName')


class LastMatch(CommonLastNextMatch):
    """
    Supporters - Supported teams -> Supported teams -> Team item -> Last match
    """
    XML_PREFIX = 'LastMatch'
    home_goals: int = HTField('HomeGoals')
    away_goals: int = HTField('AwayGoals')


class NextMatch(CommonLastNextMatch):
    """
    Supporters - Supported teams -> Supported teams -> Team item -> Next match
    """
    XML_PREFIX = 'NextMatch'
    date: datetime = HTField('MatchDate')


class PressAnnouncement(HTModel):
    """
    Supporters - Supported teams -> Supported teams -> Team item -> Press Announcement
    """
    XML_PREFIX = 'PressAnnouncement'
    send_date: datetime = HTField('SendDate')
    subject: str = HTField('Subject')
    body: str = HTField('Body')
