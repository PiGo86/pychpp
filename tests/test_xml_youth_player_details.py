from .fixtures import mocked_chpp


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