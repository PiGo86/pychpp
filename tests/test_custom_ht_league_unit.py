import re

from pychpp.models.custom.ht_league_unit import HTLeagueUnit
from pychpp.models.xml.league_details import TeamItem

from .conftest import LEAGUE_LEVEL_UNIT_PATTERN


def test_league(chpp):
    league_unit = chpp.league_unit(36378)

    assert isinstance(league_unit, HTLeagueUnit)
    assert league_unit.id == 36378
    assert league_unit.name == "VI.390"
    assert league_unit.league.id == 5

    match_league_unit = re.match(LEAGUE_LEVEL_UNIT_PATTERN, league_unit.url)

    assert match_league_unit is not None
    assert int(match_league_unit.group(1)) == 36378

    assert isinstance(league_unit.teams, list)

    for r in league_unit.teams:
        assert isinstance(r, TeamItem)

    assert league_unit.teams[3].position == 4
