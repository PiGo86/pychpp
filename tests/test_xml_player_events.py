from pychpp.fixtures.ht_datetime import HTDatetime


def test_player_events(mocked_chpp):

    pe = mocked_chpp.xml_player_events(player_id=445879103)

    assert pe.user_supporter_tier == 'none'
    assert pe.player.id == 445879103
    assert isinstance(pe.player.events, list)

    ev = pe.player.events[0]
    assert ev.date == HTDatetime.from_calendar(2024, 9, 7, 2, 37)
    assert ev.type_id == 42
    assert ev.text == ('A fait partie de l\'équipe qui a été championne de '
                       '<a href="/World/Series/?LeagueLevelUnitID=703">Championnat</a> '
                       '(<a href="/World/Leagues/League.aspx?LeagueID=5">France</a>) '
                       'lors de la saison 88.')
