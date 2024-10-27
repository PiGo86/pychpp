def test_tournament_league_tables(mocked_chpp):

    tlt = mocked_chpp.xml_tournament_league_tables(5292015)

    assert tlt.id == 5292015
    assert tlt.season == 20

    lt = tlt.tournament_league_tables[0]
    assert lt.group_id == 1

    team = lt.teams[0]
    assert team.id == 1164474
    assert team.name == 'FC BIG JIM'
    assert team.position == 1
    assert team.position_change == 0
    assert team.matches == 5
    assert team.goals_for == 26
    assert team.goals_against == 1
    assert team.won == 5
    assert team.draws == 0
    assert team.lost == 0
