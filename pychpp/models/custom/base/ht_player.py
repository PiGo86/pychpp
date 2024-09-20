from pychpp.models.custom import CustomModel
from pychpp.models.ht_init_var import HTInitVar


class BaseCommonHTPlayer(CustomModel):
    """
    Base model for Hattrick player, youth and senior
    """
    id: int
    first_name: str
    last_name: str

    def __repr__(self):
        return (f"<{self.__class__.__name__} object - "
                f"{self.first_name} {self.last_name} ({self.id})>")


class HTCommonLightPlayer(BaseCommonHTPlayer):
    """
    Base model for common Hattrick light player
    """
    is_youth: bool

    @property
    def url(self):
        if not self._url:
            if self.is_youth:
                self._url = self._BASE_URL + (f"/Club/Players/YouthPlayer.aspx"
                                              f"?youthPlayerID={self.id}")
            else:
                self._url = self._BASE_URL + (f"/Club/Players/Player.aspx"
                                              f"?playerID={self.id}")
        return self._url

    def details(self, **kwargs):
        if self.is_youth:
            return self._chpp.youth_player(id_=self.id, **kwargs)
        else:
            return self._chpp.player(id_=self.id, **kwargs)


class HTLightPlayer(BaseCommonHTPlayer):
    """
    Base model for Hattrick light player
    """
    URL_PATH = '/Club/Players/Player.aspx'

    # not used for fetching data, but to allow url property to work correctly
    _r_id = HTInitVar(param='playerID', init_arg='id_', fill_with='id')

    def details(self, **kwargs):
        return self._chpp.player(id_=self.id, **kwargs)


class HTLightYouthPlayer(BaseCommonHTPlayer):
    """
    Base model for Hattrick light youth player
    """
    URL_PATH = '/Club/Players/YouthPlayer.aspx'

    # not used for fetching data, but to allow url property to work correctly
    _r_id = HTInitVar(param='youthPlayerID', init_arg='id_', fill_with='id')

    def details(self, **kwargs):
        return self._chpp.youth_player(id_=self.id, **kwargs)