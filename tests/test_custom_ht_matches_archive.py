import re

from pychpp.fixtures.ht_datetime import HTDatetime

from .conftest import MATCH_ARCHIVE_PATTERN, MATCH_PATTERN


def test_get_other_user_matches_archives(chpp):
    ma1 = chpp.matches_archive(
        id_=1755906,
        first_match_date=HTDatetime.from_calendar(2018, 4, 10),
        last_match_date=HTDatetime.from_calendar(2018, 4, 30),
    )

    assert re.match(MATCH_ARCHIVE_PATTERN, ma1.url)

    for m in ma1:
        assert (HTDatetime.from_calendar(2018, 4, 10)
                <= m.date <=
                HTDatetime.from_calendar(2018, 6, 30))
        assert 1755906 in (m.home_team.id, m.away_team.id)
        assert re.match(MATCH_PATTERN, m.url)

    ma2 = chpp.matches_archive(id_=1755906,
                               season=60,
                               )

    assert re.match(MATCH_ARCHIVE_PATTERN, ma2.url)

    for m in ma2:
        assert (HTDatetime.from_calendar(2015, 10, 26)
                <= m.date <=
                HTDatetime.from_calendar(2016, 2, 14))
        assert 1755906 in (m.home_team.id, m.away_team.id)
        assert re.match(MATCH_PATTERN, m.url)
