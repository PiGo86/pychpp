"""High-level custom model built on top of the xml models."""

from pychpp.models.custom.base.ht_player import BaseCommonHTPlayer, HTAge
from pychpp.models.ht_field import HTProxyField, HTField
from pychpp.models.xml.player_details import PlayerDetails


class HTPlayer(BaseCommonHTPlayer, PlayerDetails):
    """Hattrick player.

    Attributes:
        id: Hattrick ID of the player.
        first_name: First name of the player.
        last_name: Last name of the player.
        age: Age of the player (HTPlayerAge object).
        age_years: Age of the player, in years.
        age_days: Age of the player, in days.

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
    """Hattrick Player -> Age."""
