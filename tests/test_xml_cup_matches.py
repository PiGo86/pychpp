from pychpp.ht_datetime import HTDatetime


def test_get_hattrick_masters_matches(mocked_chpp):

    hm = mocked_chpp.xml_cup_matches(183, season=88, cup_round=6)

    assert hm.id == 183
    assert hm.season == 88
    assert hm.round == 6
    assert hm.name == 'Hattrick Masters'
    assert isinstance(hm.match_list, list)

    hm_match = hm.match_list[2]
    assert hm_match.id == 736551978
    assert hm_match.date == HTDatetime.from_calendar(2024, 7, 11, 20, 0, 0)
    assert hm_match.home_team.id == 305963
    assert hm_match.home_team.name == 'Dude Linz'
    assert hm_match.away_team.id == 1850457
    assert hm_match.away_team.name == 'Awesenal'
    assert hm_match.match_result.available is True
    assert hm_match.match_result.home_goals == 3
    assert hm_match.match_result.away_goals == 5
    assert hm_match.league_info.available is True
    assert hm_match.league_info.home_league.id == 39
    assert hm_match.league_info.home_league.name == 'Österreich'
    assert hm_match.league_info.away_league.id == 34
    assert hm_match.league_info.away_league.name == 'China'
