from pychpp.fixtures.ht_datetime import HTDatetime


def test_ladder_list(mocked_chpp):

    xml_ladders = mocked_chpp.xml_ladder_list(team_id=964324)

    ladders = xml_ladders.ladders
    assert isinstance(ladders, list)

    ladder = ladders[2]
    assert ladder.id == 1255368
    assert ladder.name == 'Basse-Normandie'
    assert ladder.position == 1
    assert ladder.next_match_date == HTDatetime.from_calendar(2024, 7, 29, 17, 35, 0)
    assert ladder.wins == 20
    assert ladder.lost == 4
