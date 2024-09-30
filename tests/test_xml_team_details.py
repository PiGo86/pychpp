from pychpp import CHPP
from pychpp.fixtures.ht_datetime import HTDatetime
from pychpp.models.xml.team_details import TeamDetails


def test_get_current_team(chpp: 'CHPP'):

    xml_team = chpp.xml_team_details()

    assert isinstance(xml_team, TeamDetails)
    assert isinstance(xml_team.user.id, int)
    assert isinstance(xml_team.teams, list)
    assert isinstance(xml_team.teams[0].name, str)
    assert isinstance(xml_team.teams[0].bot_status.is_bot, bool)
    assert (isinstance(xml_team.teams[0].youth_team.id, int)
            or xml_team.teams[0].youth_team.id is None)


def test_get_specific_team(mocked_chpp: 'CHPP'):

    xml_team = mocked_chpp.xml_team_details(team_id=987765, version='3.6')

    assert xml_team.user.id == 12453550
    assert xml_team.user.language.id == 13
    assert xml_team.user.language.name == 'Polski'
    assert xml_team.user.supporter_tier == 'platinum'
    assert xml_team.user.login_name == 'Praqol'
    assert xml_team.user.name == 'HIDDEN'
    assert xml_team.user.icq is None
    assert xml_team.user.signup_date == HTDatetime.from_calendar(
        2012, 11, 5, 15, 42, 59,
    )
    assert xml_team.user.activation_date == HTDatetime.from_calendar(
        2012, 11, 10, 10, 50, 0,
    )
    assert xml_team.user.last_login_date == HTDatetime.from_calendar(
        2024, 9, 8, 21, 43, 45,
    )
    assert xml_team.user.has_manager_license is True
    assert xml_team.user.national_teams == []

    assert len(xml_team.teams) == 3

    assert xml_team.teams[0].id == 263018
    assert xml_team.teams[0].name == 'Sojczanka Bytom'
    assert xml_team.teams[0].short_name == 'Sojczanka'
    assert xml_team.teams[0].is_primary_club is True
    assert xml_team.teams[0].founded_date == HTDatetime.from_calendar(
        2012, 11, 10, 10, 50, 0,
    )
    assert xml_team.teams[0].arena.id == 263018
    assert xml_team.teams[0].arena.name == 'Dziura Stadium'
    assert xml_team.teams[0].league.id == 24
    assert xml_team.teams[0].league.name == 'Pologne'
    assert xml_team.teams[0].country.id == 26
    assert xml_team.teams[0].country.name == 'Pologne'
    assert xml_team.teams[0].region.id == 453
    assert xml_team.teams[0].region.name == 'Śląskie'
    assert xml_team.teams[0].trainer.id == 408819892
    assert xml_team.teams[0].homepage is None
    assert xml_team.teams[0].dress_uri == ('//res.hattrick.org/kits/29/285/2847/'
                                           '2846630/matchKitSmall.png')
    assert xml_team.teams[0].dress_alternate_uri == ('//res.hattrick.org/kits/29/285/2847/'
                                                     '2846633/matchKitSmall.png')
    assert xml_team.teams[0].league_level_unit.id == 9410
    assert xml_team.teams[0].league_level_unit.name == 'V.28'
    assert xml_team.teams[0].league_level_unit.level == 5
    assert xml_team.teams[0].bot_status.is_bot is False
    assert xml_team.teams[0].cup.still_in_cup is False
    assert xml_team.teams[0].power_rating.global_ranking == 41515
    assert xml_team.teams[0].power_rating.league_ranking == 2040
    assert xml_team.teams[0].power_rating.region_ranking == 343
    assert xml_team.teams[0].power_rating.value == 946
    assert xml_team.teams[0].friendly_team_id == 987765
    assert xml_team.teams[0].number_of_victories == 2
    assert xml_team.teams[0].number_of_undefeated == 6
    assert xml_team.teams[0].team_rank == 1973
    assert xml_team.teams[0].fan_club.id == 669731
    assert xml_team.teams[0].fan_club.name == 'Kopalnioki'
    assert xml_team.teams[0].fan_club.size == 2272
    assert xml_team.teams[0].logo_url == '//res.hattrick.org/teamlogo/3/27/264/263018/263018.png'
    assert xml_team.teams[0].guestbook.number_of_items == 46
    assert xml_team.teams[0].colors.background_color == '184466'
    assert xml_team.teams[0].colors.color == 'ffffff'
    assert xml_team.teams[0].youth_team.id == 2555250
    assert xml_team.teams[0].youth_team.name == 'Sojczanka Bytom U-19'
    assert xml_team.teams[0].number_of_visits == 5
    assert xml_team.teams[0].possible_to_challenge_midweek is False
    assert xml_team.teams[0].possible_to_challenge_weekend is False


def test_get_specific_team_currently_playing(mocked_chpp):

    xml_team = mocked_chpp.xml_team_details(team_id=326336, version='3.6')
    assert isinstance(xml_team, TeamDetails)

    assert xml_team.user.id == 8380636
    assert xml_team.user.supporter_tier == "none"
    assert xml_team.user.language.id == 51
    assert xml_team.user.language.name == "Español, Rioplatense"
    assert xml_team.user.login_name == "lpannese"
    assert xml_team.user.name == "HIDDEN"
    assert xml_team.user.icq is None
    assert xml_team.user.signup_date == HTDatetime.from_calendar(2008, 8, 18, 20, 52, 9)
    assert xml_team.user.activation_date == HTDatetime.from_calendar(2008, 8, 20, 2, 53, 0)
    assert xml_team.user.last_login_date == HTDatetime.from_calendar(2024, 9, 8, 5, 2, 47)
    assert xml_team.user.has_manager_license is True
    assert xml_team.user.national_teams == []

    team = [t for t in xml_team.teams if t.id == 326336][0]
    assert team.id == 326336
    assert team.name == "La Resaka de S."
    assert team.short_name == 'Resaka'
    assert team.is_primary_club is True
    assert team.founded_date == HTDatetime.from_calendar(2008, 8, 20, 2, 53, 0)

    assert team.arena.id == 326336
    assert team.arena.name == "Silvina Rocha"

    assert team.league.id == 7
    assert team.league.name == "Argentine"

    assert team.country.id == 7
    assert team.country.name == "Argentine"

    assert team.region.id == 66
    assert team.region.name == "Provincia de Buenos Aires"

    assert team.trainer.id == 453291604

    assert team.homepage is None

    assert team.cup.still_in_cup is None
    assert team.cup.id is None
    assert team.cup.name is None
    assert team.cup.league_level is None
    assert team.cup.level is None
    assert team.cup.level_index is None
    assert team.cup.match_round is None
    assert team.cup.match_rounds_left is None

    assert team.power_rating.global_ranking == 254
    assert team.power_rating.league_ranking == 4
    assert team.power_rating.region_ranking == 3
    assert team.power_rating.value == 1185

    assert team.friendly_team_id is None

    assert team.league_level_unit.id is None
    assert team.league_level_unit.name is None
    assert team.league_level_unit.level is None

    assert team.number_of_victories is None
    assert team.number_of_undefeated is None

    assert team.fan_club.id == 0
    assert team.fan_club.name is None
    assert team.fan_club.size == 3778

    assert team.logo_url == "//res.hattrick.org/teamlogo/4/33/327/326336/326336.png"

    assert team.youth_team.id == 2534700
    assert team.youth_team.name == "La Resaka de S"

    assert team.guestbook is None
    assert team.press_announcement is None
    assert team.colors is None

    assert team.dress_uri == "//res.hattrick.org/kits/1/1/1/1/matchKitSmall.png"
    assert team.dress_alternate_uri == "//res.hattrick.org/kits/1/1/1/2/matchKitSmall.png"

    assert team.bot_status.is_bot is False

    assert team.team_rank is None

    assert team.number_of_visits == 16


def test_team_details_version(chpp):

    td_3_7 = chpp.xml_team_details()
    assert isinstance(td_3_7.teams[0].is_deactivated, bool)

    td_3_6 = chpp.xml_team_details(version='3.6')
    assert td_3_6.teams[0].is_deactivated is None
