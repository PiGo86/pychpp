from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestYouthLeagueFixtures(HTModel):
    """
    Youth League Fixtures - Request arguments
    """
    SOURCE_FILE = 'youthleaguefixtures'
    LAST_VERSION = '1.0'

    _r_youth_league_id: Optional[int] = HTInitVar('youthleagueid', init_arg='youth_league_id')
    _r_season: Optional[int] = HTInitVar('season')


class YouthLeagueFixtures(RequestYouthLeagueFixtures):
    """
    Youth League Fixtures
    """
    id: int = HTField('YouthLeagueID')
    name: str = HTField('YouthLeagueName')
    type: int = HTField('YouthLeagueType')
    season: int = HTField('Season')
    last_match_round: int = HTField('LastMatchRound')
    nr_of_teams_in_league: int = HTField('NrOfTeamsInLeague')
    matches: List['MatchItem'] = HTField('Matches', items='Match')


class MatchItem(HTModel):
    """
    Youth League Fixtures -> Matches -> Match item
    """
    id: int = HTField('MatchID')
    round: int = HTField('MatchRound')
    status: str = HTField('Status')
    home_team: 'Team' = HTField('HomeTeam', xml_prefix='Home')
    away_team: 'Team' = HTField('AwayTeam', xml_prefix='Away')
    date: datetime = HTField('MatchDate')
    home_goals: Optional[int] = HTField('HomeGoals')
    away_goals: Optional[int] = HTField('AwayGoals')


class Team(HTModel):
    """
    Youth League Fixtures -> Matches -> Match item -> Home/Away teams
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
