from pychpp.fixtures.ht_datetime import HTDatetime


def test_national_team_matches(mocked_chpp):

    nt_matches = mocked_chpp.xml_national_team_matches()

    assert nt_matches.user_supporter_tier == 'none'
    assert nt_matches.league_office_type_id == 2

    match_ = nt_matches.matches[0]

    assert match_.id == 35352649
    assert match_.date == HTDatetime.from_calendar(2024, 10, 25, 20)
    assert match_.type == 10
    assert match_.context_id == 5001319
    assert match_.home_team_id == 3312
    assert match_.home_team_name == 'Puerto Rico'
    assert match_.away_team_id == 3298
    assert match_.away_team_name == 'Ītyōṗṗyā'
    assert match_.match_result.home_goals == 1
    assert match_.match_result.away_goals == 2
