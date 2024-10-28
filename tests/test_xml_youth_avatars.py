def test_youth_avatars(mocked_chpp):

    ya = mocked_chpp.xml_youth_avatars()

    assert ya.youth_team_id == 2942691

    pl = ya.youth_players[0]
    assert pl.id == 299306192
    assert pl.avatar.background_image == '/Img/Avatar/backgrounds/card1.png'
    assert pl.avatar.layers[0].x == 9
    assert pl.avatar.layers[0].y == 10
    assert pl.avatar.layers[0].image == '/Img/Avatar/backgrounds/y_bg_blue.png'
