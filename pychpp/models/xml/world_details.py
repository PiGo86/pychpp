from datetime import datetime
from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestWorldDetails(HTModel):
    """
    World Details - Request arguments
    """
    SOURCE_FILE = 'worlddetails'
    LAST_VERSION = '1.9'

    _r_include_regions: Optional[bool] = HTInitVar('includeRegions', init_arg='include_regions')
    _r_country_id: Optional[int] = HTInitVar('countryID', init_arg='country_id')
    _r_league_id: Optional[int] = HTInitVar('leagueID', init_arg='league_id')


class WorldDetails(RequestWorldDetails):
    """
    World Details
    """
    leagues: List['LeagueItem'] = HTField('LeagueList', items='League')


class LeagueItem(HTModel):
    """
    World Details - Leagues - League item
    """
    id: int = HTField('LeagueID')
    name: str = HTField('LeagueName')
    season: int = HTField('Season')
    season_offset: int = HTField('SeasonOffset')
    match_round: int = HTField('MatchRound')
    short_name: str = HTField('ShortName')
    continent: str = HTField('Continent')
    zone_name: str = HTField('ZoneName')
    english_name: str = HTField('EnglishName')
    language_id: int = HTField('LanguageId')
    language_name: str = HTField('LanguageName')
    country: 'LeagueItemCountry' = HTField('Country')
    cups: List['LeagueItemCupItem'] = HTField('Cups', items='Cup')
    national_team_id: int = HTField('NationalTeamId')
    u20_team_id: int = HTField('U20TeamId')
    active_teams: int = HTField('ActiveTeams')
    active_users: int = HTField('ActiveUsers')
    waiting_users: int = HTField('WaitingUsers')
    training_date: datetime = HTField('TrainingDate')
    economy_date: datetime = HTField('EconomyDate')
    cup_match_date: datetime = HTField('CupMatchDate')
    series_match_date: datetime = HTField('SeriesMatchDate')
    sequences: 'LeagueItemSequences' = HTField('.')
    number_of_levels: int = HTField('NumberOfLevels')


class LeagueItemCountry(HTModel):
    """
    World Details > Leagues > League item -> Country
    """
    available: bool = HTField('.', attrib='Available')
    id: Optional[int] = HTField('CountryID')
    name: Optional[str] = HTField('CountryName')
    currency_rate: Optional[float] = HTField('CurrencyRate')
    code: Optional[str] = HTField('CountryCode')
    date_format: Optional[str] = HTField('DateFormat')
    time_format: Optional[str] = HTField('TimeFormat')
    regions: Optional[List['LeagueItemCountryRegionItem']] = HTField('RegionList', items='Region')


class LeagueItemCountryRegionItem(HTModel):
    """
    World Details > Leagues > League item -> Country -> Regions -> Region item
    """
    id: Optional[int] = HTField('RegionID')
    name: Optional[str] = HTField('RegionName')


class LeagueItemCupItem(HTModel):
    """
    World Details > Leagues > League item -> Cups -> Cup item
    """
    id: int = HTField('CupID')
    name: str = HTField('CupName')
    league_level: int = HTField('CupLeagueLevel')
    level: int = HTField('CupLevel')
    level_index: int = HTField('CupLevelIndex')
    match_round: int = HTField('MatchRound')
    match_rounds_left: int = HTField('MatchRoundsLeft')


class LeagueItemSequences(HTModel):
    """
    World Details > Leagues > League item -> Sequences
    """
    sequence_1: Optional[datetime] = HTField('Sequence1')
    sequence_2: Optional[datetime] = HTField('Sequence2')
    sequence_3: Optional[datetime] = HTField('Sequence3')
    sequence_4: Optional[datetime] = HTField('Sequence4')
    sequence_5: Optional[datetime] = HTField('Sequence5')
    sequence_6: Optional[datetime] = HTField('Sequence6')
    sequence_7: Optional[datetime] = HTField('Sequence7')
