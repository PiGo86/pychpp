from pychpp.models.xml.youth_team_details import YouthTeamDetails


def test_get_youth_team_without_league(mocked_chpp):

    ytd = mocked_chpp.xml_youth_team_details(3147468)

    assert isinstance(ytd, YouthTeamDetails)
    assert ytd.league.id is None
