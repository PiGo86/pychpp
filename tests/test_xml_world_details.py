"""Tests for the `worlddetails.xml` CHPP file parsing."""

from pychpp.models.xml.world_details import (WorldDetails, LeagueItem,
                                             LeagueItemCountry, LeagueItemCupItem)


def test_get_world_details(mocked_chpp):
    portugal_details = mocked_chpp.xml_world_details(league_id=25, include_regions=True,
                                                     version='1.9')

    assert isinstance(portugal_details, WorldDetails)
    assert isinstance(portugal_details.leagues[0], LeagueItem)
    assert isinstance(portugal_details.leagues[0].country, LeagueItemCountry)
    assert isinstance(portugal_details.leagues[0].cups[0], LeagueItemCupItem)

    assert len(portugal_details.leagues) == 1

    world_details = mocked_chpp.xml_world_details(version='1.9')

    assert len(world_details.leagues) > 1
    assert world_details.leagues[0].country.regions == []


def test_world_details_version_2_1(mocked_chpp):
    portugal_details = mocked_chpp.xml_world_details(league_id=25, version='2.1')

    assert isinstance(portugal_details, WorldDetails)
    assert len(portugal_details.leagues) == 1

    league = portugal_details.leagues[0]
    assert league.id == 25
    assert league.name == "Portugal"
    assert league.league_system_id == 1
    assert league.total_teams == 10920
    assert league.number_of_foreign_owners == 36
    assert league.max_percentage_of_foreign_owners == 50
