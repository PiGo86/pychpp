import re

from pychpp.models.xml.world_details import LeagueItemCountryRegionItem

from .conftest import COUNTRY_LEAGUE_PATTERN, REGION_PATTERN


def test_get_league(chpp):

    portugal_league = chpp.league(25, include_regions=True)

    assert portugal_league.name == "Portugal"
    assert portugal_league.id == 25
    assert portugal_league.country.name == "Portugal"

    portugal_regions = portugal_league.country.regions
    assert len(portugal_regions) >= 1
    assert isinstance(portugal_regions[0], LeagueItemCountryRegionItem)

    assert len(portugal_league.cups) >= 1

    assert re.match(COUNTRY_LEAGUE_PATTERN, portugal_league.url)
    assert re.match(REGION_PATTERN, portugal_regions[0].url)
    # assert re.match(CUP_PATTERN, portugal_league.cups[0].url)
