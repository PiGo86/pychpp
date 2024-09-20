from pychpp.models.xml.world_details import WorldDetails, LeagueItem, LeagueItemCountry, LeagueItemCupItem
from .fixtures import chpp

def test_get_world_details(chpp):
    portugal_details = chpp.xml_world_details(league_id=25, include_regions=True)

    assert isinstance(portugal_details, WorldDetails)
    assert isinstance(portugal_details.leagues[0], LeagueItem)
    assert isinstance(portugal_details.leagues[0].country, LeagueItemCountry)
    assert isinstance(portugal_details.leagues[0].cups[0], LeagueItemCupItem)

    assert len(portugal_details.leagues) == 1

    world_details = chpp.xml_world_details()

    assert len(world_details.leagues) > 1
    assert world_details.leagues[0].country.regions == []
