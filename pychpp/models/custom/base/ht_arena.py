from pychpp.models.custom import CustomModel
from pychpp.models.ht_init_var import HTInitVar


class BaseHTArena(CustomModel):
    """
    Base model for Hattrick arena
    """
    id: int
    name: str

    URL_PATH = '/Club/Stadium/'

    def __repr__(self):
        return (f"<{self.__class__.__name__} object - "
                f"{self.name} ({self.id})>")


class HTLightArena(BaseHTArena):
    """
    Hattrick light league
    """

    _r_id = HTInitVar(param='arenaID', init_arg='id_', fill_with='id')

    def details(self):
        return self._chpp.arena(id_=self.id)
