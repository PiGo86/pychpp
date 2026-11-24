"""High-level custom model built on top of the xml models."""

from typing import Any, List, Optional

from pychpp.models.custom.base.ht_arena import HTLightArena
from pychpp.models.custom.base.ht_country import HTLightCountry
from pychpp.models.custom.base.ht_league import HTLightLeague
from pychpp.models.custom.base.ht_league_unit import HTLightLeagueUnit
from pychpp.models.custom.base.ht_player import HTLightPlayer
from pychpp.models.custom.base.ht_region import HTLightRegion
from pychpp.models.custom.base.ht_team import BaseHTTeam, HTLightYouthTeam
from pychpp.models.custom.base.ht_user import HTLightUser
from pychpp.models.ht_field import HTProxyField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.xml.players import PlayersViewTeamPlayerItem, PlayersViewTeam, RequestPlayers
from pychpp.models.xml import team_details as td


class HTTeam(td.RequestTeamDetails, td.TeamItem, BaseHTTeam):
    """Hattrick team.

    Args:
        team_id: Hattrick ID of the team. If None, the primary team is used.

    Attributes:
        id: Hattrick ID of the team.
        name: Name of the team.
        user: User owning the team.
        arena: Arena of the team.
        league: League of the team.
        country: Country of the team.
        region: Region of the team.
        league_unit: League unit of the team.
        youth_team: Youth team of the team.

    """

    XML_PREFIX = 'Teams/Team/'
    XML_FILTER = ''

    _r_team_id: Optional[int] = HTInitVar('teamID', init_arg='team_id', fill_with='id')

    user: 'HTTeamUser' = HTProxyField(td.TeamDetails, xml_prefix='../../')
    arena: 'HTTeamArena' = HTProxyField(td.TeamItem)
    league: 'HTTeamLeague' = HTProxyField(td.TeamItem)
    country: 'HTTeamCountry' = HTProxyField(td.TeamItem)
    region: 'HTTeamRegion' = HTProxyField(td.TeamItem)
    league_unit: 'HTTeamLeagueUnit' = HTProxyField(td.TeamItem, 'league_level_unit')
    youth_team: 'HTTeamYouthTeam' = HTProxyField(td.TeamItem)

    def __init__(self, team_id: Optional[int]=None, **kwargs: Any):
        if team_id is not None:
            self.XML_FILTER = f".[TeamID='{team_id}']/"
        else:
            self.XML_FILTER = ".[IsPrimaryClub='True']/"
        super().__init__(team_id=team_id, **kwargs)

    @property
    def is_bot(self) -> bool:
        """Whether the team is a bot."""
        return self.bot_status.is_bot

    def players(self) -> 'List[HTTeamPlayersItem]':
        """Get the players of the team."""
        return HTTeamPlayers(chpp=self._chpp, team_id=self.id).list


class HTTeamUser(HTLightUser, td.User):
    """User owning the team."""
    username: str = HTProxyField(td.User, 'login_name')


class HTTeamArena(HTLightArena, td.TeamItemArena):
    """Arena of the team."""
    pass


class HTTeamLeague(HTLightLeague, td.TeamItemLeague):
    """League of the team."""
    pass


class HTTeamCountry(HTLightCountry, td.TeamItemCountry):
    """Country of the team."""
    pass


class HTTeamRegion(HTLightRegion, td.TeamItemRegion):
    """Region of the team."""
    pass


class HTTeamLeagueUnit(HTLightLeagueUnit, td.TeamItemLeagueLevelUnit):
    """League unit of the team."""
    pass


class HTTeamYouthTeam(HTLightYouthTeam, td.TeamItemYouthTeam):
    """Youth team of the team."""
    pass


class HTTeamPlayers(RequestPlayers, PlayersViewTeam):
    """Players list of a team."""
    XML_PREFIX = 'Team/'
    list: List['HTTeamPlayersItem'] = HTProxyField(PlayersViewTeam, 'players')


class HTTeamPlayersItem(HTLightPlayer, PlayersViewTeamPlayerItem):
    """Hattrick light player for team."""
