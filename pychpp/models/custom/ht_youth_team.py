from datetime import datetime
from typing import TYPE_CHECKING, List

from pychpp.models.ht_field import HTProxyField
from pychpp.models.xml import youth_team_details as ytd
from pychpp.models.custom import CustomModel

if TYPE_CHECKING:
    from pychpp.models.custom import ht_team, ht_user, ht_youth_player


class HTYouthTeam(ytd.BaseYouthTeamDetails, CustomModel):
    """
    Hattrick Youth Team
    """

    URL_PATH = '/Club/Youth/'

    id: int = HTProxyField(ytd.YouthTeamDetails, 'id')
    name: str = HTProxyField(ytd.YouthTeamDetails, 'name')
    short_name: str = HTProxyField(ytd.YouthTeamDetails, 'short_name')
    created_date: datetime = HTProxyField(ytd.YouthTeamDetails, 'created_date')
    arena: 'ytd.Arena' = HTProxyField(ytd.YouthTeamDetails, 'arena')

    user_id: int = HTProxyField(ytd.YouthTeamDetails, 'user_id')
    senior_team_id: int = HTProxyField(ytd.YouthTeamDetails, 'owning_team.id')
    league_id: int = HTProxyField(ytd.YouthTeamDetails, 'league.id')

    def players(self) -> 'List[ht_youth_player.HTLightYouthPlayer]':
        xml_players = self._chpp.xml_youth_player_list(youth_team_id=self.id)
        return [self._chpp.light_youth_player(youth_team_id=self.id, id_=p.id, data=xml_players._data)
                for p in xml_players.list]

    def senior_team(self) -> 'ht_team.HTTeam':
        return self._chpp.team(id=self.senior_team_id)

    def user(self) -> 'ht_user.HTUser':
        return self._chpp.user(id=self.user_id)