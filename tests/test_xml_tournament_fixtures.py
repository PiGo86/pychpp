"""Tests for the `tournamentfixtures.xml` CHPP file parsing."""

from pychpp.fixtures.ht_datetime import HTDatetime


def test_tournament_fixtures(mocked_chpp):
    tf = mocked_chpp.xml_tournament_fixtures(3116071, version='1.0')

    match_ = tf.matches[0]

    assert match_.id == 34922028
    assert match_.home_team_id == 2052633
    assert match_.home_team_name == 'Immersieg'
    assert match_.home_goals == 5
    assert match_.away_team_id == 2056780
    assert match_.away_team_name == 'Atlético de Sintra'
    assert match_.away_goals == 1
    assert match_.date == HTDatetime.from_calendar(2024, 9, 6, 7, 5)
    assert match_.type == 51
    assert match_.round == 9
    assert match_.group == 0
    assert match_.status == 2
    assert match_.home_statement is None
    assert match_.away_statement is None


def test_tournament_fixtures_version_1_1(mocked_chpp):
    tf = mocked_chpp.xml_tournament_fixtures(3116071, match_round=9, version='1.1')

    assert len(tf.matches) == 32
    assert all(match_.round == 9 for match_ in tf.matches)

    match_ = tf.matches[0]

    assert match_.id == 42712658
    assert match_.home_team_name == 'Club Atletico Fray Luis Beltran'
    assert match_.home_goals == 3
    assert match_.away_team_name == 'Pijaki z Jednej Paki'
    assert match_.away_goals == 0
    assert match_.date == HTDatetime.from_calendar(2026, 10, 30, 7, 5)
    assert match_.type == 51
    assert match_.round == 9
    assert match_.group == 0
    assert match_.status == 2
    assert match_.home_statement is None
    assert match_.away_statement is None
