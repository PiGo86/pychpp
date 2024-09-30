from datetime import datetime
from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestLeagueFixtures(HTModel):
    """
    League Fixtures - Request arguments
    """
    SOURCE_FILE = 'leaguefixtures'
    LAST_VERSION = '1.2'

    _r_league_level_unit_id: int = HTInitVar('leagueLevelUnitID', init_arg='league_level_unit_id')
    _r_season: int = HTInitVar('season', init_arg='season')


class LeagueFixtures(RequestLeagueFixtures):
    """
    League Fixtures
    """
    id: int = HTField('LeagueLevelUnitID')
    name: str = HTField('LeagueLevelUnitName')
    season: int = HTField('Season')

    matches: List['MatchItem'] = HTField('.', items='Match')


class MatchItem(HTModel):
    """
    League Fixtures -> Match item
    """
    id: int = HTField('MatchID')
    round: int = HTField('MatchRound')
    home_team: 'MatchItemHomeTeamItem' = HTField('HomeTeam')
    away_team: 'MatchItemAwayTeamItem' = HTField('AwayTeam')
    date: datetime = HTField('MatchDate')
    home_goals: Optional[int] = HTField('HomeGoals')
    away_goals: Optional[int] = HTField('AwayGoals')


class MatchItemHomeTeamItem(HTModel):
    """
    League Fixtures -> Match item -> Home team item
    """
    id: int = HTField('HomeTeamID')
    name: str = HTField('HomeTeamName')


class MatchItemAwayTeamItem(HTModel):
    """
    League Fixtures -> Match item -> Away team item
    """
    id: int = HTField('AwayTeamID')
    name: str = HTField('AwayTeamName')
