import pytest

from pychpp.models.xml.national_team_details import NationalTeamDetails
from pychpp.ht_error import HTUnknownTeamIdError


def test_get_nt_details(mocked_chpp):
    portugal_details = mocked_chpp.xml_national_team_details(team_id=3014)

    assert isinstance(portugal_details, NationalTeamDetails)

    assert portugal_details.id == 3014
    assert portugal_details.league.id == 25
    assert portugal_details.league.name == "Portugal"
    assert portugal_details.name == "Portugal"


def test_get_nonexistent_nt(chpp):
    with pytest.raises(HTUnknownTeamIdError):
        chpp.xml_national_team_details(team_id=1000000)
