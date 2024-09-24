from pychpp.models.custom import CustomModel
from pychpp.models.ht_init_var import HTInitVar


class BaseHTLeagueUnit(CustomModel):
    """
    Base model for Hattrick league unit
    """
    id: int
    name: str

    URL_PATH = '/World/Series/'

    def __repr__(self):
        return (f"<{self.__class__.__name__} object - "
                f"{self.name} ({self.id})>")


class HTLightLeagueUnit(BaseHTLeagueUnit):
    """
    Hattrick light league unit
    """

    _r_id = HTInitVar(param='leagueLevelUnitID', init_arg='id_', fill_with='id')

    def details(self):
        return self._chpp.league_unit(id_=self.id)
