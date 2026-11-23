"""Models for the `tournamentfixtures.xml` CHPP file."""

from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestTournamentFixtures(HTModel):
    """Tournament Fixtures - Request arguments."""
    SOURCE_FILE = 'tournamentfixtures'
    LAST_VERSION = '1.1'

    _r_tournament_id: int = HTInitVar('tournamentId', init_arg='tournament_id')
    _r_season: Optional[int] = HTInitVar('season', init_arg='season')
    _r_match_round: Optional[int] = HTInitVar('matchRound', init_arg='match_round')


class TournamentFixtures(RequestTournamentFixtures):
    """Tournament Fixtures."""
    matches: List['MatchItem'] = HTField('Matches', items='Match')


class MatchItem(HTModel):
    """Tournament Fixtures -> Matches -> Match item."""
    id: int = HTField('MatchId')
    home_team_id: int = HTField('HomeTeamId')
    home_team_name: str = HTField('HomeTeamName')
    home_short_team_name: str = HTField('HomeShortTeamName')
    away_team_id: int = HTField('AwayTeamId')
    away_team_name: str = HTField('AwayTeamName')
    away_short_team_name: str = HTField('AwayShortTeamName')
    date: datetime = HTField('MatchDate')
    type: int = HTField('MatchType')
    round: int = HTField('MatchRound')
    group: int = HTField('Group')
    status: int = HTField('Status')
    home_goals: int = HTField('HomeGoals')
    away_goals: int = HTField('AwayGoals')
    home_statement: str = HTField('HomeStatement')
    away_statement: str = HTField('AwayStatement')
