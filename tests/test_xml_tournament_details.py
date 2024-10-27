from pychpp.fixtures.ht_datetime import HTDatetime


def test_tournament_details(mocked_chpp):

    td = mocked_chpp.xml_tournament_details(3116071, season=23)

    assert td.id == 3116071
    assert td.name == 'Heroes of 2017 Trophy'
    assert td.type == 8
    assert td.season == 23
    assert td.logo_url == '//res.hattrick.org/tournamentlogo/generation-trophy-purple.png'
    assert td.trophy_type == 98
    assert td.number_of_teams == 2_878
    assert td.number_of_groups == 1
    assert td.last_match_round == 14
    assert td.first_match_round_date == HTDatetime.from_calendar(2024, 9, 2, 7, 5)
    assert td.next_match_round_date is None
    assert td.is_matches_ongoing is False
    assert td.creator.id == 3
    assert td.creator.login_name == 'HT-Daniel'
