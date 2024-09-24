from pychpp.models.custom.base.ht_player import BaseCommonHTPlayer
from pychpp.models.custom.base.ht_player import HTYouthPlayerSkills
from pychpp.models.ht_field import HTProxyField
from pychpp.models.xml.youth_player_details import YouthPlayerDetails


class HTYouthPlayer(BaseCommonHTPlayer, YouthPlayerDetails):
    """
    Hattrick Youth Player
    """
    URL_PATH = '/Club/Players/YouthPlayer.aspx'

    skills: 'HTYouthPlayerSkills' = HTProxyField(YouthPlayerDetails)
