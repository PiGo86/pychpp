def test_get_avatars(mocked_chpp):

    avatars = mocked_chpp.xml_avatars(action_type='players', team_id=960935)

    assert avatars.team.id == 960935

    players = avatars.team.players
    assert isinstance(players, list)

    player = players[2]
    assert player.id == 458114412
    assert player.avatar.background_image == '/Img/Avatar/backgrounds/card1.png'

    layers = player.avatar.layers
    assert isinstance(layers, list)

    layer = layers[0]
    assert layer.x == 9
    assert layer.y == 10
    assert layer.image == '/Img/Avatar/backgrounds/bg_blue.png'
