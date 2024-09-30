from datetime import datetime
from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestBaseWorldCup(HTModel):
    """
    Base World Cup - Request arguments
    """
    SOURCE_FILE = 'worldcup'
    LAST_VERSION = '1.1'

    _r_action_type: Optional[str] = HTInitVar('actionType', init_arg='action_type')
    _r_cup_id: Optional[int] = HTInitVar('cupID', init_arg='cup_id')
    _r_season: int = HTInitVar('season', init_arg='season')


class BaseWorldCup(RequestBaseWorldCup):
    """
    Base World Cup
    """
    cup_id: int = HTField('CupID')
    season: int = HTField('Season')
    match_round: int = HTField('MatchRound')


class RequestWorldCupViewMatches(RequestBaseWorldCup):
    """
    World Cup - View matches - Request arguments
    """
    _r_match_round: Optional[int] = HTInitVar('matchRound', init_arg='match_round')
    _r_cup_series_unit_id: int = HTInitVar('cupSeriesUnitID', init_arg='cup_series_unit_id')


class WorldCupViewMatches(RequestWorldCupViewMatches, BaseWorldCup):
    """
    World Cup - View matches
    """
    cup_series_unit_id: int = HTField('CupSeriesUnitID')
    matches: Optional[List['ViewMatchesMatchItem']] = HTField('Matches', items='Match')
    rounds: List['ViewMatchesRoundItem'] = HTField('Rounds', items='Round')


class ViewMatchesMatchItem(HTModel):
    """
    World Cup - View matches -> Matches -> Match item
    """
    id: int = HTField('MatchID')
    home_team: 'ViewMatchesMatchItemTeam' = HTField('HomeTeam')
    away_team: 'ViewMatchesMatchItemTeam' = HTField('AwayTeam')
    date: datetime = HTField('MatchDate')
    finished_date: datetime = HTField('FinishedDate')
    home_goals: int = HTField('HomeGoals')
    away_goals: int = HTField('AwayGoals')


class ViewMatchesMatchItemTeam(HTModel):
    """
    World Cup - View matches -> Matches -> Match item -> Home/Away team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')


class ViewMatchesRoundItem(HTModel):
    """
    World Cup - View matches -> Rounds -> Round item
    """
    match_round: int = HTField('MatchRound')
    start_date: datetime = HTField('StartDate')


class RequestWorldCupViewGroups(RequestBaseWorldCup):
    """
    World Cup - View groups - Request arguments
    """


class WorldCupViewGroups(RequestWorldCupViewGroups, BaseWorldCup):
    """
    World Cup - View groups
    """
    scores: List['ViewGroupsTeamItem'] = HTField('WorldCupScores', items='Team')
    rounds: List['ViewGroupsRoundItem'] = HTField('Rounds', items='Round')


class ViewGroupsTeamItem(HTModel):
    """
    World Cup - View groups -> Scores -> Team item
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    place: int = HTField('Place')
    cup_series_unit_id: int = HTField('CupSeriesUnitID')
    cup_series_unit_name: str = HTField('CupSeriesUnitName')
    matches_played: int = HTField('MatchesPlayed')
    goals_for: int = HTField('GoalsFor')
    goals_against: int = HTField('GoalsAgainst')
    points: int = HTField('Points')


class ViewGroupsRoundItem(HTModel):
    """
    World Cup - View groups -> Rounds -> Round item
    """
    match_round: int = HTField('MatchRound')
    start_date: datetime = HTField('StartDate')
