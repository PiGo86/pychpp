from typing import Optional

from pychpp.models.custom import CustomModel
from pychpp.models.ht_field import HTProxyField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.xml.region_details import RequestRegionDetails, Region, RegionDetails


class HTRegion(RequestRegionDetails, CustomModel):
    """
    Hattrick region
    """
    URL_PATH = '/World/Regions/Region.aspx/'
    XML_PREFIX = 'League/Region/'

    _r_region_id: Optional[int] = HTInitVar('regionID', init_arg='region_id', fill_with='id')

    league_id: int = HTProxyField(RegionDetails, xml_prefix='../../')

    id: int = HTProxyField(Region)
    name: str = HTProxyField(Region)
    number_of_users: int = HTProxyField(Region)
    number_of_online: int = HTProxyField(Region)
    weather_id: int = HTProxyField(Region)
    tomorrow_weather_id: int = HTProxyField(Region)

    def league(self, **kwargs):
        return self._chpp.league(id_=self.league_id, **kwargs)