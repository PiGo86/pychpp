def test_league_levels(mocked_chpp):
    league_levels = mocked_chpp.xml_league_levels(league_id=5)

    assert league_levels.id == 5
    assert league_levels.season == 89
    assert league_levels.nr_of_league_levels == 6

    levels = league_levels.levels
    assert isinstance(levels, list)

    level = levels[2]
    assert level.league_level == 3
    assert level.league_level_unit_id_list == ('708,709,710,711,712,713,714,715,'
                                               '716,717,718,719,720,721,722,723')
    assert level.nr_of_league_level_units == 16
    assert level.nr_of_teams == 128
    assert level.nr_of_shared_promotion_slots_per_series == 1
    assert level.nr_of_direct_promotion_slots_per_series == 0
    assert level.nr_of_qualification_promotion_slots_per_series == 0
    assert level.nr_of_direct_demotion_slots_per_series == 2
    assert level.nr_of_qualification_demotion_slots_per_series == 2
