from typing import Optional

from pychpp.models.custom.base.ht_region import BaseHTRegion, HTLightRegion
from pychpp.models.ht_field import HTProxyField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.xml.region_details import RequestRegionDetails, Region, RegionDetails, League


class HTRegion(RequestRegionDetails, BaseHTRegion):
    """
    Hattrick region
    """
    XML_PREFIX = 'League/Region/'

    _r_region_id: Optional[int] = HTInitVar('regionID', init_arg='region_id', fill_with='id')

    id: int = HTProxyField(Region)
    name: str = HTProxyField(Region)
    number_of_users: int = HTProxyField(Region)
    number_of_online: int = HTProxyField(Region)
    weather_id: int = HTProxyField(Region)
    tomorrow_weather_id: int = HTProxyField(Region)

    league: 'HTRegionLeague' = HTProxyField(RegionDetails, xml_prefix='../../')


class HTRegionLeague(HTLightRegion, League):
    """
    Hattrick region -> League
    """
