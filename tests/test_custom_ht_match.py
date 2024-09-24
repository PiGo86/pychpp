import re

from pychpp.fixtures.ht_datetime import HTDatetime
from pychpp.models.custom.ht_match import HTMatch

from .conftest import MATCH_PATTERN


def test_get_match(mocked_chpp):

    m = mocked_chpp.match(547513790, events=True)

    assert isinstance(m, HTMatch)
    assert m.id == 547513790

    m_match = re.match(MATCH_PATTERN, m.url)
    assert m_match is not None
    assert int(m_match.group(1)) == 547513790

    assert m.date == HTDatetime.from_calendar(2015, 12, 19, 21, 0)
    assert m.home_team.name == "Olympique Mig"
    assert m.away_team.name == "Camden County Jerks"
    assert m.added_minutes == 0
    assert m.arena.id == 1162154
    assert len(m.events) == 25
    assert m.events[14].minute == 72
    assert m.events[14].match_part == 2
    assert m.events[14].type_id == 285
    assert m.events[14].variation == 3
    assert m.events[14].subject_team_id == 292366
    assert m.events[14].subject_player_id == 373737451
    assert m.events[14].object_player_id == 314946894
    assert "coup franc" in m.events[14].text
