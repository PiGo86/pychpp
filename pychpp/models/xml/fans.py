from datetime import datetime
from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestFans(HTModel):
    """
    Fans - Request arguments
    """
    SOURCE_FILE = 'fans'
    LAST_VERSION = '1.3'

    _r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')


class Fans(RequestFans):
    """
    Fans
    """
    team: 'Team' = HTField('Team')


class Team(HTModel):
    """
    Fans -> Team
    """
    id: int = HTField('TeamID')
    fan_club_id: int = HTField('FanclubId')
    fan_club_name: str = HTField('FanclubName')
    fan_mood: int = HTField('FanMood')
    members: int = HTField('Members')
    fan_season_expectation: int = HTField('FanSeasonExpectation')
    played_matches: List['PlayedMatchItem'] = HTField('PlayedMatches', items='Match')
    upcoming_matches: List['UpcomingMatchItem'] = HTField('UpcomingMatches', items='Match')


class BaseMatchItem(HTModel):
    """
    Fans -> Team -> Played/Upcoming matches -> Match item
    """
    id: int = HTField('MatchID')
    home_team: 'BaseMatchItemTeam' = HTField('HomeTeam', xml_prefix='Home')
    away_team: 'BaseMatchItemTeam' = HTField('AwayTeam', xml_prefix='Away')
    date: datetime = HTField('MatchDate')
    type: int = HTField('MatchType')
    fan_match_expectation: int = HTField('FanMatchExpectation')


class BaseMatchItemTeam(HTModel):
    """
    Fans -> Team -> Played/Upcoming matches -> Match item -> Home/Away team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')


class PlayedMatchItem(BaseMatchItem):
    """
    Fans -> Team -> Played matches -> Match item
    """
    home_goals: int = HTField('HomeGoals')
    away_goals: int = HTField('AwayGoals')
    fan_mood_after_match: int = HTField('FanMoodAfterMatch')
    weather: int = HTField('Weather')
    sold_seats: int = HTField('SoldSeats')


class UpcomingMatchItem(BaseMatchItem):
    """
    Fans -> Team -> Upcoming matches -> Match item
    """
