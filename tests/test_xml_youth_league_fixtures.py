from pychpp.fixtures.ht_datetime import HTDatetime


def test_youth_league_fixtures(mocked_chpp):

    ylf = mocked_chpp.xml_youth_league_fixtures(
        youth_league_id=251460,
        season=91,
    )

    assert ylf.id == 251460
    assert ylf.name == 'Liga juniorów'
    assert ylf.type == 3
    assert ylf.season == 91
    assert ylf.last_match_round == 14
    assert ylf.nr_of_teams_in_league == 12

    match_ = ylf.matches[0]
    assert match_.id == 135854949
    assert match_.round == 1
    assert match_.status == 'FINISHED'
    assert match_.home_team.id == 2917550
    assert match_.home_team.name == 'RANDALL'
    assert match_.away_team.id == 2749554
    assert match_.away_team.name == 'NK Alcatraz'
    assert match_.date == HTDatetime.from_calendar(2024, 7, 26, 17, 25)
    assert match_.home_goals == 3
    assert match_.away_goals == 2
