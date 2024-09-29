from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestYouthTeamDetails(HTModel):
    """
    Youth Team Details - Request arguments
    """
    SOURCE_FILE = 'youthteamdetails'
    LAST_VERSION = '1.2'

    _r_youth_team_id: Optional[int] = HTInitVar('youthTeamID', init_arg='youth_team_id')
    _r_show_scouts: Optional[bool] = HTInitVar('showScouts', init_arg='show_scouts')

    XML_PREFIX = 'YouthTeam/'


class YouthTeamDetails(RequestYouthTeamDetails):
    """
    Youth Team Details
    """
    id: int = HTField('YouthTeamID')
    name: str = HTField('YouthTeamName')
    short_name: str = HTField('ShortTeamName')
    created_date: datetime = HTField('CreatedDate')
    user_id: int = HTField('UserId')
    country: 'Country' = HTField('Country')
    region: 'Region' = HTField('Region')
    arena: 'Arena' = HTField('YouthArena')
    league: 'League' = HTField('YouthLeague')
    owning_team: 'OwningTeam' = HTField('OwningTeam')
    trainer: 'Trainer' = HTField('YouthTrainer')
    next_training_match_date: datetime = HTField('NextTrainingMatchDate')
    scouts: Optional[List['ScoutItem']] = HTField('ScoutList', items='Scout')


class Country(HTModel):
    """
    Youth Team Details -> Country
    """
    id: int = HTField('CountryID')
    name: str = HTField('CountryName')


class Region(HTModel):
    """
    Youth Team Details -> Region
    """
    id: int = HTField('RegionID')
    name: str = HTField('RegionName')


class Arena(HTModel):
    """
    Youth Team Details -> Arena
    """
    id: int = HTField('YouthArenaID')
    name: str = HTField('YouthArenaName')


class League(HTModel):
    """
    Youth Team Details -> League
    """
    id: int = HTField('YouthLeagueID')
    name: str = HTField('YouthLeagueName')
    status: int = HTField('YouthLeagueStatus')


class OwningTeam(HTModel):
    """
    Youth Team Details -> Owning team
    """
    id: int = HTField('MotherTeamID')
    name: str = HTField('MotherTeamName')


class Trainer(HTModel):
    """
    Youth Team Details -> Trainer
    """
    id: int = HTField('YouthPlayerID')


class ScoutItem(HTModel):
    """
    Youth Team Details -> Scouts -> Scout item
    """
    id: int = HTField('YouthScoutID')
    name: str = HTField('ScoutName')
    age: int = HTField('Age')
    country: 'Country' = HTField('Country')
    region: 'Region' = HTField('Region')
    in_country: 'Country' = HTField('InCountry')
    in_region: 'Region' = HTField('InRegion')
    hired_date: datetime = HTField('HiredDate')
    last_called: datetime = HTField('LastCalled')
    player_type_search: int = HTField('PlayerTypeSearch')
    hof_player_id: int = HTField('HofPlayerId')
    travel: 'Travel' = HTField('Travel')


class Travel(HTModel):
    """
    Youth Team Details -> Scouts -> Scout item -> Travel
    """
    start_date: datetime = HTField('TravelStartDate')
    length: int = HTField('TravelLength')
    type: int = HTField('TravelType')
