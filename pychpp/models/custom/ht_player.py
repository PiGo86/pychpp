from pychpp.models.custom.base.ht_player import BaseCommonHTPlayer, HTAge
from pychpp.models.ht_field import HTProxyField, HTField
from pychpp.models.xml.player_details import PlayerDetails


class HTPlayer(BaseCommonHTPlayer, PlayerDetails):
    """
    Hattrick Player
    """
    URL_PATH = '/Club/Players/Player.aspx'

    age_years: int = HTProxyField(PlayerDetails, 'age')
    age_days: int = HTProxyField(PlayerDetails)
    age: 'HTPlayerAge' = HTField('.',
                                 suppl_attrs={
                                     'years': 'age_years',
                                     'days': 'age_days',
                                 })


class HTPlayerAge(HTAge):
    """
    Hattrick Player -> Age
    """
