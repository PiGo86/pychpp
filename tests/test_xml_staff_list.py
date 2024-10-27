from pychpp.fixtures.ht_datetime import HTDatetime


def test_staff_list(mocked_chpp):

    sl = mocked_chpp.xml_staff_list()

    assert sl.trainer.id == 421746800
    assert sl.trainer.name == "Quentin Lavigne"
    assert sl.trainer.age == 51
    assert sl.trainer.age_days == 64
    assert sl.trainer.contract_date == HTDatetime.from_calendar(
        2021, 5, 5, 10, 20)
    assert sl.trainer.cost == 2_500
    assert sl.trainer.country_id == 5
    assert sl.trainer.type == 2
    assert sl.trainer.leadership == 2
    assert sl.trainer.skill_level == 4
    assert sl.trainer.status == 1

    staff_member = sl.staff_members[2]
    assert staff_member.id == 474265
    assert staff_member.name == "Frédéric Aubert"
    assert staff_member.type == 2
    assert staff_member.level == 5
    assert staff_member.hired_date == HTDatetime.from_calendar(2019, 11, 4, 17, 37)
    assert staff_member.cost == 163_200
    assert staff_member.hof_player_id == 0
