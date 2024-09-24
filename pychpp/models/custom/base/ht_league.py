from pychpp.models.custom import CustomModel
from pychpp.models.ht_init_var import HTInitVar


class BaseHTLeague(CustomModel):
    """
    Base model for Hattrick team
    """
    id: int
    name: str

    URL_PATH = '/World/Leagues/League.aspx'

    def __repr__(self):
        return (f"<{self.__class__.__name__} object - "
                f"{self.name} ({self.id})>")


class HTLightLeague(BaseHTLeague):
    """
    Hattrick light league
    """

    _r_id = HTInitVar(param='leagueID', init_arg='id_', fill_with='id')

    def details(self):
        return self._chpp.league(id_=self.id)
