from pychpp.models.xml.national_teams import NationalTeams, NationalTeamItem


def test_get_nts(mocked_chpp):
    national_teams = mocked_chpp.xml_national_teams(league_office_type_id=2)

    assert isinstance(national_teams, NationalTeams)
    assert len(national_teams.national_teams) > 0

    portugal_entry = list(
        filter(lambda k: k.id == 3014, national_teams.national_teams)
    )[0]
    assert isinstance(portugal_entry, NationalTeamItem)
    assert portugal_entry.id == 3014
    assert portugal_entry.name == "Portugal"
