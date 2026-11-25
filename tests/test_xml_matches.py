"""Tests for the `matches.xml` CHPP file parsing."""

from pychpp.fixtures.ht_datetime import HTDatetime


def test_xml_matches(mocked_chpp):
    xml_matches = mocked_chpp.xml_matches(version='2.9')

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


def test_xml_matches_version_3_0(mocked_chpp):
    xml_matches = mocked_chpp.xml_matches()

    team = xml_matches.team
    assert team.id == 1165592
    assert team.name == 'Les Poitevins de La Chapelle'
    assert team.short_name == 'Poitevins'
    assert team.league.id == 5
    assert team.league.name == 'France'
    assert team.league_level_unit.id == 73592
    assert team.league_level_unit.name == 'VII.777'
    assert team.league_level_unit.level == 7

    matches = team.matches
    assert len(matches) == 9

    match = matches[0]
    assert match.id == 768781755
    assert match.home_team.id == 3360132
    assert match.home_team.name == 'SC Meaux Academy'
    assert match.home_team.short_name == 'Academy'
    assert match.away_team.id == 1165592
    assert match.away_team.name == 'Les Poitevins de La Chapelle'
    assert match.away_team.short_name == 'Poitevins'
    assert match.date == HTDatetime.from_calendar(2026, 10, 24, 21, 0, 0)
    assert match.source_system == 'Hattrick'
    assert match.type == 1
    assert match.context_id == 36881
    assert match.cup_level == 0
    assert match.cup_level_index == 0
    assert match.home_goals == 10
    assert match.away_goals == 0
    assert match.status == 'FINISHED'
    # since version 3.0
    assert match.home_statement is None
    assert match.away_statement is None
    assert match.fan_match_expectation == 4

    # FanMatchExpectation is only supplied for matches listed in fans.xml
    assert matches[3].id == 775863574
    assert matches[3].fan_match_expectation is None

    upcoming = matches[4]
    assert upcoming.id == 773525893
    assert upcoming.status == 'UPCOMING'
    assert upcoming.orders_given is False
    assert upcoming.fan_match_expectation == 5
