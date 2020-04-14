import os

import pytest

from pychpp import __version__
from pychpp import CHPP
from pychpp.ht_team import HTTeam, HTYouthTeam
from pychpp.ht_user import HTUser
from pychpp.ht_player import HTPlayer
from pychpp.ht_arena import HTArena


PYCHPP_CONSUMER_KEY = os.environ['PYCHPP_CONSUMER_KEY']
PYCHPP_CONSUMER_SECRET = os.environ['PYCHPP_CONSUMER_SECRET']
PYCHPP_ACCESS_TOKEN_KEY = os.environ['PYCHPP_ACCESS_TOKEN_KEY']
PYCHPP_ACCESS_TOKEN_SECRET = os.environ['PYCHPP_ACCESS_TOKEN_SECRET']


def test_version():
    assert __version__ == '0.1.1'


def test_request_token():
    chpp = CHPP(consumer_key=PYCHPP_CONSUMER_KEY,
                consumer_secret=PYCHPP_CONSUMER_SECRET,
                )

    auth = chpp.get_auth(scope='')

    assert isinstance(auth, dict)
    for key in auth.keys():
        assert key in ('request_token', 'request_token_secret', 'url',)

    assert isinstance(auth['request_token'], str) and auth['request_token']
    assert isinstance(auth['request_token_secret'], str) and auth['request_token_secret']
    assert (isinstance(auth['url'], str)
            and 'https://chpp.hattrick.org/oauth/authorize.aspx?scope=&oauth_token=' in auth['url'])


@pytest.fixture
def chpp():
    return CHPP(consumer_key=PYCHPP_CONSUMER_KEY,
                consumer_secret=PYCHPP_CONSUMER_SECRET,
                access_token_key=PYCHPP_ACCESS_TOKEN_KEY,
                access_token_secret=PYCHPP_ACCESS_TOKEN_SECRET,
                )


def test_get_current_team(chpp):

    team = chpp.team()

    assert isinstance(team, HTTeam)
    assert isinstance(team.ht_id, int)
    assert isinstance(team.name, str)

    youth_team = team.youth_team
    assert isinstance(youth_team, HTYouthTeam) or youth_team is None

    user = team.user
    test_user = chpp.user()
    assert user.ht_id == test_user.ht_id


def test_get_specific_team(chpp):

    team = chpp.team(ht_id=591993)
    assert isinstance(team, HTTeam)
    assert team.ht_id == 591993
    assert team.name == "thekiki's"
    assert team.short_name == 'thekikis'
    assert team.is_primary_club is True

    user = team.user
    assert isinstance(user, HTUser)
    assert user.ht_id == 6336642
    assert user.username == 'thekiki76'
    assert user.supporter_tier == 'platinum'

    youth_team = team.youth_team
    assert isinstance(youth_team, HTYouthTeam)
    assert youth_team.name == 'thebabykikis'


def test_get_current_user(chpp):

    user = chpp.user()

    assert isinstance(user, HTUser)
    assert isinstance(user.ht_id, int)
    assert isinstance(user.username, str)


def test_get_player(chpp):

    player = chpp.player(ht_id=432002549)

    assert isinstance(player, HTPlayer)
    assert player.passing_skill is None
    assert player.owner_notes is None

    assert player.ht_id == 432002549
    assert player.agreeability == 2
    assert player.aggressiveness == 3
    assert player.honesty == 3

    assert isinstance(player.tsi, int)
    assert isinstance(player.injury_level, int)


def test_get_current_user_arena(chpp):

    arena = chpp.arena()
    assert isinstance(arena, HTArena)
    assert isinstance(arena.ht_id, int)
    assert isinstance(arena.name, str)
