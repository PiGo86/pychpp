def test_staff_avatars(mocked_chpp):

    sa = mocked_chpp.xml_staff_avatars()

    assert sa.trainer.id == 421746800
    assert sa.trainer.avatar.background_image == '/Img/Avatar/backgrounds/card1.png'
    assert sa.trainer.avatar.layers[0].x == 9
    assert sa.trainer.avatar.layers[0].y == 10
    assert sa.trainer.avatar.layers[0].image == '/Img/Avatar/backgrounds/bg_blue.png'

    staff_member = sa.staff_members[0]
    assert staff_member.id == 480936
    assert staff_member.avatar.background_image == '/Img/Avatar/backgrounds/card1.png'
    assert staff_member.avatar.layers[0].x == 9
    assert staff_member.avatar.layers[0].y == 10
    assert staff_member.avatar.layers[0].image == '/Img/Avatar/backgrounds/bg_blue.png'
