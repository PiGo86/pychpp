from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestCupMatches(HTModel):
    """
    Cup Matches - Request arguments
    """
    SOURCE_FILE = "cupmatches"
    LAST_VERSION = "1.4"

    _r_cup_id: int = HTInitVar('CupID', init_arg='cup_id')
    _r_season: Optional[int] = HTInitVar('Season', init_arg='season')
    _r_cup_round: Optional[int] = HTInitVar('CupRound', init_arg='cup_round')
    _s_start_after_match_id: Optional[int] = HTInitVar('StartAfterMatchID',
                                                       init_arg='start_after_match_id')


class CupMatches(RequestCupMatches):
    """
    Cup Matches
    """
    XML_PREFIX = 'Cup/'

    id: int = HTField('CupID')
    season: int = HTField('CupSeason')
    round: int = HTField('CupRound')
    name: str = HTField('CupName')
    match_list: List['MatchListMatchItem'] = HTField('MatchList', items='Match')


class MatchListMatchItem(HTModel):
    """
    Cup Matches -> Match list -> Match item
    """
    id: int = HTField('MatchID')
    date: datetime = HTField('MatchDate')
    home_team: 'MatchListMatchItemTeam' = HTField('HomeTeam')
    away_team: 'MatchListMatchItemTeam' = HTField('AwayTeam')
    match_result: 'MatchListMatchItemMatchResult' = HTField('MatchResult')
    league_info: 'MatchListMatchItemLeagueInfo' = HTField('LeagueInfo')


class MatchListMatchItemTeam(HTModel):
    """
    Cup Matches -> Match list -> Match item -> Home/Away team
    """
    id: int = HTField('TeamId')
    name: str = HTField('TeamName')


class MatchListMatchItemMatchResult(HTModel):
    """
    Cup Matches -> Match list -> Match item -> Match result
    """
    available: bool = HTField('.', attrib='Available')
    home_goals: Optional[int] = HTField('HomeGoals')
    away_goals: Optional[int] = HTField('AwayGoals')


class MatchListMatchItemLeagueInfo(HTModel):
    """
    Cup Matches -> Match list -> Match item -> League info
    """
    available: bool = HTField('.', attrib='Available')
    home_league: Optional['MatchListMatchItemLeagueInfoTeam'] = HTField('.',
                                                                        xml_prefix='HomeLeague')
    away_league: Optional['MatchListMatchItemLeagueInfoTeam'] = HTField('.',
                                                                        xml_prefix='AwayLeague')


class MatchListMatchItemLeagueInfoTeam(HTModel):
    """
    Cup Matches -> Match list -> Match item -> League info -> Home/Away team league info
    """
    id: Optional[int] = HTField('ID')
    name: Optional[str] = HTField('Name')
