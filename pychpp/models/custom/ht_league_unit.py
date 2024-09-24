from typing import List

from pychpp.models.custom.base.ht_league import HTLightLeague
from pychpp.models.custom.base.ht_league_unit import BaseHTLeagueUnit
from pychpp.models.custom.base.ht_team import HTLightTeam
from pychpp.models.ht_field import HTProxyField
from pychpp.models.xml.league_details import LeagueDetails, League, TeamItem


class HTLeagueUnit(LeagueDetails, BaseHTLeagueUnit):
    """
    Hattrick League Level Unit
    """
    id: int = HTProxyField(LeagueDetails, 'league_level_unit_id')
    name: str = HTProxyField(LeagueDetails, 'league_level_unit_name')
    league: 'HTLeagueUnitLeague' = HTProxyField(LeagueDetails)
    teams: List['HTLeagueUnitLeagueTeamItem'] = HTProxyField(LeagueDetails)


class HTLeagueUnitLeague(HTLightLeague, League):
    """
    Hattrick League Level Unit -> League
    """


class HTLeagueUnitLeagueTeamItem(HTLightTeam, TeamItem):
    """
    Hattrick League Level Unit -> Teams -> Team item
    """
