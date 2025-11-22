from pychpp.models.custom.base.ht_player import BaseCommonHTPlayer
from pychpp.models.xml.youth_player_details import YouthPlayerDetails


class HTYouthPlayer(BaseCommonHTPlayer, YouthPlayerDetails):
    """
    Hattrick Youth Player
    """
    URL_PATH = '/Club/Players/YouthPlayer.aspx'
