import pytest

from pychpp.models.custom.ht_challenge import HTChallengeManager
from pychpp.ht_error import HTUnauthorizedAction

from .conftest import PYCHPP_SCOPE


def test_is_challengeable(chpp):

    challenge = HTChallengeManager(chpp)
    team_ids_to_test = [1750803, 299981]

    if "manage_challenges" in PYCHPP_SCOPE:
        test = challenge.are_challengeable(team_ids=team_ids_to_test)
        assert isinstance(test, dict)
        for k, v in test.items():
            assert k in team_ids_to_test
            assert isinstance(v, bool)
    else:
        with pytest.raises(HTUnauthorizedAction):
            challenge.are_challengeable(team_ids=team_ids_to_test)
