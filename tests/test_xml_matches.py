from pychpp.fixtures.ht_datetime import HTDatetime


def test_xml_matches(mocked_chpp):

    xml_matches = mocked_chpp.xml_matches()

    team = xml_matches.team
    assert team.id == 1165592
    assert team.name == 'Les Poitevins de La Chapelle'
    assert team.short_name == 'Poitevins'
    assert team.league.id == 5
    assert team.league.name == 'France'
    assert team.league_level_unit.id == 36777
    assert team.league_level_unit.name == 'VI.789'
    assert team.league_level_unit.level == 6

    matches = team.matches
    assert isinstance(matches, list)

    match = matches[0]
    assert match.id == 739348986
    assert match.home_team.id == 2165975
    assert match.home_team.name == 'diable noir'
    assert match.home_team.short_name == 'diable'
    assert match.away_team.id == 1165592
    assert match.away_team.name == 'Les Poitevins de La Chapelle'
    assert match.away_team.short_name == 'Poitevins'
    assert match.date == HTDatetime.from_calendar(2024, 9, 28, 21, 0, 0)
    assert match.source_system == 'Hattrick'
    assert match.type == 1
    assert match.context_id == 36777
    assert match.cup_level == 0
    assert match.cup_level_index == 0
    assert match.home_goals == 1
    assert match.away_goals == 6
    assert match.status == 'FINISHED'
