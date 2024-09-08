from datetime import datetime
from typing import List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class MatchesArchive(HTModel):
    """
    Matches Archive
    """
    _r_team_id: int = HTInitVar('teamID', init_arg='team_id')
    _r_is_youth: bool = HTInitVar('isYouth', init_arg='is_youth')
    _r_first_match_date: datetime = HTInitVar('FirstMatchDate', init_arg='first_match_date')
    _r_last_match_date: datetime = HTInitVar('LastMatchDate', init_arg='last_match_date')
    _r_season: int = HTInitVar('season', init_arg='season')
    _r_include_hto: bool = HTInitVar('includeHTO', init_arg='include_hto')

    team_id: int = HTField('Team/TeamID')
    team_name: str = HTField('Team/TeamName')
    first_match_date: datetime = HTField('FirstMatchDate')
    last_match_date: datetime = HTField('LastMatchDate')
    matches: List['MatchItem'] = HTField('MatchList', items='Match')


class MatchItem(HTModel):
    """
    Matches Archives -> Matches -> Match item
    """
    id: int = HTField('MatchID')
    home_team: 'MatchItemHomeTeam' = HTField('HomeTeam')
    away_team: 'MatchItemAwayTeam' = HTField('AwayTeam')
    date: datetime = HTField('MatchDate')
    type_id: int = HTField('MatchType')
    context_id: int = HTField('MatchContextId')
    source_system: str = HTField('SourceSystem')
    rule_id: int = HTField('MatchRuleId')
    cup: 'MatchItemCup' = HTField('.')
    home_goals: int = HTField('HomeGoals')
    away_goals: int = HTField('AwayGoals')


class MatchItemHomeTeam(HTModel):
    """
    Matches Archives -> Matches -> Match item -> Home team
    """
    id: int = HTField('HomeTeamID')
    name: str = HTField('HomeTeamName')


class MatchItemAwayTeam(HTModel):
    """
    Matches Archives -> Matches -> Match item -> Away team
    """
    id: int = HTField('AwayTeamID')
    name: str = HTField('AwayTeamName')


class MatchItemCup(HTModel):
    """
    Matches Archives -> Matches -> Match item -> Cup
    """
    id: int = HTField('CupId')
    level: int = HTField('CupLevel')
    level_index: int = HTField('CupLevelIndex')
