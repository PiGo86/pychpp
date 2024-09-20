from pychpp.models.custom import CustomModel
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.xml.player_details import PlayerDetails
from pychpp.models.xml.players import PlayersViewTeamPlayerItem, RequestPlayers
from pychpp.models.xml.youth_player_details import YouthPlayerDetails
from pychpp.models.xml.youth_player_list import YouthPlayerListList, YouthPlayerListListPlayerItem, \
    RequestYouthPlayerList


class BaseHTYouthPlayer(CustomModel):

    URL_PATH = '/Club/Players/YouthPlayer.aspx'

    def __repr__(self):
        return (f"<{self.__class__.__name__} object - "
                f"{getattr(self, 'first_name')} {getattr(self, 'last_name')} ({getattr(self, 'id')})>")


class HTLightYouthPlayer(BaseHTYouthPlayer, RequestYouthPlayerList, YouthPlayerListListPlayerItem):
    """
    Hattrick Youth Player - Light
    """
    XML_PREFIX = 'PlayerList/YouthPlayer/'

    # not used for fetching data, but to allow url property to work correctly
    _r_id = HTInitVar(param='youthPlayerId', init_arg='id_', fill_with='id')

    def _pre_init(self, id_, **kwargs):
        self.XML_FILTER=f".[YouthPlayerID='{id_}']/"

    def details(self) -> 'HTYouthPlayer':
        return self._chpp.youth_player(id_=self.id)

class HTYouthPlayer(BaseHTYouthPlayer, YouthPlayerDetails):
    """
    Hattrick Youth Player
    """
