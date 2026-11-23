"""Tests for the `stafflist.xml` CHPP file parsing."""

from pychpp.fixtures.ht_datetime import HTDatetime


def test_staff_list(mocked_chpp):
    sl = mocked_chpp.xml_staff_list(version='1.2')

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


def test_staff_list_version_1_3(mocked_chpp):
    sl = mocked_chpp.xml_staff_list(version='1.3')

    assert sl.trainer.id == 421746800
    assert sl.trainer.name == "Quentin Lavigne"
    assert sl.total_staff_members == 5
    assert sl.total_cost == 655_300

    staff_member = sl.staff_members[0]
    assert staff_member.id == 480936
    assert staff_member.name == "Kenan Bonnet"
    assert staff_member.contract_expires == HTDatetime.from_calendar(2027, 1, 5, 19, 36)

    staff_member = sl.staff_members[2]
    assert staff_member.id == 474265
    assert staff_member.name == "Frédéric Aubert"
    assert staff_member.type == 2
    assert staff_member.cost == 163_200
    assert staff_member.hof_player_id == 0
    assert staff_member.contract_expires == HTDatetime.from_calendar(2026, 11, 23, 17, 37)
