from pychpp.fixtures.ht_datetime import HTDatetime


def test_xml_fans(mocked_chpp):

    fans = mocked_chpp.xml_fans()

    t = fans.team
    assert t.id == 1165592
    assert t.fan_club_id == 656629
    assert t.fan_club_name == 'Les Exilés du Poitou'
    assert t.fan_mood == 10
    assert t.members == 1_976
    assert t.fan_season_expectation == 5

    played_m = t.played_matches
    assert isinstance(played_m, list)

    pm = played_m[0]
    assert pm.id == 739348980
    assert pm.home_team.id == 1165592
    assert pm.home_team.name == 'Les Poitevins de La Chapelle'
    assert pm.away_team.id == 2233206
    assert pm.away_team.name == 'bastia en force'
    assert pm.date == HTDatetime.from_calendar(2024, 9, 21, 21, 0, 0)
    assert pm.type == 1
    assert pm.home_goals == 4
    assert pm.away_goals == 0
    assert pm.fan_match_expectation == 7
    assert pm.fan_mood_after_match == 10
    assert pm.weather == 2
    assert pm.sold_seats == 35_148

    upcoming_m = t.upcoming_matches
    assert isinstance(upcoming_m, list)

    um = upcoming_m[0]
    assert um.id == 739349000
    assert um.home_team.id == 1751435
    assert um.home_team.name == 'Kermouster Atlethic Club 2'
    assert um.away_team.id == 1165592
    assert um.away_team.name == 'Les Poitevins de La Chapelle'
    assert um.date == HTDatetime.from_calendar(2024, 10, 26, 21, 0, 0)
    assert um.type == 1
    assert um.fan_match_expectation == 8
