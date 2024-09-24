from pychpp.models.custom import CustomModel
from pychpp.models.ht_init_var import HTInitVar


class BaseHTUser(CustomModel):
    """
    Base model for Hattrick user
    """
    id: int
    username: str

    URL_PATH = '/Club/Manager/'

    def __repr__(self):
        return (f"<{self.__class__.__name__} object - "
                f"{self.username} ({self.id})>")


class HTLightUser(BaseHTUser):
    """
    Hattrick light user
    """

    _r_id = HTInitVar(param='userID', init_arg='id_', fill_with='id')

    def details(self):
        return self._chpp.user(id_=self.id)
