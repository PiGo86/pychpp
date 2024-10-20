from pychpp.fixtures.ht_datetime import HTDatetime


def test_hof_players(mocked_chpp):

    hof = mocked_chpp.xml_hof_players(team_id=1750803)

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
