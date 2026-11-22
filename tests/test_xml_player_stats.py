from pychpp.fixtures.ht_datetime import HTDatetime
from pychpp.models.xml.player_stats import PlayerStats


def test_player_stats_version_1_0(mocked_chpp):

    ps = mocked_chpp.xml_player_stats(player_id=430759322, version='1.0')

    assert isinstance(ps, PlayerStats)
    assert ps.id == 430759322
    assert ps.first_name == 'Frédérik'
    assert ps.nick_name is None
    assert ps.last_name == 'Rivière'
    assert ps.number == 1
    assert ps.owning_team.id == 1165592
    assert ps.owning_team.name == 'Les Poitevins de La Chapelle'
    assert ps.owning_team.league_id == 5
    assert len(ps.match_stats) == 35

    match = ps.match_stats[0]
    assert match.id == 773525893
    assert match.type == 1
    assert match.source_system == 'Hattrick'
    assert match.date == HTDatetime.from_calendar(year=2026, month=11, day=21,
                                                  hour=21, minute=10, second=0)
    assert match.home_team.name == 'FC TAIZ 2'
    assert match.away_team.name == 'Les Poitevins de La Chapelle'
    assert match.is_walkover is False
    assert match.age == 51
    assert match.age_days == 69
    assert match.tsi == 0
    assert match.form == 3
    assert match.stamina is None
    assert match.loyalty == 20
    assert match.experience == 5
    assert match.goals == 0
    assert match.yellow_cards == 0
    assert match.red_cards == 0
    assert match.injury_level == 999
    assert match.played_minutes == 0
    assert match.rating == 0.0
    assert match.rating_end_of_game == 0.0
    assert match.positions == []

    played = next(m for m in ps.match_stats if m.played_minutes > 0)
    assert played.id == 763492533
    assert played.played_minutes == 94
    assert played.rating == 0.5
    assert played.rating_end_of_game == 0.0
    assert played.stamina == 2
    assert played.injury_level == 0
    assert [(p.position_code, p.minutes) for p in played.positions] == [(111, 94)]
