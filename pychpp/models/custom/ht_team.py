from datetime import datetime
from typing import List, Optional

from pychpp.models.ht_field import HTProxyField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.xml.team_details import BaseTeamDetails, TeamItem, TeamDetails, TeamItemPowerRating, \
    TeamItemLeagueLevelUnit, TeamItemFanClub, TeamItemGuestbook, TeamItemPressAnnouncement, TeamItemColors, \
    TeamItemBotStatus, TeamItemFlags, TeamItemTrophyItem, TeamItemSupportedTeams, TeamItemSupporters
from pychpp.models.custom import ht_youth_team, ht_player, ht_user, ht_arena, ht_region, ht_league_unit, CustomModel


class HTTeam(BaseTeamDetails, CustomModel):

    XML_PREFIX = 'Teams/Team/'
    XML_FILTER = ''
    URL_PATH = "/Club/"

    _r_team_id: Optional[int] = HTInitVar('teamID', init_arg='team_id', fill_with='id')

    id: int = HTProxyField(TeamItem)
    name: str = HTProxyField(TeamItem)
    short_name: str = HTProxyField(TeamItem)
    is_primary_club: bool = HTProxyField(TeamItem)
    founded_date: datetime = HTProxyField(TeamItem)
    # league: 'TeamItemLeague' = HTField('League')
    # country: 'TeamItemCountry' = HTField('Country')
    # trainer: 'TeamItemTrainer' = HTField('Trainer')
    homepage: str = HTProxyField(TeamItem)
    # cup: 'TeamItemCup' = HTField('Cup')
    power_rating: 'TeamItemPowerRating' = HTProxyField(TeamItem)
    friendly_team_id: int = HTProxyField(TeamItem)
    number_of_victories: int = HTProxyField(TeamItem)
    number_of_undefeated: int = HTProxyField(TeamItem)
    fan_club: 'TeamItemFanClub' = HTProxyField(TeamItem)
    logo_url: str = HTProxyField(TeamItem)
    guestbook: Optional['TeamItemGuestbook'] = HTProxyField(TeamItem)
    press_announcement: Optional['TeamItemPressAnnouncement'] = HTProxyField(TeamItem)
    colors: Optional['TeamItemColors'] = HTProxyField(TeamItem)
    dress_uri: str = HTProxyField(TeamItem)
    dress_alternate_uri: str = HTProxyField(TeamItem)
    bot_status: 'TeamItemBotStatus' = HTProxyField(TeamItem)
    team_rank: int = HTProxyField(TeamItem)
    youth_team_id: int = HTProxyField(TeamItem)
    youth_team_name: str = HTProxyField(TeamItem)
    number_of_visits: int = HTProxyField(TeamItem)
    flags: Optional['TeamItemFlags'] = HTProxyField(TeamItem)
    trophies: List['TeamItemTrophyItem'] = HTProxyField(TeamItem)
    supported_teams: Optional['TeamItemSupportedTeams'] = HTProxyField(TeamItem)
    supporters: Optional['TeamItemSupporters'] = HTProxyField(TeamItem)
    possible_to_challenge_midweek: bool = HTProxyField(TeamItem)
    possible_to_challenge_weekend: bool = HTProxyField(TeamItem)

    user_id: int = HTProxyField(TeamDetails, 'user.id', xml_prefix='../../')
    arena_id: int = HTProxyField(TeamItem, 'arena.id')
    region_id: int = HTProxyField(TeamItem, 'region.id')
    league_unit_id: int = HTProxyField(TeamItem, 'league_level_unit.id')

    def _pre_init(self, team_id=None, **kwargs):
        if team_id is not None:
            self.XML_FILTER=f".[TeamID='{team_id}']/"
        else:
            self.XML_FILTER=f".[IsPrimaryClub='True']/"

    @property
    def is_bot(self) -> bool:
        return self.bot_status.is_bot

    def arena(self) -> ht_arena.HTArena:
        return self._chpp.arena(id_=self.arena_id)

    def league_unit(self) -> ht_league_unit.HTLeagueUnit:
        return self._chpp.league_unit(id_=self.league_unit_id)

    def players(self) -> 'List[ht_player.HTLightPlayer]':
        xml_players = self._chpp.xml_players(team_id=self.id)
        return [self._chpp.light_player(team_id=self.id, id_=p.id, data=xml_players._data)
                for p in xml_players.team.players]

    def region(self) -> 'ht_region.HTRegion':
        return self._chpp.region(id_=self.region_id)

    def user(self) -> 'ht_user.HTUser':
        return self._chpp.user(id_=self.user_id)

    def youth_team(self) -> 'ht_youth_team.HTYouthTeam':
        return (self._chpp.youth_team(id_=self.youth_team_id)
                if self.youth_team_id is not None else None)
