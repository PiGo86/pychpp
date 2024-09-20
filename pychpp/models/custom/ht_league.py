from typing import List

from pychpp.models.custom.base.ht_country import BaseHTCountry
from pychpp.models.custom.base.ht_league import BaseHTLeague
from pychpp.models.custom.base.ht_region import HTLightRegion
from pychpp.models.ht_field import HTProxyField
from pychpp.models.xml.world_details import RequestWorldDetails, LeagueItem, LeagueItemCountry, \
    LeagueItemCountryRegionItem


class HTLeague(RequestWorldDetails, LeagueItem, BaseHTLeague):
    """
    Hattrick League
    """
    XML_PREFIX = 'LeagueList/League/'

    country: 'HTLeagueCountry' = HTProxyField(LeagueItem)


class HTLeagueCountry(LeagueItemCountry, BaseHTCountry):
    regions: List['HTLeagueCountryRegion'] = HTProxyField(LeagueItemCountry)


class HTLeagueCountryRegion(LeagueItemCountryRegionItem, HTLightRegion):
    pass
