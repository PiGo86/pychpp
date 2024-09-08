import xml.etree.ElementTree
from typing import List
from xml.etree.ElementTree import ElementTree

from pychpp.models.ht_field import HTProxyField
from pychpp.models.xml.team_details import BaseTeamDetails, TeamItem, TeamDetails
from pychpp.models.custom import ht_youth_team, ht_player, ht_user


class HTTeam(BaseTeamDetails, TeamItem):

    XML_PREFIX='Teams/Team/'
    XML_FILTER=''
    URL_PATH = "/Club"

    user_id: int = HTProxyField(TeamDetails, 'user.id', xml_prefix='../../')

    def _pre_init(self, team_id=None, **kwargs):
        if team_id is not None:
            self.XML_FILTER=f".[TeamID='{team_id}']/"
        else:
            self.XML_FILTER=f".[IsPrimaryClub='True']/"

    @property
    def is_bot(self) -> bool:
        return self.bot_status.is_bot

    def youth_team(self) -> 'ht_youth_team.HTYouthTeam':
        return (self._chpp.youth_team(id_=self.youth_team_id)
                if self.youth_team_id is not None else None)

    def players(self) -> 'List[ht_player.HTLightPlayer]':
        xml_players = self._chpp.xml_players(team_id=self.id)
        return [self._chpp.light_player(id_=p.id, data=xml_players._data) for p in xml_players.team.players]

    def user(self) -> 'ht_user.HTUser':
        return self._chpp.user(id_=self.user_id)
