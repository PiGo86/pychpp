from pychpp.fixtures.ht_datetime import HTDatetime


def test_match_orders(mocked_chpp):

    mo = mocked_chpp.xml_match_orders(match_id=739349000)

    assert mo.id == 739349000
    assert mo.source_system == 'Hattrick'

    assert mo.match_data.home_team.id == 1751435
    assert mo.match_data.home_team.name == 'Kermouster Atlethic Club 2'
    assert mo.match_data.away_team.id == 1165592
    assert mo.match_data.away_team.name == 'Les Poitevins de La Chapelle'
    assert mo.match_data.arena.id == 1747997
    assert mo.match_data.arena.name == 'La routourne'
    assert mo.match_data.date == HTDatetime.from_calendar(2024, 10, 26, 21)
    assert mo.match_data.type == 1
    assert mo.match_data.attitude == 0
    assert mo.match_data.tactic_type == 0
    assert mo.match_data.coach_modifier == 0

    pos = mo.match_data.lineup.positions[0]
    assert pos.id == 414086970
    assert pos.role_id == 100
    assert pos.first_name == 'Joseph'
    assert pos.nick_name is None
    assert pos.last_name == 'Chevalier'
    assert pos.behaviour == 0

    ben = mo.match_data.lineup.bench[0]
    assert ben.id == 430759322
    assert ben.role_id == 200
    assert ben.first_name == 'Frédérik'
    assert ben.nick_name is None
    assert ben.last_name == 'Rivière'

    kicker = mo.match_data.lineup.kickers[0]
    assert kicker.id == 0
    assert kicker.role_id == 22
