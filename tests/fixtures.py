import os
import pathlib
import xml.etree.ElementTree as EltTree

import pytest

from pychpp import CHPP


PYCHPP_CONSUMER_KEY = os.environ["PYCHPP_CONSUMER_KEY"]
PYCHPP_CONSUMER_SECRET = os.environ["PYCHPP_CONSUMER_SECRET"]
PYCHPP_ACCESS_TOKEN_KEY = os.environ["PYCHPP_ACCESS_TOKEN_KEY"]
PYCHPP_ACCESS_TOKEN_SECRET = os.environ["PYCHPP_ACCESS_TOKEN_SECRET"]
PYCHPP_SCOPE = os.environ["PYCHPP_SCOPE"]

BASE_PATTERN = r"https://www.hattrick.org/goto.ashx\?path="
TEAM_PATTERN = BASE_PATTERN + r"/Club/\?teamID=(\d+)"
YOUTH_PLAYER_PATTERN = BASE_PATTERN + r"/Club/Players/YouthPlayer.aspx/\?youthPlayerId=(\d+)"
PLAYER_PATTERN = BASE_PATTERN + r"/Club/Players/Player.aspx\?playerId=(\d+)"
YOUTH_TEAM_PATTERN = BASE_PATTERN + r"/Club/Youth/\?youthTeamId=(\d+)"
ARENA_PATTERN = BASE_PATTERN + r"/Club/Stadium/\?arenaID=(\d+)"
USER_PATTERN = BASE_PATTERN + r"/Club/Manager/\?userId=(\d+)"
REGION_PATTERN = BASE_PATTERN + r"/World/Regions/Region.aspx\?RegionID=(\d+)"
MATCH_ARCHIVE_PATTERN = BASE_PATTERN + r"%2FClub%2FMatches%2FArchive.aspx%3F(TeamID%3D(\d*))?(%26)\?(season%3D(\d*))?"
MATCH_PATTERN = BASE_PATTERN + r"/Club/Matches/Match.aspx\?matchID=(\d+)"
COUNTRY_LEAGUE_PATTERN = BASE_PATTERN + r"/World/Leagues/League.aspx\?LeagueID=(\d+)"
CUP_PATTERN = BASE_PATTERN + r"/World/Cup/Cup.aspx\?CupID=(\d+)"


@pytest.fixture
def chpp():
    return CHPP(consumer_key=PYCHPP_CONSUMER_KEY,
                consumer_secret=PYCHPP_CONSUMER_SECRET,
                access_token_key=PYCHPP_ACCESS_TOKEN_KEY,
                access_token_secret=PYCHPP_ACCESS_TOKEN_SECRET,
                )


@pytest.fixture
def mocked_chpp(monkeypatch):

    def mock_request(*args, **kwargs):

        args_dict = {'file': kwargs.pop('file'), 'version': kwargs.pop('version')}
        args_dict.update(sorted(kwargs.items()))
        filename = '&'.join(f"{k}={v}" for k, v in args_dict.items()) + '.xml'

        path = pathlib.Path(__file__).parent / "test_resources" / filename

        with open(path) as f:
            txt = f.read()

        return EltTree.fromstring(txt)

    monkeypatch.setattr(CHPP, 'request', mock_request)

    return CHPP(consumer_key='', consumer_secret='')
