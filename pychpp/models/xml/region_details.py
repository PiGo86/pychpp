from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RegionDetails(HTModel):
    """
    Region Details
    """
    SOURCE_FILE = 'regiondetails'
    LAST_VERSION = '1.2'

    _r_region_id: int = HTInitVar('regionID', init_arg='region_id')

    league_id: int = HTField('League/LeagueID')
    league_name: str = HTField('League/LeagueName')
    region: 'Region' = HTField('League/Region')


class Region(HTModel):
    """
    Region Details -> Region
    """
    id: int = HTField('RegionID')
    name: str = HTField('RegionName')
    number_of_users: int = HTField('NumberOfUsers')
    number_of_online: int = HTField('NumberOfOnline')
    weather_id: int = HTField('WeatherID')
    tomorrow_weather_id: int = HTField('TomorrowWeatherID')