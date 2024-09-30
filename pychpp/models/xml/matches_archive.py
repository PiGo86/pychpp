from datetime import datetime, date
from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestMatchesArchive(HTModel):
    """
    Matches Archive - Request arguments
    """
    SOURCE_FILE = 'matchesarchive'
    LAST_VERSION = '1.5'

    _r_team_id: Optional[int] = HTInitVar('teamID', init_arg='team_id', fill_with='team_id')
    _r_is_youth: Optional[bool] = HTInitVar('isYouth', init_arg='is_youth')
    _r_first_match_date: Optional[date] = HTInitVar('FirstMatchDate', init_arg='first_match_date')
    _r_last_match_date: Optional[date] = HTInitVar('LastMatchDate', init_arg='last_match_date')
    _r_season: Optional[int] = HTInitVar('season', init_arg='season')
    _r_include_hto: Optional[bool] = HTInitVar('includeHTO', init_arg='include_hto')

    XML_PREFIX = 'Team/'


class MatchesArchive(RequestMatchesArchive):
    """
    Matches Archive
    """
    team: 'Team' = HTField('.')
    first_match_date: Optional[datetime] = HTField('FirstMatchDate')
    last_match_date: Optional[datetime] = HTField('LastMatchDate')
    matches: List['MatchItem'] = HTField('MatchList', items='Match')


class Team(HTModel):
    """
    Matches Archives -> Team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')


class MatchItem(HTModel):
    """
    Matches Archives -> Matches -> Match item
    """
    id: int = HTField('MatchID')
    home_team: 'MatchItemTeam' = HTField('HomeTeam', xml_prefix='Home')
    away_team: 'MatchItemTeam' = HTField('AwayTeam', xml_prefix='Away')
    date: datetime = HTField('MatchDate')
    type_id: int = HTField('MatchType')
    context_id: int = HTField('MatchContextId')
    source_system: str = HTField('SourceSystem')
    rule_id: int = HTField('MatchRuleId')
    cup: 'MatchItemCup' = HTField('.')
    home_goals: int = HTField('HomeGoals')
    away_goals: int = HTField('AwayGoals')


class MatchItemTeam(HTModel):
    """
    Matches Archives -> Matches -> Match item -> Team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')


class MatchItemCup(HTModel):
    """
    Matches Archives -> Matches -> Match item -> Cup
    """
    id: int = HTField('CupId')
    level: int = HTField('CupLevel')
    level_index: int = HTField('CupLevelIndex')
