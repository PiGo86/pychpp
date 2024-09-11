import os
import datetime as dt
import pytz
import pytest
import re
import pathlib
import xml.etree.ElementTree

from pychpp import CHPP

from .fixtures import chpp, mocked_chpp


def test_request_token(chpp: CHPP):

    auth = chpp.get_auth(scope='')

    assert isinstance(auth, dict)
    for key in auth.keys():
        assert key in ('request_token', 'request_token_secret', 'url',)

    assert isinstance(auth['request_token'], str) and auth['request_token']
    assert isinstance(auth['request_token_secret'],
                      str) and auth['request_token_secret']
    assert (isinstance(auth['url'], str)
            and 'https://chpp.hattrick.org/oauth/authorize.aspx'
                '?scope=&oauth_token=' in auth['url'])


def test_get_own_youth_player(mocked_chpp):

    yp = mocked_chpp.youth_player(ht_id=259808489)
    assert yp.ht_id == 259808489
    assert yp.first_name == "Alain"
    assert yp.last_name == "Rombaut"
    assert yp.age == HTAge(age=20, age_days=15)
    assert yp.arrival_date == HTDatetime.from_calendar(year=2020, month=4,
                                                       day=11, hour=9,
                                                       minute=34, second=0)
    assert yp.can_be_promoted_in == -351
    assert yp.number == 100
    assert yp.cards == 0
    assert yp.injury_level == -1
    assert yp.specialty == 0
    assert yp.career_goals == 5
    assert yp.career_hattricks == 0
    assert yp.league_goals == 0
    assert yp.friendly_goals == 0
    assert yp.team_id == 2816963
    assert yp.team_name == "Les Petits Chapelains"
    assert yp.team_league_id == 446815
    assert yp.senior_team_id == 1165592
    assert yp.senior_team_name == "Les Poitevins de La Chapelle"

    assert isinstance(yp.skills["keeper"], HTSkillYouth)
    assert yp.skills["keeper"].level is None
    assert yp.skills["keeper"].maximum_reached is False
    assert yp.skills["keeper"].maximum == 2

    assert isinstance(yp.skills["playmaker"], HTSkillYouth)
    assert yp.skills["playmaker"].level == 4
    assert yp.skills["playmaker"].maximum_reached is False
    assert yp.skills["playmaker"].maximum == 4

    assert isinstance(yp.skills["defender"], HTSkillYouth)
    assert yp.skills["defender"].level == 4
    assert yp.skills["defender"].maximum_reached is True
    assert yp.skills["defender"].maximum == 4


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
    assert arena.name == 'Le Piquant'
    assert arena.url == "https://www.hattrick.org/goto.ashx" \
                        "?path=/Club/Arena/?ArenaID=295023"

    team = arena.team
    assert isinstance(team, HTTeam)
    assert team.ht_id == 295023
    assert team.name == 'Les piments verts'
    assert team.url == "https://www.hattrick.org/goto.ashx" \
                       "?path=/Club/?TeamID=295023"


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
    assert region.url == "https://www.hattrick.org/goto.ashx" \
                         "?path=/World/Regions/Region.aspx?RegionID=149"


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

    ma2 = chpp.matches_archive(
        ht_id=1165592,
        first_match_date=HTDatetime.from_calendar(2020, 1, 1),
        last_match_date=HTDatetime.from_calendar(2020, 3, 31),
    )

    assert ma2[0].ht_id == 652913955
    assert ma2[0].home_team_name == "Les Poitevins de La Chapelle"
    assert ma2[0].away_team_name == "FC Traversonne"
    assert ma2[0].datetime == HTDatetime.from_calendar(2020, 1, 1, 15, 10, 0)
    assert ma2[0].type == 5
    assert ma2[0].context_id == 0
    assert ma2[0].rule_id == 0
    assert ma2[0].cup_level == 0
    assert ma2[0].cup_level_index == 0
    assert ma2[0].home_goals == 2
    assert ma2[0].away_goals == 0
    assert ma2[0].url == "https://www.hattrick.org/goto.ashx" \
                         "?path=/Club/Matches/Match.aspx?matchID=652913955"

    for m in ma2:
        assert (HTDatetime.from_calendar(2020, 1, 1)
                <= m.datetime <=
                HTDatetime.from_calendar(2020, 3, 31))


def test_get_other_user_matches_archives(chpp):
    ma1 = chpp.matches_archive(
        ht_id=1755906,
        first_match_date=HTDatetime.from_calendar(2018, 4, 10),
        last_match_date=HTDatetime.from_calendar(2018, 4, 30),
    )

    assert re.match(MATCH_ARCHIVE_PATTERN, ma1.url)

    for m in ma1:
        assert (HTDatetime.from_calendar(2018, 4, 10)
                <= m.datetime <=
                HTDatetime.from_calendar(2018, 6, 30))
        assert 1755906 in (m.home_team_id, m.away_team_id)
        assert re.match(MATCH_PATTERN, m.url)

    ma2 = chpp.matches_archive(ht_id=1755906,
                               season=60,
                               )

    assert re.match(MATCH_ARCHIVE_PATTERN, ma2.url)

    for m in ma2:
        assert (HTDatetime.from_calendar(2015, 10, 26)
                <= m.datetime <=
                HTDatetime.from_calendar(2016, 2, 14))
        assert 1755906 in (m.home_team_id, m.away_team_id)
        assert re.match(MATCH_PATTERN, m.url)


def test_get_match(chpp):
    m = chpp.match(ht_id=547513790, events=True)

    assert isinstance(m, HTMatch)
    assert m.ht_id == 547513790
    assert m.url == "https://www.hattrick.org/goto.ashx?" \
                    "path=/Club/Matches/Match.aspx?matchID=547513790"
    assert m.datetime == HTDatetime.from_calendar(2015, 12, 19, 21, 0)
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
            challenge.is_challengeable(team_ht_id=1750803)


def test_league(chpp):
    league = chpp.league(ht_id=36378)

    assert isinstance(league, HTLeague)
    assert league.ht_id == 36378
    assert league.name == "VI.390"
    assert league.country_id == 5
    assert league.url == "https://www.hattrick.org/goto.ashx" \
                         "?path=/World/Series/?LeagueLevelUnitID=36378"

    assert isinstance(league.teams, list)

    for r in league.teams:
        assert isinstance(r, HTTeamRank)

    assert league.teams[3].position == 4


def test_get_match_lineup(mocked_chpp):
    match_lineup = mocked_chpp.match_lineup(ht_id=660688698, team_id=86324)

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

    # Ending lineup
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

    # Starting lineup
    assert len(match_lineup.starting_lineup_players) == 13
    assert isinstance(match_lineup.starting_lineup_players[2], HTLineupPlayer)
    assert isinstance(match_lineup.starting_lineup_players[2].player, HTPlayer)
    assert match_lineup.starting_lineup_players[2].ht_id == 453372830
    assert match_lineup.starting_lineup_players[2].first_name == "Gaspar"
    assert match_lineup.starting_lineup_players[2].role_id == 105
    assert match_lineup.starting_lineup_players[2].role_name == "Left back"
    assert match_lineup.starting_lineup_players[10].role_id == 113
    assert match_lineup.starting_lineup_players[10].role_name == "Left forward"
    assert re.match(PLAYER_PATTERN,
                    match_lineup.starting_lineup_players[10].url)

    # Substitutions
    substitutions = match_lineup.substitutions
    assert len(substitutions) == 2
    sub = substitutions[1]
    assert isinstance(sub, HTSubstitution)
    assert sub.team_id == 86324
    assert sub.subject_player_id == 453372834
    assert sub.object_player_id == 453372838
    assert sub.order_type == 1
    assert sub.new_position_id == 108
    assert sub.new_position_behaviour == 0
    assert sub.match_minute == 73
    assert sub.match_part == 2

    ml2 = mocked_chpp.match_lineup(ht_id=685566813, team_id=1750803)

    assert ml2.ht_id == 685566813
    assert ml2.home_team_name == "Capdenaguet"
    assert ml2.away_team_id == 1165592
    assert ml2.away_team_name == "Les Poitevins de La Chapelle"
    assert ml2.arena_id == 960796
    assert ml2.game_type == 5

    assert ml2.formations == [(0, "451"),
                              (50, "442"),
                              (50, "433"),
                              (50, "523"),
                              ]

    # specific case : injured player is not replaced
    ml3 = mocked_chpp.match_lineup(ht_id=690094305, team_id=296272)

    assert ml3.formations == [(0, "433"),
                              (63, "333"),
                              ]

    ml4 = mocked_chpp.match_lineup(ht_id=690183773, team_id=2053693)

    assert ml4.formations == [(0, "253"),
                              (8, "153"),
                              ]

    # test swap substitution
    ml5 = mocked_chpp.match_lineup(ht_id=685860616, team_id=113143)

    assert ml5.formations == [(0, "352"),
                              ]

    # other unreplaced player
    ml6 = mocked_chpp.match_lineup(ht_id=690328642, team_id=773670)

    assert ml6.formations == [(0, "532"),
                              (81, "432"),
                              ]

    # goalkeeper replaced by field player
    ml7 = mocked_chpp.match_lineup(ht_id=693127128, team_id=291394)

    assert ml7.formations == [(0, "352"),
                              (77, "252"),
                              (81, "152"),
                              ]

    # substitute player become captain and is swapped
    ml8 = mocked_chpp.match_lineup(ht_id=695301077, team_id=294798)

    assert ml8.formations == [(0, "343"),
                              (75, "253"),
                              ]


def test_get_youth_match_lineup(mocked_chpp):
    match_lineup = mocked_chpp.match_lineup(ht_id=120287045,
                                            team_id=2854893,
                                            source='youth')

    assert isinstance(match_lineup.lineup_players[0], HTLineupPlayer)

    youth_player = match_lineup.lineup_players[0].player
    assert isinstance(youth_player, HTYouthPlayer)
    assert youth_player.ht_id == 282977457
    assert youth_player.first_name == "和人 (Kazuto)"
    assert youth_player.last_name == "古川 (Furukawa)"

    assert re.match(YOUTH_PLAYER_PATTERN, match_lineup.lineup_players[0].url)


def test_get_world_details(chpp):
    portugal_details = chpp.world(ht_id=25, include_regions=True)

    assert isinstance(portugal_details, HTWorld)
    assert isinstance(portugal_details.leagues[0], HTCountryLeague)
    assert isinstance(portugal_details.leagues[0].country, HTCountry)
    assert isinstance(portugal_details.leagues[0].cups[0], HTCup)

    assert len(portugal_details.leagues) == 1
    assert portugal_details.league(ht_id=25).league_name == "Portugal"
    assert portugal_details.league(name="portugal").ht_id == 25
    assert portugal_details.league(ht_id=25).country.country_name == "Portugal"

    portugal_regions = portugal_details.league(ht_id=25).country.regions
    assert len(portugal_regions) >= 1
    assert isinstance(portugal_regions[0], HTRegionItem)
    assert isinstance(portugal_regions[0].region, HTRegion)
    assert len(portugal_details.league(ht_id=25).cups) >= 1

    with pytest.raises(UnknownLeagueError):
        portugal_details.league(ht_id=26)

    world_details = chpp.world()

    assert len(world_details.leagues) > 1
    assert world_details.leagues[0].country.regions is None

    assert re.match(COUNTRY_LEAGUE_PATTERN,
                    portugal_details.league(ht_id=25).url)
    assert re.match(REGION_PATTERN, portugal_regions[0].region.url)
    assert re.match(CUP_PATTERN, portugal_details.league(ht_id=25).cups[0].url)


def test_use_ht_datetime():

    ht_d = HTDatetime(datetime=dt.datetime(year=2020, month=9, day=7))
    assert (ht_d.season, ht_d.week, ht_d.weekday) == (75, 15, 1)
    assert ht_d.league == ""

    ht_d.league = "Brazil"
    assert ht_d.season == 63
    assert ht_d.league == "Brazil"

    ht_d = ht_d + dt.timedelta(days=900)
    assert (ht_d.season, ht_d.week, ht_d.weekday) == (71, 15, 5)
    cet = pytz.timezone("CET")
    date = cet.localize(dt.datetime(year=2023, month=2, day=24))
    assert ht_d.datetime == date
    assert ht_d.league == "Brazil"

    ht_d.timezone = "America/Belize"
    assert ht_d == HTDatetime.from_calendar(2023, 2, 23, 17,
                                            timezone="America/Belize")
    assert (ht_d.season, ht_d.week, ht_d.weekday) == (71, 15, 4)

    ht_d = HTDatetime.from_calendar(2020, 9, 21, 1, 30)
    assert (ht_d.season, ht_d.week, ht_d.weekday) == (76, 1, 1)
    ht_d.timezone = "America/Bahia"
    assert (ht_d.season, ht_d.week, ht_d.weekday) == (75, 16, 7)


def test_get_nt_details(chpp):
    portugal_details = chpp.national_team(ht_id=3014)

    assert isinstance(portugal_details, HTNationalTeam)

    assert portugal_details.ht_id == 3014
    assert portugal_details.league_id == 25
    assert portugal_details.league_name == "Portugal"
    assert portugal_details.team_name == "Portugal"

    with pytest.raises(HTUnknownTeamIdError):
        chpp.national_team(ht_id=1000000)


def test_get_nts(chpp):
    national_teams = chpp.national_teams(ht_id=2)

    assert isinstance(national_teams, HTNationalTeams)
    assert len(national_teams.teams) > 0
    assert national_teams.url == "https://www.hattrick.org/goto.ashx?path=" + \
                                 "/World/NationalTeams/NationalTeams.aspx?" + \
                                 "viewType=1&leagueOfficeTypeId=2"

    portugal_entry = list(
        filter(lambda k: k.ht_id == 3014, national_teams.teams)
    )[0]
    assert isinstance(portugal_entry, HTNationalTeamEntry)
    assert portugal_entry.ht_id == 3014
    assert portugal_entry.team_name == "Portugal"


def test_get_world_cup_rounds(chpp):
    wc_groups = chpp.world_cup_groups(season=76)

    assert isinstance(wc_groups, HTWorldCupGroups)
    assert wc_groups.cup_id == 137
    assert wc_groups.cup_name == "World Cup"
    assert wc_groups.season == 76

    # Deactivated waiting for CHPP fix
    # assert isinstance(wc_groups.scores[0], HTWorldCupScore)

    assert len(wc_groups.rounds) == 6
    assert isinstance(wc_groups.rounds[0], HTWorldCupRound)

    wc_groups_u20 = chpp.world_cup_groups(season=76, cup_id=149)

    assert wc_groups_u20.cup_name == "U-20 World Cup"


def test_get_world_cup_matches(chpp):
    wc_matches = chpp.world_cup_matches(season=76, cup_series_unit_id=1697)

    assert isinstance(wc_matches, HTWorldCupMatches)
    assert wc_matches.cup_id == 137
    assert wc_matches.cup_name == "World Cup"
    assert wc_matches.season == 76
    assert wc_matches.cup_series_unit_id == 1697
    assert wc_matches.match_round == 1

    assert len(wc_matches.matches) == 6
    assert isinstance(wc_matches.matches[0], HTWorldCupMatch)
    assert wc_matches.matches[0].home_team_id == 3002
    assert wc_matches.matches[0].home_team_name == "Deutschland"
    assert wc_matches.matches[0].match_id == 669657311

    assert len(wc_matches.rounds) == 6
    assert isinstance(wc_matches.rounds[0], HTWorldCupRound)


def test_get_league_fixtures(chpp):
    l_fixtures = chpp.league_fixtures(ht_id=36378, season=76)

    assert isinstance(l_fixtures, HTLeagueFixtures)
    assert l_fixtures.ht_id == 36378
    assert l_fixtures.season == 76
    assert l_fixtures.name == "VI.390"

    assert isinstance(l_fixtures.matches, list)
    assert len(l_fixtures.matches) == 56
    assert isinstance(l_fixtures.matches[10], HTLeagueFixturesMatch)


def test_get_training(mocked_chpp):

    training = mocked_chpp.training(team_ht_id=1165592)

    assert isinstance(training, HTTraining)

    assert training.team_ht_id == 1165592
    assert training.team_name == "Les Poitevins de La Chapelle"

    assert training.training_level == 98
    assert training.new_training_level is None
    assert training.training_type == 3
    assert training.stamina_training_part == 25
    assert training.last_training_training_type == 5
    assert training.last_training_training_level == 95
    assert training.last_training_stamina_training_part == 16

    assert training.trainer_ht_id == 421746800
    assert training.trainer_name == "Quentin Lavigne"
    assert training.trainer_arrival_date == HTDatetime.from_calendar(
        2018, 3, 23, 19, 44, 0)

    assert training.morale == 4
    assert training.self_confidence == 5

    assert training.experience_442 == 7
    assert training.experience_433 == 4
    assert training.experience_451 == 3
    assert training.experience_352 == 8
    assert training.experience_532 == 4
    assert training.experience_343 == 3
    assert training.experience_541 == 6
    assert training.experience_523 == 9
    assert training.experience_550 == 5
    assert training.experience_253 == 10


def test_get_team_transfers(mocked_chpp):

    transfers_team = mocked_chpp.transfers_team(ht_id=940, page_index=1)

    assert isinstance(transfers_team, HTTransfersTeam)

    assert transfers_team.ht_id == 940
    assert transfers_team.name == "FC Vanilla"
    assert transfers_team.activated_date == (
        HTDatetime.from_calendar(2003, 2, 1, 3, 15, 0))
    assert transfers_team.total_sum_of_buys == 572_579_730
    assert transfers_team.total_sum_of_sales == 569_274_290
    assert transfers_team.number_of_buys == 65
    assert transfers_team.number_of_sales == 144

    assert transfers_team.page_index == 1
    assert transfers_team.pages == 9
    assert transfers_team.start_date == HTDatetime.from_calendar(2008, 10, 11,
                                                                 16, 5, 0)
    assert transfers_team.end_date == HTDatetime.from_calendar(2009, 10, 31,
                                                               9, 44, 0)

    assert isinstance(transfers_team.transfer_list, list)
    assert len(transfers_team.transfer_list) == 25

    transfer_item = transfers_team.transfer_list[10]
    assert isinstance(transfer_item, HTTransfersTeamItem)
    assert transfer_item.ht_id == 177997172
    assert transfer_item.deadline == HTDatetime.from_calendar(2009, 6, 26,
                                                              21, 21, 0)
    assert transfer_item.transfer_type == "S"
    assert transfer_item.price == 10_000_000
    assert transfer_item.player_id == 0
    assert transfer_item.player_name == "André da Costa"
    assert transfer_item.tsi == 10_260
    assert transfer_item.buyer_team_id == 494228
    assert transfer_item.buyer_team_name == "LOS CARA DEPERCHAS"
    assert transfer_item.seller_team_id == 940
    assert transfer_item.seller_team_name == "FC Vanilla"
