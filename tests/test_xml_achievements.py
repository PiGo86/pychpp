from pychpp import CHPP
from pychpp.fixtures.ht_datetime import HTDatetime
from pychpp.models.xml.achievements import Achievements


def test_achievements_version_1_2(mocked_chpp: 'CHPP'):
    a = mocked_chpp.xml_achievements(user_id=1728698, version='1.2')

    assert isinstance(a, Achievements)
    assert a.max_points == 740
    assert len(a.achievements) == 46

    ach = a.achievements[0]
    assert ach.type_id == 1
    assert ach.title == 'La course au classement'
    assert ach.category_id == 2
    assert ach.event_date == HTDatetime.from_calendar(2021, 12, 20, 5, 6, 0)
    assert ach.points == 40
    assert ach.multilevel is True
    assert ach.rank == 4
    assert ach.number_of_events == 79278

    # fields added in >=1.3 / >=1.4 are not available
    assert ach.completed is None
    assert ach.max_points is None
    assert ach.progress_value is None
    assert ach.progress_value_date is None
    assert ach.current_variation is None
    assert ach.next_variation is None
    assert ach.category_group_id is None


def test_achievements_version_1_3(mocked_chpp: 'CHPP'):
    a = mocked_chpp.xml_achievements(user_id=1728698, version='1.3')

    assert a.max_points == 740
    assert len(a.achievements) == 46

    # multilevel achievement with variations
    ach = a.achievements[0]
    assert ach.type_id == 1
    assert ach.completed is False
    assert ach.max_points == 100
    assert ach.progress_value == 194
    assert ach.progress_value_date == HTDatetime.from_calendar(2022, 1, 10, 5, 5, 0)
    assert ach.current_variation.rank == 4
    assert ach.current_variation.value_to_achieve == 500
    assert ach.current_variation.points == 40
    assert ach.next_variation.rank == 3
    assert ach.next_variation.value_to_achieve == 100
    assert ach.next_variation.points == 45

    # non-multilevel achievement: no progress/variation
    simple = next(x for x in a.achievements if not x.multilevel)
    assert simple.type_id == 2
    assert simple.completed is True
    assert simple.max_points == 10
    assert simple.progress_value is None
    assert simple.current_variation is None
    assert simple.next_variation is None

    # CategoryGroupID is only available from 1.4
    assert ach.category_group_id is None


def test_achievements_version_1_4(mocked_chpp: 'CHPP'):
    a = mocked_chpp.xml_achievements(user_id=1728698, version='1.4')

    assert a.max_points == 740
    assert len(a.achievements) == 46

    ach = a.achievements[0]
    assert ach.type_id == 1
    assert ach.category_id == 2
    assert ach.category_group_id == 1
    assert ach.completed is False
    assert ach.max_points == 100
    assert ach.progress_value == 194
    assert ach.progress_value_date == HTDatetime.from_calendar(2022, 1, 10, 5, 5, 0)
    assert ach.current_variation.rank == 4
    assert ach.current_variation.value_to_achieve == 500
    assert ach.current_variation.points == 40
    assert ach.next_variation.rank == 3
    assert ach.next_variation.value_to_achieve == 100
    assert ach.next_variation.points == 45

    assert all(x.category_group_id is not None for x in a.achievements)
