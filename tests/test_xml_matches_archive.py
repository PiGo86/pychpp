from pychpp.fixtures.ht_datetime import HTDatetime
from pychpp.models.xml.matches_archive import MatchesArchive, MatchItem, MatchItemTeam


def test_get_current_user_matches_archive(chpp):
    ma1 = chpp.xml_matches_archive()
    assert isinstance(ma1, MatchesArchive)

    m = ma1.matches[0]
    assert isinstance(m, MatchItem)
    assert isinstance(m.home_team, MatchItemTeam)
    assert isinstance(m.home_team.id, int)
    assert isinstance(m.home_team.name, str)

    ma2 = chpp.xml_matches_archive(
        team_id=1165592,
        first_match_date=HTDatetime.from_calendar(2020, 1, 1),
        last_match_date=HTDatetime.from_calendar(2020, 3, 31),
    )

    assert isinstance(ma2, MatchesArchive)
    assert ma2.matches[0].id == 652913955
    assert ma2.matches[0].home_team.name == "Les Poitevins de La Chapelle"
    assert ma2.matches[0].away_team.name == "FC Traversonne"
    assert ma2.matches[0].date == HTDatetime.from_calendar(2020, 1, 1, 15, 10, 0)
    assert ma2.matches[0].type_id == 5
    assert ma2.matches[0].context_id == 0
    assert ma2.matches[0].rule_id == 0
    assert ma2.matches[0].cup.level == 0
    assert ma2.matches[0].cup.level_index == 0
    assert ma2.matches[0].home_goals == 2
    assert ma2.matches[0].away_goals == 0

    for m in ma2.matches:
        assert (HTDatetime.from_calendar(2020, 1, 1)
                <= m.date <=
                HTDatetime.from_calendar(2020, 3, 31))
