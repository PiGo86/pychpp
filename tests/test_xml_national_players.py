def test_national_players(mocked_chpp):

    ntp = mocked_chpp.xml_national_players(team_id=3004)

    assert ntp.user_supporter_tier == 'none'
    assert ntp.team_id == 3004
    assert ntp.team_name == 'France'
    assert ntp.action_type == 'view'

    player = ntp.players[0]
    assert player.id == 448825568
    assert player.name == 'Abdelmouqit Selawi'
    assert player.cards == 0
    assert player.specialty == 5
    assert player.avatar.background_image == '/Img/Avatar/backgrounds/card1.png'
    assert player.avatar.layer.x == 9
    assert player.avatar.layer.y == 10
    assert player.avatar.layer.image == '/Img/Avatar/backgrounds/bg_blue.png'
