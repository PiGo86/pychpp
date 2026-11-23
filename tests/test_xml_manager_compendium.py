"""Tests for the `managercompendium.xml` CHPP file parsing."""

from pychpp.models.xml.manager_compendium import ManagerCompendium


def test_get_current_user(chpp):
    user = chpp.xml_manager_compendium()

    assert isinstance(user, ManagerCompendium)
    assert isinstance(user.id, int)
    assert isinstance(user.login_name, str)


def test_manager_compendium_version_1_8(mocked_chpp):
    mc = mocked_chpp.xml_manager_compendium()

    assert mc.id == 1728698
    assert mc.login_name == 'Jean-Mi'
    assert mc.supporter_tier == 'none'
    assert mc.has_manager_license is True
    assert mc.currency.name == '€'
    assert mc.currency.rate == 10.0
    assert mc.language.id == 5
    assert mc.language.name == 'Français'
    assert mc.country.id == 5
    assert mc.country.name == 'France'
    assert len(mc.last_logins) == 6
    assert mc.last_logins[0] == '2026-11-21 19:03:44 : 89.92.***.***'

    team = mc.teams[0]
    assert team.id == 1165592
    assert team.name == 'Les Poitevins de La Chapelle'
    assert team.gender_id == 1
    assert team.league_system_id == 1
    assert team.arena.id == 1162154
    assert team.arena.name == 'Stade de La Chapelle'
    assert team.league.id == 5
    assert team.league.name == 'France'
    assert team.league.season == 96
    assert team.country.id == 5
    assert team.country.name == 'France'
    assert team.league_level_unit.id == 73592
    assert team.league_level_unit.name == 'VII.777'
    assert team.region.id == 148
    assert team.region.name == 'Poitou-Charentes'
    assert team.youth_team.id == 2942691
    assert team.youth_team.name == 'Les Petits Chapelains'
    assert team.youth_team.league.id == 225490
    assert team.youth_team.league.name == 'Robaphipie League'

    assert mc.national_teams_coach == []
    assert mc.national_teams_assistant == []
    assert mc.avatar.background_image == '/Img/Avatar/backgrounds/card1.png'
    assert mc.avatar.layers == []
