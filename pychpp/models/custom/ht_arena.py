from pychpp.models.ht_field import HTProxyField
from pychpp.models.xml.arena_details import CurrentCapacity
from pychpp.models.xml.arena_details import ExpandedCapacity
from pychpp.models.xml.arena_details import RequestArenaDetails, ArenaDetails
from pychpp.models.custom import ht_team, ht_region


class HTArena(RequestArenaDetails):
    """
    Hattrick Arena
    """
    id: int = HTProxyField(ArenaDetails, 'id')
    name: str = HTProxyField(ArenaDetails, 'name')
    image: str = HTProxyField(ArenaDetails, 'image')
    fallback_image: str = HTProxyField(ArenaDetails, 'fallback_image')
    current_capacity: 'CurrentCapacity' = HTProxyField(ArenaDetails, 'current_capacity')
    expanded_capacity: 'ExpandedCapacity' = HTProxyField(ArenaDetails, 'expanded_capacity')

    _team_id: int = HTProxyField(ArenaDetails, 'team.id')
    _league_id: int = HTProxyField(ArenaDetails, 'league.id')
    _region_id: int = HTProxyField(ArenaDetails, 'region.id')

    def team(self, **kwargs):
        return ht_team.HTTeam(self._chpp, team_id=self._team_id, **kwargs)

    def region(self, **kwargs):
        return ht_region.HTRegion(self._chpp, region_id=self._region_id, **kwargs)
