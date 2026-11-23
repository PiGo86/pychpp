"""Tests for the `nationalteamdetails.xml` CHPP file parsing."""

import pytest

from pychpp.models.xml.national_team_details import NationalTeamDetails
from pychpp.fixtures.ht_error import HTUnknownTeamIdError


def test_get_nt_details(mocked_chpp):
    portugal_details = mocked_chpp.xml_national_team_details(team_id=3014, version='1.9')

    assert isinstance(portugal_details, NationalTeamDetails)

    assert portugal_details.id == 3014
    assert portugal_details.league.id == 25
    assert portugal_details.league.name == "Portugal"
    assert portugal_details.name == "Portugal"


def test_get_nt_details_version_2_0(mocked_chpp):
    portugal_details = mocked_chpp.xml_national_team_details(team_id=3014, version='2.0')

    assert isinstance(portugal_details, NationalTeamDetails)

    assert portugal_details.id == 3014
    assert portugal_details.name == "Portugal"
    assert portugal_details.national_coach.id == 2766638
    assert portugal_details.national_coach.login_name == "_JPaulo_"
    assert portugal_details.assistant_coach.id == 13420564
    assert portugal_details.assistant_coach.login_name == "Biluu8"
    assert len(portugal_details.scouts) == 5
    assert portugal_details.scouts[0].id == 13439917
    assert portugal_details.scouts[0].login_name == "StefanoSoares"
    assert portugal_details.scouts[4].id == 10730860
    assert portugal_details.scouts[4].login_name == "P-Pires"


def test_get_nonexistent_nt(chpp):
    with pytest.raises(HTUnknownTeamIdError):
        chpp.xml_national_team_details(team_id=1000000)
