from pychpp.models.custom import CustomModel
from pychpp.models.ht_init_var import HTInitVar


class BaseHTRegion(CustomModel):
    """
    Base model for Hattrick region
    """
    id: int
    name: str

    URL_PATH = '/World/Regions/Region.aspx'

    def __repr__(self):
        return (f"<{self.__class__.__name__} object - "
                f"{self.name} ({self.id})>")


class HTLightRegion(BaseHTRegion):
    """
    Hattrick light region
    """

    _r_id = HTInitVar(param='regionID', init_arg='id_', fill_with='id')

    def details(self):
        return self._chpp.region(id_=self.id)
