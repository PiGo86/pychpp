from pychpp.models.custom.base.ht_arena import BaseHTArena
from pychpp.models.custom.base.ht_league import HTLightLeague
from pychpp.models.custom.base.ht_region import HTLightRegion
from pychpp.models.custom.base.ht_team import HTLightTeam
from pychpp.models.ht_field import HTProxyField
from pychpp.models.xml import arena_details


class HTArena(arena_details.ArenaDetailsDefault, BaseHTArena):
    """
    Hattrick Arena
    """
    team: 'HTArenaTeam' = HTProxyField(arena_details.ArenaDetailsDefault)
    league: 'HTArenaLeague' = HTProxyField(arena_details.ArenaDetailsDefault)
    region: 'HTArenaRegion' = HTProxyField(arena_details.ArenaDetailsDefault)


class HTArenaTeam(arena_details.Team, HTLightTeam):
    pass


class HTArenaLeague(arena_details.League, HTLightLeague):
    pass


class HTArenaRegion(arena_details.Region, HTLightRegion):
    pass
