from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestMatches(HTModel):
    """
    Matches - Request arguments
    """
    SOURCE_FILE = 'matches'
    LAST_VERSION = '2.9'

    _r_team_id: Optional[int] = HTInitVar('teamID', init_arg='team_id')
    _r_is_youth: Optional[bool] = HTInitVar('isYouth', init_arg='is_youth')
    _r_last_match_date: Optional[datetime] = HTInitVar('LastMatchDate', init_arg='last_match_date')


class Matches(RequestMatches):
    """
    Matches
    """
    team: 'Team' = HTField('Team')


class Team(HTModel):
    """
    Matches -> Team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    short_name: str = HTField('ShortTeamName')
    league: 'League' = HTField('League')
    league_level_unit: 'LeagueLevelUnit' = HTField('LeagueLevelUnit')
    matches: Optional[List['MatchItem']] = HTField('MatchList', items='Match')


class League(HTModel):
    """
    Matches -> Team -> League
    """
    id: int = HTField('LeagueID')
    name: str = HTField('LeagueName')


class LeagueLevelUnit(HTModel):
    """
    Matches -> Team -> League -> League Level Unit
    """
    id: int = HTField('LeagueLevelUnitID')
    name: str = HTField('LeagueLevelUnitName')
    level: int = HTField('LeagueLevel')


class MatchItem(HTModel):
    """
    Matches -> Team -> Matches -> Match item
    """
    id: int = HTField('MatchID')
    home_team: 'MatchItemTeam' = HTField('HomeTeam', xml_prefix='Home')
    away_team: 'MatchItemTeam' = HTField('AwayTeam', xml_prefix='Away')
    date: datetime = HTField('MatchDate')
    source_system: str = HTField('SourceSystem')
    type: int = HTField('MatchType')
    context_id: int = HTField('MatchContextId')
    cup_level: int = HTField('CupLevel')
    cup_level_index: int = HTField('CupLevelIndex')
    home_goals: Optional[int] = HTField('HomeGoals')
    away_goals: Optional[int] = HTField('AwayGoals')
    status: str = HTField('Status')
    orders_given: Optional[bool] = HTField('OrdersGiven')


class MatchItemTeam(HTModel):
    """
    Matches -> Team -> Matches -> Match item -> Home/Away team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    short_name: str = HTField('TeamNameShortName')
