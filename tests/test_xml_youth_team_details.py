from pychpp.models.xml.youth_team_details import YouthTeamDetails


def test_get_youth_team_without_league(mocked_chpp):

    ytd = mocked_chpp.xml_youth_team_details(3147468, version='1.2')

    assert isinstance(ytd, YouthTeamDetails)
    assert ytd.league.id is None


def test_youth_team_details_version_1_5(mocked_chpp):

    ytd = mocked_chpp.xml_youth_team_details(youth_team_id=2942691, version='1.5')

    assert isinstance(ytd, YouthTeamDetails)
    assert ytd.id == 2942691
    assert ytd.name == 'Les Petits Chapelains'
    assert ytd.user_id == 1728698
    assert ytd.gender_id == 1
    assert ytd.league_system_id == 1
    assert ytd.is_playing_match is False
    assert ytd.league.id == 225490
    assert ytd.league.name == 'Robaphipie League'
    assert ytd.league.status == 3
