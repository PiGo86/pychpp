from pychpp.models.custom import CustomModel
from pychpp.models.xml.region_details import RegionDetails

class HTRegion(RegionDetails, CustomModel):
    """
    Hattrick region
    """

    URL_PATH = '/World/Regions/Region.aspx'

    def league(self, **kwargs):
        return ht_league.HTLeague(chpp=self._chpp, league_id=self.league_id, **kwargs)