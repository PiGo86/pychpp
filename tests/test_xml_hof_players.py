"""Tests for the `hofplayers.xml` CHPP file parsing."""

from pychpp.fixtures.ht_datetime import HTDatetime


def test_hof_players(mocked_chpp):
    hof = mocked_chpp.xml_hof_players(team_id=1750803, version='1.2')

    players = hof.players
    assert isinstance(players, list)

    p = players[0]
    assert p.id == 426606995
    assert p.first_name == 'Claus Christoph'
    assert p.nick_name is None
    assert p.last_name == 'Lewandowski'
    assert p.age == 42
    assert p.next_birthday == HTDatetime.from_calendar(2024, 10, 26)
    assert p.country_id == 3
    assert p.arrival_date == HTDatetime.from_calendar(2020, 5, 7, 22, 48)
    assert p.expert_type == 12
    assert p.hof_date == HTDatetime.from_calendar(2024, 4, 17, 12, 1)
    assert p.hof_age == 41

    # fields added in 1.3 are not available
    assert p.matches_in_club is None
    assert p.best_performance_value is None
    assert p.no_of_times_training_match_hero is None
    assert p.faithful_to_the_club is None
    assert p.no_of_clean_sheet is None


def test_hof_players_version_1_3(mocked_chpp):
    hof = mocked_chpp.xml_hof_players(team_id=1750803, version='1.3')

    players = hof.players
    assert len(players) == 10

    p = players[0]
    assert p.id == 415400436
    assert p.first_name == 'Henning'
    assert p.nick_name is None
    assert p.last_name == 'Eisgruber'
    assert p.age == 54
    assert p.next_birthday == HTDatetime.from_calendar(2027, 2, 3)
    assert p.country_id == 3
    assert p.arrival_date == HTDatetime.from_calendar(2019, 7, 1, 20, 10)
    assert p.expert_type == 1
    assert p.hof_date == HTDatetime.from_calendar(2023, 12, 6, 8, 15)
    assert p.hof_age == 44

    # fields added in 1.3 (only shown when the team has Gold supporter)
    assert p.matches_in_club == 161
    assert p.best_performance_value == 9.0
    assert p.no_of_times_training_match_hero == 2
    assert p.faithful_to_the_club == 1619
    assert p.no_of_clean_sheet == 0
