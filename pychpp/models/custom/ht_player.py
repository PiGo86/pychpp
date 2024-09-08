from pychpp.models.xml.player_details import PlayerDetails
from pychpp.models.xml.players import PlayersViewTeamPlayerItem, RequestPlayers


class BaseHTPlayer:

    def __repr__(self):
        return (f"<{self.__class__.__name__} object - "
                f"{getattr(self, 'first_name')} {getattr(self, 'last_name')} ({getattr(self, 'id')})>")

class HTLightPlayer(BaseHTPlayer, RequestPlayers, PlayersViewTeamPlayerItem):
    """
    Hattrick Player (light version)
    """
    XML_PREFIX = 'Team/PlayerList/Player/'

    def _pre_init(self, id_, **kwargs):
        self.XML_FILTER=f".[PlayerID='{id_}']/"

    def details(self) -> 'HTPlayer':
        return self._chpp.player(id_=self.id)

class HTPlayer(BaseHTPlayer, PlayerDetails):
    """
    Hattrick Player
    """
