from datetime import datetime
from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestTeamHistory(HTModel):
    """
    Team History - Request arguments
    """
    SOURCE_FILE = 'teamhistory'
    LAST_VERSION = '1.0'

    _r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')


class TeamHistory(RequestTeamHistory):
    """
    Team History
    """
    XML_PREFIX = 'Team/'

    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    league: 'League' = HTField('League')
    founded_date: datetime = HTField('FoundedDate')
    history: List['SeasonItem'] = HTField('TeamHistory', items='Season')
    trophies: Optional[List['TrophyItem']] = HTField('TrophyList', items='Trophy')


class League(HTModel):
    """
    Team History -> League
    """
    id: int = HTField('LeagueID')
    name: str = HTField('LeagueName')


class SeasonItem(HTModel):
    """
    Team History -> Team history -> Season item
    """
    index: int = HTField('.', attrib='Index')
    season_number: int = HTField('SeasonNumber')
    league_level_unit_id: int = HTField('LeagueLevelUnitID')
    league_level_unit_name: str = HTField('LeagueLevelUnitName')
    league_level: int = HTField('LeagueLevel')
    position: int = HTField('Position')
    points: int = HTField('Points')
    goals_for: int = HTField('GoalsFor')
    goals_against: int = HTField('GoalsAgainst')
    cup_round: int = HTField('CupRound')
    cup_rounds_left: int = HTField('CupRoundsLeft')


class TrophyItem(HTModel):
    """
    Team History -> Trophy list -> Trophy item
    """
    type_id: int = HTField('TrophyTypeId')
    season: int = HTField('TrophySeason')
    league_level: int = HTField('LeagueLevel')
    league_level_unit_id: int = HTField('LeagueLevelUnitId')
    league_level_unit_name: str = HTField('LeagueLevelUnitName')
    gained_date: datetime = HTField('GainedDate')
    image_url: str = HTField('ImageUrl')
    cup_league_level: Optional[int] = HTField('CupLeagueLevel')
    cup_level: Optional[int] = HTField('CupLevel')
    cup_level_index: Optional[int] = HTField('CupLevelIndex')
