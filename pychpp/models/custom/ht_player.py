from pychpp.models.custom import CustomModel
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.xml.player_details import PlayerDetails
from pychpp.models.xml.players import PlayersViewTeamPlayerItem, RequestPlayers


class BaseHTPlayer(CustomModel):

    def __repr__(self):
        return (f"<{self.__class__.__name__} object - "
                f"{getattr(self, 'first_name')} {getattr(self, 'last_name')} ({getattr(self, 'id')})>")

class HTLightPlayer(BaseHTPlayer, RequestPlayers, PlayersViewTeamPlayerItem):
    """
    Hattrick Player (light version)
    """

    # not used for fetching data, but to allow url property to work correctly
    _r_id = HTInitVar(param='PlayerID', init_arg='id_', fill_with='id')

    XML_PREFIX = 'Team/PlayerList/Player/'

    def _pre_init(self, id_, **kwargs):
        self.XML_FILTER=f".[PlayerID='{id_}']/"

    def details(self) -> 'HTPlayer':
        return self._chpp.player(id_=self.id)

class HTPlayer(BaseHTPlayer, PlayerDetails):
    """
    Hattrick Player
    """
