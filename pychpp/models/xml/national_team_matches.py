from datetime import datetime
from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestNationalTeamMatches(HTModel):
    """
    National Team Matches - Request arguments
    """
    SOURCE_FILE = 'nationalteammatches'
    LAST_VERSION = '1.4'

    _r_league_office_type_id: Optional[int] = HTInitVar('LeagueOfficeTypeID',
                                                        init_arg='league_office_type_id')


class NationalTeamMatches(RequestNationalTeamMatches):
    """
    National Team Matches
    """
    user_supporter_tier: str = HTField('UserSupporterTier')
    league_office_type_id: int = HTField('LeagueOfficeTypeID')
    matches: List['MatchItem'] = HTField('Matches', items='Match')


class MatchItem(HTModel):
    """
    National Team Matches -> Matches -> Match item
    """
    id: int = HTField('MatchID')
    date: datetime = HTField('MatchDate')
    type: int = HTField('MatchType')
    context_id: Optional[int] = HTField('MatchContextId')
    home_team_id: int = HTField('HomeTeamId')
    home_team_name: str = HTField('HomeTeamName')
    away_team_id: int = HTField('AwayTeamId')
    away_team_name: str = HTField('AwayTeamName')
    match_result: Optional['MatchResult'] = HTField('MatchResult')


class MatchResult(HTModel):
    """
    National Team Matches -> Matches -> Match item -> Match result
    """
    home_goals: Optional[int] = HTField('HomeGoals')
    away_goals: Optional[int] = HTField('AwayGoals')
