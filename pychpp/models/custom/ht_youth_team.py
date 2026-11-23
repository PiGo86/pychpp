"""High-level custom model built on top of the xml models."""

from datetime import datetime
from typing import TYPE_CHECKING, List

from pychpp.models.custom.base.ht_player import HTLightYouthPlayer
from pychpp.models.ht_field import HTProxyField
from pychpp.models.xml import youth_team_details as ytd
from pychpp.models.custom import CustomModel
from pychpp.models.xml.youth_player_list import YouthPlayerListListPlayerItem, \
    YouthPlayerListList

if TYPE_CHECKING:
    from pychpp.models.custom import ht_team, ht_user


class HTYouthTeam(ytd.RequestYouthTeamDetails, CustomModel):
    """Hattrick Youth Team."""

    URL_PATH = '/Club/Youth/'

    id: int = HTProxyField(ytd.YouthTeamDetails, 'id')
    name: str = HTProxyField(ytd.YouthTeamDetails, 'name')
    short_name: str = HTProxyField(ytd.YouthTeamDetails, 'short_name')
    created_date: datetime = HTProxyField(ytd.YouthTeamDetails, 'created_date')
    arena: 'ytd.Arena' = HTProxyField(ytd.YouthTeamDetails, 'arena')

    user_id: int = HTProxyField(ytd.YouthTeamDetails, 'user_id')
    senior_team_id: int = HTProxyField(ytd.YouthTeamDetails, 'owning_team.id')
    league_id: int = HTProxyField(ytd.YouthTeamDetails, 'league.id')

    def players(self) -> List[YouthPlayerListListPlayerItem]:
        """Get the players of the youth team."""
        xml_players = HTYouthTeamPlayers(chpp=self._chpp,
                                         youth_team_id=self.id)
        return xml_players.list

    def senior_team(self) -> 'ht_team.HTTeam':
        """Get the senior team owning this youth team."""
        return self._chpp.team(id=self.senior_team_id)

    def user(self) -> 'ht_user.HTUser':
        """Get the user owning this youth team."""
        return self._chpp.user(id=self.user_id)


class HTYouthTeamPlayers(YouthPlayerListList):
    """Players list of a youth team."""
    list: List['HTYouthTeamPlayerItem'] = HTProxyField(YouthPlayerListList)


class HTYouthTeamPlayerItem(HTLightYouthPlayer, YouthPlayerListListPlayerItem):
    """Hattrick light player for youth team."""
