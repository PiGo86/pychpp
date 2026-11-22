from pychpp.fixtures.ht_datetime import HTDatetime
from pychpp.models.xml.team_history import TeamHistory


def test_team_history_version_1_0(mocked_chpp):

    th = mocked_chpp.xml_team_history(team_id=1165592, version='1.0')

    assert isinstance(th, TeamHistory)
    assert th.id == 1165592
    assert th.name == 'Les Poitevins de La Chapelle'
    assert th.league.id == 5
    assert th.league.name == 'France'
    assert th.founded_date == HTDatetime.from_calendar(year=2017, month=9, day=9,
                                                       hour=17, minute=9, second=0)

    assert len(th.history) == 30

    season = th.history[0]
    assert season.index == 0
    assert season.season_number == 66
    assert season.league_level_unit_id == 73092
    assert season.league_level_unit_name == 'VII.277'
    assert season.league_level == 7
    assert season.position == 3
    assert season.points == 28
    assert season.goals_for == 34
    assert season.goals_against == 18
    assert season.cup_round == -1
    assert season.cup_rounds_left == -1

    last = th.history[-1]
    assert last.index == 29
    assert last.season_number == 95
    assert last.league_level_unit_name == 'VI.893'
    assert last.position == 8

    assert len(th.trophies) == 3

    trophy = th.trophies[0]
    assert trophy.type_id == 17
    assert trophy.season == 79
    assert trophy.league_level == 5
    assert trophy.league_level_unit_id == 21672
    assert trophy.league_level_unit_name == 'V.96'
    assert trophy.gained_date == HTDatetime.from_calendar(year=2021, month=12, day=4,
                                                          hour=2, minute=59, second=0)
    assert trophy.image_url == '/App_Themes/Standard/Images/Trophies/v.png'
    assert trophy.cup_league_level is None
    assert trophy.cup_level is None
    assert trophy.cup_level_index is None
