from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_model import HTField, HTInitVar, HTModel


class CommonRequestArenaDetails(HTModel):
    """
    Arena Details - Common request arguments
    """
    SOURCE_FILE = "arenadetails"
    LAST_VERSION = "1.7"

    _r_stats_type: Optional[str] = HTInitVar('StatsType', init_arg='stats_type')


class RequestArenaDetailsDefault(CommonRequestArenaDetails):
    """
    Arena Details - Default - Request arguments
    """
    _r_arena_id: Optional[int] = HTInitVar('arenaID', init_arg='arena_id', fill_with='id')
    _r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')


class ArenaDetailsDefault(RequestArenaDetailsDefault):
    """
    Arena Details
    """
    id: int = HTField('Arena/ArenaID')
    name: str = HTField('Arena/ArenaName')
    image: str = HTField('Arena/ArenaImage')
    fallback_image: str = HTField('Arena/ArenaFallbackImage')
    team: 'Team' = HTField('Arena/Team')
    league: 'League' = HTField('Arena/League')
    region: 'Region' = HTField('Arena/Region')
    current_capacity: 'CurrentCapacity' = HTField('Arena/CurrentCapacity')
    expanded_capacity: 'ExpandedCapacity' = HTField('Arena/ExpandedCapacity')


class Team(HTModel):
    """
    Arena Details -> Team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')


class League(HTModel):
    """
    Arena Details -> League
    """
    id: int = HTField('LeagueID')
    name: str = HTField('LeagueName')


class Region(HTModel):
    """
    Arena Details -> Region
    """
    id: int = HTField('RegionID')
    name: str = HTField('RegionName')


class BaseCapacity(HTModel):
    """
    Arena Details -> Base capacity
    """
    terraces: Optional[int] = HTField('Terraces')
    basic: Optional[int] = HTField('Basic')
    roof: Optional[int] = HTField('Roof')
    vip: Optional[int] = HTField('VIP')
    total: Optional[int] = HTField('Total')


class CurrentCapacity(BaseCapacity):
    """
    Arena Details -> Current capacity
    """
    rebuilt_date: Optional[datetime] = HTField('RebuiltDate')


class ExpandedCapacity(BaseCapacity):
    """
    Arena Details -> Expanded capacity
    """
    available: bool = HTField('.', attrib='Available')
    expansion_date: Optional[datetime] = HTField('ExpansionDate')


class RequestArenaDetailsMyArena(CommonRequestArenaDetails):
    """
    Arena Details - My Arena - Request arguments
    """
    _r_arena_id: Optional[int] = HTInitVar('arenaID', init_arg='id', fill_with='id')
    _r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')
    _r_match_type: Optional[str] = HTInitVar('MatchType', init_arg='match_type')
    _r_first_date: Optional[datetime] = HTInitVar('FirstDate', init_arg='first_date')
    _r_last_date: Optional[datetime] = HTInitVar('LastDate', init_arg='last_date')


class ArenaDetailsMyArena(RequestArenaDetailsMyArena):
    """
    Arena Details - My Arena
    """
    id: Optional[int] = HTField('MyArena/ArenaID')
    name: Optional[str] = HTField('MyArena/ArenaName')
    image: Optional[str] = HTField('MyArena/ArenaImage')
    fallback_image: Optional[str] = HTField('MyArena/ArenaFallbackImage')
    match_types: Optional[str] = HTField('MyArena/MatchTypes')
    first_date: Optional[datetime] = HTField('MyArena/FirstDate')
    last_date: Optional[datetime] = HTField('MyArena/LastDate')
    number_of_matches: Optional[int] = HTField('MyArena/NumberOfMatches')
    visitors_average: Optional['Visitors'] = HTField('VisitorsAverage')
    visitors_most: Optional['Visitors'] = HTField('VisitorsMost')
    visitors_least: Optional['Visitors'] = HTField('VisitorsLeast')


class Visitors(HTModel):
    """
    Arena Details - My Arena - Visitors (average, most or least)
    """
    terraces: int = HTField('Terraces')
    basic: int = HTField('Basic')
    roof: int = HTField('Roof')
    vip: int = HTField('VIP')
    total: int = HTField('Total')


class RequestArenaDetailsLeagueArenaStats(CommonRequestArenaDetails):
    """
    Arena Details - League Arena Stats - Request arguments
    """
    _r_league_id: int = HTInitVar('StatsLeagueID', init_arg='league_id')


class ArenaDetailsLeagueArenaStats(RequestArenaDetailsLeagueArenaStats):
    """
    Arena Details - League Arena Stats
    """
    league_id: int = HTField('LeagueArenaStats/LeagueID')
    league_name: str = HTField('LeagueArenaStats/LeagueName')
    created_date: datetime = HTField('LeagueArenaStats/CreatedDate')
    arenas: List['Arenas'] = HTField('OtherArenasStatList', items='ArenaStat')


class Arenas(HTModel):
    """
    Arena Details - League Arena Stats - Arena item
    """
    id: int = HTField('ArenaID')
    name: str = HTField('ArenaName')
    image: str = HTField('ArenaImage')
    fallback_image: str = HTField('ArenaFallbackImage')
    arena_size: int = HTField('ArenaSize')
    arena_league_id: int = HTField('ArenaLeagueID')
    arena_league_name: str = HTField('ArenaLeagueName')
    arena_region_id: int = HTField('ArenaRegionID')
    arena_region_name: str = HTField('ArenaRegionName')
