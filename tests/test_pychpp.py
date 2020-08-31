import os
import datetime
import pytest
import re

from pychpp import __version__
from pychpp import CHPP
from pychpp.ht_team import HTTeam, HTYouthTeam
from pychpp.ht_user import HTUser
from pychpp.ht_player import HTPlayer, HTYouthPlayer, HTLineupPlayer
from pychpp.ht_arena import HTArena
from pychpp.ht_region import HTRegion
from pychpp.ht_match import HTMatch
from pychpp.ht_match_lineup import HTMatchLineup
from pychpp.ht_matches_archive import HTMatchesArchive, HTMatchesArchiveItem
from pychpp.ht_skill import HTSkill, HTSkillYouth
from pychpp.ht_challenge import HTChallengeManager
from pychpp.ht_league import HTLeague
from pychpp.ht_rank import HTRank
from pychpp.ht_error import HTUnauthorizedAction

PYCHPP_CONSUMER_KEY = os.environ["PYCHPP_CONSUMER_KEY"]
PYCHPP_CONSUMER_SECRET = os.environ["PYCHPP_CONSUMER_SECRET"]
PYCHPP_ACCESS_TOKEN_KEY = os.environ["PYCHPP_ACCESS_TOKEN_KEY"]
PYCHPP_ACCESS_TOKEN_SECRET = os.environ["PYCHPP_ACCESS_TOKEN_SECRET"]
PYCHPP_SCOPE = os.environ["PYCHPP_SCOPE"]

YOUTH_PLAYER_PATTERN = r"https://www.hattrick.org/goto.ashx\?path=/Club/Players/YouthPlayer.aspx\?YouthPlayerID=(\d+)"
PLAYER_PATTERN = r"https://www.hattrick.org/goto.ashx\?path=/Club/Players/Player.aspx\?playerId=(\d+)"
YOUTH_TEAM_PATTERN = r"https://www.hattrick.org/goto.ashx\?path=/Club/Youth/\?YouthTeamID=(\d+)"
ARENA_PATTERN = r"https://www.hattrick.org/goto.ashx\?path=/Club/Arena/\?ArenaID=(\d+)"
USER_PATTERN = r"https://www.hattrick.org/goto.ashx\?path=/Club/Manager/\?userId=(\d+)"
REGION_PATTERN = r"https://www.hattrick.org/goto.ashx\?path=/World/Regions/Region.aspx\?RegionID=(\d+)"
MATCH_ARCHIVE_PATTERN = r"https://www.hattrick.org/goto.ashx\?path=%2FClub%2FMatches%2FArchive.aspx%3F(TeamID%3D(\d*))?(%26)?(season%3D(\d*))?"
MATCH_PATTERN = r"https://www.hattrick.org/goto.ashx\?path=/Club/Matches/Match.aspx\?matchID=(\d+)"


def test_version():
    assert __version__ == '0.2.6'


def test_request_token():
    chpp = CHPP(consumer_key=PYCHPP_CONSUMER_KEY,
                consumer_secret=PYCHPP_CONSUMER_SECRET,
                )

    auth = chpp.get_auth(scope='')

    assert isinstance(auth, dict)
    for key in auth.keys():
        assert key in ('request_token', 'request_token_secret', 'url',)

    assert isinstance(auth['request_token'], str) and auth['request_token']
    assert isinstance(auth['request_token_secret'],
                      str) and auth['request_token_secret']
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
    assert isinstance(team.url, str)

    youth_team = team.youth_team
    assert isinstance(youth_team, HTYouthTeam) or youth_team is None

    user = team.user
    test_user = chpp.user()
    assert user.ht_id == test_user.ht_id

    players = team.players
    assert isinstance(players, list)
    for p in players:
        assert isinstance(p, HTPlayer)


def test_get_specific_team(chpp):
    team = chpp.team(ht_id=591993)
    assert isinstance(team, HTTeam)
    assert team.ht_id == 591993
    assert team.name == "thekiki's"
    assert team.short_name == 'thekikis'
    assert team.is_primary_club is True
    assert team.power_rating > 0
    assert team.url == "https://www.hattrick.org/goto.ashx?path=/Club/?TeamID=591993"

    user = team.user
    assert isinstance(user, HTUser)
    assert user.ht_id == 6336642
    assert user.username == 'thekiki76'
    assert user.supporter_tier == 'platinum'
    assert user.url == "https://www.hattrick.org/goto.ashx?path=/Club/Manager/?userId=6336642"

    youthteam = team.youth_team
    assert isinstance(youthteam, HTYouthTeam)
    assert youthteam.name == 'thebabykikis'
    assert re.match(YOUTH_TEAM_PATTERN, youthteam.url)

    arena = team.arena
    assert isinstance(arena, HTArena)
    assert arena.name == "thekiki's evil"
    assert re.match(ARENA_PATTERN, arena.url)


def test_get_secondary_team(chpp):
    team = chpp.team(ht_id=44307)

    assert isinstance(team, HTTeam)
    assert team.ht_id == 44307
    assert team.name == "Grynvalla IK"
    assert team.short_name == 'Grynvalla'
    assert team.is_primary_club is False
    assert team.url == "https://www.hattrick.org/goto.ashx?path=/Club/?TeamID=44307"

    user = team.user
    assert isinstance(user, HTUser)
    assert user.ht_id == 182085
    assert user.username == "Kvarak"
    assert user.url == "https://www.hattrick.org/goto.ashx?path=/Club/Manager/?userId=182085"

    youthteam = team.youth_team
    assert isinstance(youthteam, HTYouthTeam)
    assert youthteam.name == "Grynets pojkar"
    assert re.match(YOUTH_TEAM_PATTERN, youthteam.url)

    arena = team.arena
    assert isinstance(arena, HTArena)
    assert arena.name == "Grynvallen"
    assert re.match(ARENA_PATTERN, arena.url)


def test_get_current_user(chpp):
    user = chpp.user()

    assert isinstance(user, HTUser)
    assert isinstance(user.ht_id, int)
    assert isinstance(user.username, str)
    assert isinstance(user.url, str)
    assert re.match(USER_PATTERN, user.url)


def test_get_player(chpp):
    player = chpp.player(ht_id=432002549)

    assert isinstance(player, HTPlayer)
    assert isinstance(player.skills, dict)
    assert {i for i in player.skills.keys()}.issubset(HTSkill.SKILLS_NAME)
    assert player.owner_notes is None

    assert player.ht_id == 432002549
    assert player.agreeability == 2
    assert player.aggressiveness == 3
    assert player.honesty == 3
    assert player.url == "https://www.hattrick.org/goto.ashx?path=/Club/Players/Player.aspx?playerId=432002549"

    assert isinstance(player.skills, dict)
    assert len(player.skills) == 8
    for i in player.skills.keys():
        assert i in ("stamina", "keeper", "defender", "playmaker",
                     "winger", "scorer", "passing", "set_pieces")

    assert isinstance(player.tsi, int)
    assert isinstance(player.injury_level, int)


def test_get_youth_player(chpp):
    youthteam = chpp.youth_team()
    assert isinstance(youthteam, HTYouthTeam)
    if youthteam.ht_id != 0:
        youthplayer = youthteam.players[0]
        assert isinstance(youthplayer, HTYouthPlayer)
        assert {i for i in youthplayer.skills.keys()}.issubset(
            HTSkillYouth.SKILLS_TAG)
        assert re.match(YOUTH_PLAYER_PATTERN, youthplayer.url)


def test_get_current_user_arena(chpp):
    arena = chpp.arena()
    assert isinstance(arena, HTArena)
    assert isinstance(arena.ht_id, int) or arena.ht_id is None
    assert isinstance(arena.name, str)
    assert isinstance(arena.url, str)
    assert re.match(ARENA_PATTERN, arena.url)


def test_get_specific_arena(chpp):
    arena = chpp.arena(ht_id=295023)
    assert isinstance(arena, HTArena)
    assert arena.ht_id == 295023
    assert arena.name == 'Les piments verts Arena'
    assert arena.url == "https://www.hattrick.org/goto.ashx?path=/Club/Arena/?ArenaID=295023"

    team = arena.team
    assert isinstance(team, HTTeam)
    assert team.ht_id == 295023
    assert team.name == 'Les piments verts'
    assert team.url == "https://www.hattrick.org/goto.ashx?path=/Club/?TeamID=295023"


def test_get_current_user_region(chpp):
    region = chpp.region()
    assert isinstance(region, HTRegion)
    assert isinstance(region.ht_id, int)
    assert isinstance(region.name, str)
    assert isinstance(region.number_of_users, int)
    assert isinstance(region.number_of_online, int)
    assert isinstance(region.weather, int)
    assert isinstance(region.tomorrow_weather, int)
    assert isinstance(region.url, str)
    assert re.match(REGION_PATTERN, region.url)


def test_get_specific_region(chpp):
    region = chpp.region(ht_id=149)
    assert isinstance(region, HTRegion)
    assert region.ht_id == 149
    assert region.name == "Provence-Alpes-Côte d'Azur"
    assert isinstance(region.number_of_users, int)
    assert isinstance(region.number_of_online, int)
    assert isinstance(region.weather, int)
    assert isinstance(region.tomorrow_weather, int)
    assert region.url == "https://www.hattrick.org/goto.ashx?path=/World/Regions/Region.aspx?RegionID=149"


def test_get_current_user_matches_archive(chpp):
    ma1 = chpp.matches_archive()
    assert isinstance(ma1, HTMatchesArchive)
    assert isinstance(ma1.url, str)
    assert re.match(MATCH_ARCHIVE_PATTERN, ma1.url)
    m = ma1[0]
    assert isinstance(m, HTMatchesArchiveItem)
    assert isinstance(m.home_team, HTTeam)
    assert isinstance(m.url, str)
    assert re.match(MATCH_PATTERN, m.url)

    ma2 = chpp.matches_archive(ht_id=1165592,
                               first_match_date=datetime.datetime(2020, 1, 1),
                               last_match_date=datetime.datetime(2020, 3, 31), )

    assert ma2[0].ht_id == 652913955
    assert ma2[0].home_team_name == "Les Poitevins de La Chapelle"
    assert ma2[0].away_team_name == "FC Traversonne"
    assert ma2[0].date == datetime.datetime(2020, 1, 1, 15, 10)
    assert ma2[0].type == 5
    assert ma2[0].context_id == 0
    assert ma2[0].rule_id == 0
    assert ma2[0].cup_level == 0
    assert ma2[0].cup_level_index == 0
    assert ma2[0].home_goals == 2
    assert ma2[0].away_goals == 0
    assert ma2[0].url == "https://www.hattrick.org/goto.ashx?path=/Club/Matches/Match.aspx?matchID=652913955"

    for m in ma2:
        assert datetime.datetime(
            2020, 1, 1) <= m.date <= datetime.datetime(2020, 3, 31)


def test_get_other_user_matches_archives(chpp):
    ma1 = chpp.matches_archive(ht_id=1755906,
                               first_match_date=datetime.datetime(2018, 4, 10),
                               last_match_date=datetime.datetime(2018, 4, 30),
                               )

    assert re.match(MATCH_ARCHIVE_PATTERN, ma1.url)

    for m in ma1:
        assert datetime.datetime(
            2018, 4, 10) <= m.date <= datetime.datetime(2018, 6, 30)
        assert 1755906 in (m.home_team_id, m.away_team_id)
        assert re.match(MATCH_PATTERN, m.url)

    ma2 = chpp.matches_archive(ht_id=1755906,
                               season=60,
                               )

    assert re.match(MATCH_ARCHIVE_PATTERN, ma2.url)

    for m in ma2:
        assert datetime.datetime(
            2015, 10, 26) <= m.date <= datetime.datetime(2016, 2, 14)
        assert 1755906 in (m.home_team_id, m.away_team_id)
        assert re.match(MATCH_PATTERN, m.url)


def test_get_match(chpp):
    m = chpp.match(ht_id=547513790, events=True)

    assert isinstance(m, HTMatch)
    assert m.ht_id == 547513790
    assert m.url == "https://www.hattrick.org/goto.ashx?path=/Club/Matches/Match.aspx?matchID=547513790"
    assert m.date == datetime.datetime(2015, 12, 19, 21, 0)
    assert m.home_team_name == "Olympique Mig"
    assert m.away_team_name == "Camden County Jerks"
    assert m.added_minutes == 0
    assert m.arena_id == 1162154
    assert len(m.events) >= 0
    assert m.events[14]["minute"] == 72
    assert m.events[14]["match_part"] == 2
    assert m.events[14]["id"] == 285
    assert m.events[14]["variation"] == 3
    assert m.events[14]["subject_team_id"] == 292366
    assert m.events[14]["subject_player_id"] == 373737451
    assert m.events[14]["object_player_id"] == 314946894
    # Description is localized
    # assert "free kick" in m.events[14]["description"]


def test_is_challengeable(chpp):
    challenge = HTChallengeManager(chpp)

    if "manage_challenges" in PYCHPP_SCOPE:
        ich = challenge.is_challengeable(team_ht_id=1750803)
        assert isinstance(ich, dict)
        for b in ich.values():
            assert isinstance(b, bool)
    else:
        with pytest.raises(HTUnauthorizedAction):
            ich = challenge.is_challengeable(team_ht_id=1750803)


def test_league(chpp):
    league = chpp.league(ht_id=36378)

    assert isinstance(league, HTLeague)
    assert league.ht_id == 36378
    assert league.name == "VI.390"
    assert league.country_id == 5
    assert league.url == "https://www.hattrick.org/goto.ashx?path=/World/Series/?LeagueLevelUnitID=36378"

    assert isinstance(league.ranks, list)

    for r in league.ranks:
        assert isinstance(r, HTRank)

    assert league.ranks[3].position == 4


def test_get_match_lineup(chpp):
    match_lineup = chpp.match_lineup(ht_id=660688698, team_id=86324)

    assert isinstance(match_lineup, HTMatchLineup)
    assert isinstance(match_lineup.match, HTMatch)

    assert match_lineup.ht_id == 660688698
    assert match_lineup.home_team_name == "Gazela.f.c"
    assert match_lineup.away_team_id == 86324
    assert match_lineup.away_team_name == "Apanha Bolas FC"
    assert match_lineup.arena_id == 1420520
    assert match_lineup.game_type == 1
    assert re.match(MATCH_PATTERN, match_lineup.url)

    assert isinstance(match_lineup.arena, HTArena)

    assert len(match_lineup.lineup_players) == 20
    assert isinstance(match_lineup.lineup_players[0], HTLineupPlayer)
    assert isinstance(match_lineup.lineup_players[0].player, HTPlayer)
    assert match_lineup.lineup_players[0].ht_id == 453372825
    assert match_lineup.lineup_players[0].first_name == "Teodoro"
    assert match_lineup.lineup_players[0].role_id == 100
    assert match_lineup.lineup_players[0].role_name == "Keeper"
    assert match_lineup.lineup_players[15].role_id == 120
    assert match_lineup.lineup_players[15].role_name == "Unknown role"
    assert re.match(PLAYER_PATTERN, match_lineup.lineup_players[15].url)

    match_lineup = chpp.match_lineup(
        ht_id=116104524, team_id=2828377, source='youth')
    assert isinstance(match_lineup.lineup_players[0], HTLineupPlayer)
    assert isinstance(match_lineup.lineup_players[0].player, HTYouthPlayer)
    assert re.match(YOUTH_PLAYER_PATTERN, match_lineup.lineup_players[0].url)
