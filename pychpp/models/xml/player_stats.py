"""Models for the `playerstats.xml` CHPP file."""

from datetime import datetime
from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestPlayerStats(HTModel):
    """Player Stats - Request arguments."""
    SOURCE_FILE = 'playerstats'
    LAST_VERSION = '1.0'

    _r_player_id: Optional[int] = HTInitVar('playerID', init_arg='player_id')


class PlayerStats(RequestPlayerStats):
    """Player Stats."""
    XML_PREFIX = 'Player/'

    id: int = HTField('PlayerID')
    first_name: str = HTField('FirstName')
    nick_name: str = HTField('NickName')
    last_name: str = HTField('LastName')
    number: Optional[int] = HTField('PlayerNumber')
    owning_team: 'OwningTeam' = HTField('OwningTeam')
    match_stats: List['MatchItem'] = HTField('MatchStats', items='Match')


class OwningTeam(HTModel):
    """Player Stats -> Owning team."""
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    league_id: int = HTField('LeagueID')


class MatchItem(HTModel):
    """Player Stats -> Match stats -> Match item."""
    id: int = HTField('MatchID')
    type: int = HTField('MatchType')
    source_system: str = HTField('SourceSystem')
    date: datetime = HTField('MatchDate')
    home_team: 'MatchItemHomeTeam' = HTField('HomeTeam')
    away_team: 'MatchItemAwayTeam' = HTField('AwayTeam')
    is_walkover: bool = HTField('IsWalkover')
    age: int = HTField('Age')
    age_days: int = HTField('AgeDays')
    tsi: int = HTField('TSI')
    form: int = HTField('PlayerForm')
    stamina: Optional[int] = HTField('Stamina')
    loyalty: Optional[int] = HTField('Loyalty')
    experience: int = HTField('Experience')
    goals: int = HTField('GoalsInMatch')
    yellow_cards: int = HTField('YellowCardsInMatch')
    red_cards: int = HTField('RedCardsInMatch')
    injury_level: int = HTField('InjuryLevel')
    played_minutes: int = HTField('PlayedMinutes')
    rating: float = HTField('Rating')
    rating_end_of_game: float = HTField('RatingEndOfGame')
    positions: Optional[List['PositionItem']] = HTField('Positions', items='Position')


class MatchItemHomeTeam(HTModel):
    """Player Stats -> Match stats -> Match item -> Home team."""
    name: str = HTField('HomeTeamName')


class MatchItemAwayTeam(HTModel):
    """Player Stats -> Match stats -> Match item -> Away team."""
    name: str = HTField('AwayTeamName')


class PositionItem(HTModel):
    """Player Stats -> Match stats -> Match item -> Positions -> Position item."""
    position_code: int = HTField('PositionCode')
    minutes: int = HTField('Minutes')
