def test_training_events(mocked_chpp):

    te = mocked_chpp.xml_training_events(456732884)

    assert te.user_supporter_tier == 'none'

    assert te.player.id == 456732884
    assert te.player.training_events_available is True
    assert isinstance(te.player.training_events, list)

    ev = te.player.training_events[0]
    assert ev.index == 0
    assert ev.skill_id == 6
    assert ev.old_level == 11
    assert ev.new_level == 12
    assert ev.season == 88
    assert ev.match_round == 13
    assert ev.day_number == 5
