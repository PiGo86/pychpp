from pychpp.fixtures.ht_datetime import HTDatetime
from pychpp.models.xml.youth_player_details import YouthPlayerDetails


def test_get_own_youth_player(mocked_chpp):

    yp = mocked_chpp.youth_player(301741211)

    assert yp.id == 301741211
    assert yp.first_name == "Akpa"
    assert yp.last_name == "Tao"
    assert yp.age == 24
    assert yp.age_days == 44
    assert yp.arrival_date == HTDatetime.from_calendar(year=2022, month=1, day=16,
                                                       hour=16, minute=17, second=0)
    assert yp.can_be_promoted_in == -828
    assert yp.number == 100
    assert yp.statement is None
    assert yp.native_country_id == 5
    assert yp.native_country_name == 'France'
    assert yp.cards == 0
    assert yp.injury_level == -1
    assert yp.specialty == 0
    assert yp.career_goals == 0
    assert yp.career_hattricks == 0
    assert yp.league_goals == 0
    assert yp.friendly_goals == 0

    assert yp.owning_youth_team.id == 2942691
    assert yp.owning_youth_team.name == "Les Petits Chapelains"
    assert yp.owning_youth_team.league_id == 225490

    assert yp.owning_youth_team.senior_team.id == 1165592
    assert yp.owning_youth_team.senior_team.name == "Les Poitevins de La Chapelle"

    assert yp.skills.keeper.skill.is_available is False
    assert yp.skills.keeper.skill.is_max_reached is False
    assert yp.skills.keeper.skill.may_unlock is False
    assert yp.skills.keeper.skill.level is None

    assert yp.skills.keeper.skill_max.is_available is False
    assert yp.skills.keeper.skill_max.may_unlock is False
    assert yp.skills.keeper.skill_max.level is None

    assert yp.skills.defender.skill.is_available is True
    assert yp.skills.defender.skill.is_max_reached is True
    assert yp.skills.defender.skill.may_unlock is None
    assert yp.skills.defender.skill.level == 3

    assert yp.skills.defender.skill_max.is_available is True
    assert yp.skills.defender.skill_max.may_unlock is None
    assert yp.skills.defender.skill_max.level == 3

    assert yp.skills.playmaker.skill.is_available is False
    assert yp.skills.playmaker.skill.is_max_reached is False
    assert yp.skills.playmaker.skill.may_unlock is True
    assert yp.skills.playmaker.skill.level is None

    assert yp.skills.playmaker.skill_max.is_available is False
    assert yp.skills.playmaker.skill_max.may_unlock is True
    assert yp.skills.playmaker.skill_max.level is None

    assert yp.skills.winger.skill.is_available is True
    assert yp.skills.winger.skill.is_max_reached is False
    assert yp.skills.winger.skill.may_unlock is None
    assert yp.skills.winger.skill.level == 1

    assert yp.skills.winger.skill_max.is_available is False
    assert yp.skills.winger.skill_max.may_unlock is True
    assert yp.skills.winger.skill_max.level is None

    assert yp.skills.passing.skill.is_available is False
    assert yp.skills.passing.skill.is_max_reached is False
    assert yp.skills.passing.skill.may_unlock is True
    assert yp.skills.passing.skill.level is None

    assert yp.skills.passing.skill_max.is_available is False
    assert yp.skills.passing.skill_max.may_unlock is True
    assert yp.skills.passing.skill_max.level is None

    assert yp.skills.scorer.skill.is_available is False
    assert yp.skills.scorer.skill.is_max_reached is False
    assert yp.skills.scorer.skill.may_unlock is False
    assert yp.skills.scorer.skill.level is None

    assert yp.skills.scorer.skill_max.is_available is True
    assert yp.skills.scorer.skill_max.may_unlock is None
    assert yp.skills.scorer.skill_max.level == 3

    assert yp.skills.set_pieces.skill.is_available is False
    assert yp.skills.set_pieces.skill.is_max_reached is False
    assert yp.skills.set_pieces.skill.may_unlock is False
    assert yp.skills.set_pieces.skill.level is None

    assert yp.skills.set_pieces.skill_max.is_available is False
    assert yp.skills.set_pieces.skill_max.may_unlock is False
    assert yp.skills.set_pieces.skill_max.level is None


def test_get_not_owned_youth_player(mocked_chpp):
    ypd = mocked_chpp.xml_youth_player_details(youth_player_id=384579961)
    assert isinstance(ypd, YouthPlayerDetails)
    assert ypd.skills is None


def test_get_youth_player_midnight_arrival(mocked_chpp):
    ypd = mocked_chpp.xml_youth_player_details(youth_player_id=395385356)
    assert isinstance(ypd, YouthPlayerDetails)
    assert ypd.arrival_date == HTDatetime.from_calendar(2025, 8, 4, 0, 0, 0)


def test_get_youth_player_currently_playing(mocked_chpp):
    ypd = mocked_chpp.xml_youth_player_details(youth_player_id=395583001)
    assert isinstance(ypd, YouthPlayerDetails)
