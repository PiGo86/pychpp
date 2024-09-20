from typing import List

from pychpp.models.custom.base.ht_arena import HTLightArena
from pychpp.models.custom.base.ht_league import HTLightLeague
from pychpp.models.custom.base.ht_region import HTLightRegion
from pychpp.models.custom.base.ht_team import HTLightTeam, HTLightYouthTeam
from pychpp.models.custom.base.ht_user import BaseHTUser
from pychpp.models.ht_field import HTProxyField
from pychpp.models.xml import manager_compendium as mc


class HTUser(mc.ManagerCompendium, BaseHTUser):
    """
    Hattrick user
    """
    username: str = HTProxyField(mc.ManagerCompendium, attr_name='login_name')
    teams: List['HTUserTeam'] = HTProxyField(mc.ManagerCompendium)


class HTUserTeam(mc.TeamItem, HTLightTeam):
    arena: 'HTUserTeamArena' = HTProxyField(mc.TeamItem)
    league: 'HTUserTeamLeague' = HTProxyField(mc.TeamItem)
    region: 'HTUserTeamRegion' = HTProxyField(mc.TeamItem)
    youth_team: 'HTUserTeamYouthTeam' = HTProxyField(mc.TeamItem)


class HTUserTeamArena(mc.TeamItemArena, HTLightArena):
    pass


class HTUserTeamLeague(mc.TeamItemLeague, HTLightLeague):
    pass


class HTUserTeamRegion(mc.TeamItemRegion, HTLightRegion):
    pass


class HTUserTeamYouthTeam(mc.TeamItemYouthTeam, HTLightYouthTeam):
    pass
