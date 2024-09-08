from pychpp.models.xml.region_details import RegionDetails

class HTRegion(RegionDetails):
    """
    Hattrick region
    """

    def league(self, **kwargs):
        return ht_league.HTLeague(chpp=self._chpp, league_id=self.league_id, **kwargs)