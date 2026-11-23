"""Tests for the `youthleaguedetails.xml` CHPP file parsing."""

def test_youth_league_details(mocked_chpp):
    yld = mocked_chpp.xml_youth_league_details(version='1.0')

    assert yld.id == 225490
    assert yld.name == 'Robaphipie League'
    assert yld.type == 3
    assert yld.season == 130
    assert yld.last_match_round == 0
    assert yld.nr_of_teams_in_league == 4

    team = yld.teams[0]
    assert team.id == 499165
    assert team.name == 'Jena West II'
    assert team.position == 1
    assert team.position_change == 0
    assert team.matches == 0
    assert team.goals_for == 0
    assert team.goals_against == 0
    assert team.points == 0
    assert team.won == 0
    assert team.draws == 0
    assert team.lost == 0


def test_youth_league_details_version_1_1(mocked_chpp):
    yld = mocked_chpp.xml_youth_league_details(version='1.1')

    assert yld.id == 225490
    assert yld.name == 'Robaphipie League'
    assert yld.league_system_id == 1
    assert yld.nr_of_teams_in_league == 4
    assert len(yld.teams) == 4

    team = yld.teams[0]
    assert team.id == 3295934
    assert team.name == 'santa rita'
    assert team.position == 1
