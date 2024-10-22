from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestLeagueLevels(HTModel):
    """
    League Levels - Request arguments
    """
    SOURCE_FILE = 'leaguelevels'
    LAST_VERSION = '1.0'

    _r_league_id: Optional[int] = HTInitVar('LeagueID', init_arg='league_id')


class LeagueLevels(RequestLeagueLevels):
    """
    League Levels
    """
    id: int = HTField('LeagueID')
    season: int = HTField('Season')
    nr_of_league_levels: int = HTField('NrOfLeagueLevels')
    levels: List['LeagueLevelItem'] = HTField('LeagueLevelList', items='LeagueLevelItem')


class LeagueLevelItem(HTModel):
    """
    League Levels -> Levels -> League Level item
    """
    league_level: int = HTField('LeagueLevel')
    nr_of_league_level_units: int = HTField('NrOfLeagueLevelUnits')
    nr_of_teams: int = HTField('NrOfTeams')
    league_level_unit_id_list: str = HTField('LeagueLevelUnitIdList')
    nr_of_shared_promotion_slots_per_series: int = HTField('NrOfSharedPromotionSlotsPerSeries')
    nr_of_direct_promotion_slots_per_series: int = HTField('NrOfDirectPromotionSlotsPerSeries')
    nr_of_qualification_promotion_slots_per_series: int = HTField(
        'NrOfQualificationPromotionSlotsPerSeries',
    )
    nr_of_direct_demotion_slots_per_series: int = HTField('NrOfDirectDemotionSlotsPerSeries')
    nr_of_qualification_demotion_slots_per_series: int = HTField(
        'NrOfQualificationDemotionSlotsPerSeries',
    )
