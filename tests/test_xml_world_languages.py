def test_world_languages(mocked_chpp):

    wl = mocked_chpp.xml_world_languages()

    assert wl.language_list[-1].id == 12
    assert wl.language_list[-1].name == 'Japanese'
