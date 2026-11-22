from pychpp.fixtures.ht_datetime import HTDatetime
from pychpp.models.xml.match_details import MatchDetails


def test_get_future_match_details(mocked_chpp):
    md = mocked_chpp.xml_match_details(744337584, version='3.1')

    assert isinstance(md, MatchDetails)
    assert md.match.finished_date is None


def test_get_htointegrated_match_details(mocked_chpp):
    md = mocked_chpp.xml_match_details(36370661, 'htointegrated', match_events=True, version='3.1')

    assert isinstance(md, MatchDetails)
    assert md.match.officials is None


def test_match_details_version_3_2(mocked_chpp):
    md = mocked_chpp.xml_match_details(775863574, match_events=True)

    assert isinstance(md, MatchDetails)
    match = md.match
    assert match.id == 775863574
    assert match.type == 3
    assert match.context_id == 1344
    assert match.rule_id == 0
    assert match.cup_level == 2
    assert match.cup_level_index == 1
    assert match.date == HTDatetime.from_calendar(2026, 11, 18, 15, 15, 0)
    assert match.finished_date == HTDatetime.from_calendar(2026, 11, 18, 17, 2, 0)
    assert match.added_minutes == 2

    home = match.home_team
    assert home.id == 1165592
    assert home.name == 'Les Poitevins de La Chapelle'
    assert home.goals == 0
    # since version 3.2
    assert home.has_replay is False
    assert home.nr_of_replays == 0

    away = match.away_team
    assert away.id == 3478697
    assert away.name == 'Fc Drouais'
    assert away.goals == 5
    # HasReplay/NrOfReplays are only shown to the owner of the team
    assert away.has_replay is None
    assert away.nr_of_replays is None

    # ExpectedResult is only present when replay data is available to the user
    assert match.expected_result is None

    goal = match.goals[0]
    assert goal.player_id == 517075778
    assert goal.player_name == 'Robin Rouat'
    assert goal.team_id == 3478697
    assert goal.home_goals_after == 0
    assert goal.away_goals_after == 1
    assert goal.minute == 20
    assert goal.match_part == 1

    booking = match.bookings[0]
    assert booking.player_id == 517075783
    assert booking.player_name == 'Raphaël Garcia'
    assert booking.team_id == 3478697
    assert booking.type == 1
    assert booking.minute == 30
    assert booking.match_part == 1

    injury = match.injuries[0]
    assert injury.player_id == 422524621
    assert injury.player_name == 'Étienne Asselin'
    assert injury.team_id == 1165592
    assert injury.type == 1
    assert injury.minute == 15
    assert injury.match_part == 1

    assert match.possession.first_half_home == 35
    assert match.possession.first_half_away == 65
    assert match.possession.second_half_home == 34
    assert match.possession.second_half_away == 66

    event = match.events[0]
    assert event.minute == 0
    assert event.match_part == 0
    assert event.type_id == 32
    assert event.variation == 5
    assert event.subject_team_id == 50000
    assert event.subject_player_id == 1162154
    assert event.object_player_id == 1970
    assert event.text[0:14] == 'La météo était'

    assert match.arena.id == 1162154
    assert match.arena.name == 'Stade de La Chapelle'
    assert match.arena.weather_id == 2
    assert match.arena.sold.total == 1970
    assert match.arena.sold.terraces == 1344
    assert match.arena.sold.vip == 21

    assert match.officials.referee.id == 493211977
    assert match.officials.referee.name == 'Saymen La Roche'
