from pychpp.fixtures.ht_datetime import HTDatetime


def test_ladder_details(mocked_chpp):
    xml_ladder = mocked_chpp.xml_ladder_details(ladder_id=1257867, page_index=0)

    ladder = xml_ladder.ladder
    assert ladder.id == 1257867
    assert ladder.name == 'France'
    assert ladder.num_of_teams == 1_095
    assert ladder.page_size == 25
    assert ladder.page_index == 0
    assert ladder.king_team_id == 964324
    assert ladder.king_team_name == 'Malherbe United II'
    assert ladder.king_since == HTDatetime.from_calendar(2024, 10, 15, 17, 40)

    teams = ladder.teams
    assert isinstance(teams, list)

    team = teams[1]
    assert team.id == 17889051
    assert team.name == 'W.S.D.'
    assert team.position == 2
    assert team.wins == 38
    assert team.lost == 3
    assert team.wins_in_a_row == 2
    assert team.lost_in_a_row == 0
