from pychpp.models.custom import CustomModel
from pychpp.models.ht_init_var import HTInitVar


class BaseHTCountry(CustomModel):
    """
    Base model for Hattrick country
    """
    id: int
    name: str

    URL_PATH = '/World/Leagues/League.aspx'

    def __repr__(self):
        return (f"<{self.__class__.__name__} object - "
                f"{self.name} ({self.id})>")


class HTLightCountry(BaseHTCountry):
    """
    Hattrick light country
    """

    _r_id = HTInitVar(param='countryID', init_arg='id_', fill_with='id')

    def details(self, **kwargs):
        return self._chpp.league(country_id=self.id, **kwargs)
