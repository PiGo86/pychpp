from pychpp.models.xml.league_fixtures import LeagueFixtures, MatchItem


def test_get_league_fixtures(mocked_chpp):
    l_fixtures = mocked_chpp.xml_league_fixtures(league_level_unit_id=36378, season=76)

    assert isinstance(l_fixtures, LeagueFixtures)
    assert l_fixtures.id == 36378
    assert l_fixtures.season == 76
    assert l_fixtures.name == "VI.390"

    assert isinstance(l_fixtures.matches, list)
    assert len(l_fixtures.matches) == 56
    assert isinstance(l_fixtures.matches[10], MatchItem)
