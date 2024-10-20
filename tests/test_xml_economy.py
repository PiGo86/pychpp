def test_xml_economy(mocked_chpp):

    eco = mocked_chpp.xml_economy()
    t = eco.team

    assert t.id == 1165592
    assert t.name == 'Les Poitevins de La Chapelle'

    assert t.cash == 60_613_476
    assert t.expected_cash == 62_261_366
    assert t.sponsors_popularity == 8
    assert t.supporters_popularity == 10
    assert t.fan_club_size == 1_976

    assert t.income_spectators == 3_260_290
    assert t.income_sponsors == 670_000
    assert t.income_sponsors_bonus == 360_000
    assert t.income_financial == 0
    assert t.income_sold_players == 0
    assert t.income_sold_players_commission == 0
    assert t.income_sum == 4_290_290

    assert t.costs_arena == 334_300
    assert t.costs_players == 1_455_300
    assert t.costs_financial == 0
    assert t.costs_staff == 652_800
    assert t.costs_bought_players == 0
    assert t.costs_arena_building == 0
    assert t.costs_youth == 200_000
    assert t.costs_sum == 2_642_400

    assert t.expected_weeks_total == 1_647_890

    assert t.last_income_spectators == 63_129
    assert t.last_income_sponsors == 670_000
    assert t.last_income_financial == 0
    assert t.last_income_sold_players == 0
    assert t.last_income_sold_players_commission == 559_999
    assert t.last_income_sum == 1_653_128

    assert t.last_costs_arena == 334_300
    assert t.last_costs_players == 1_455_300
    assert t.last_costs_financial == 0
    assert t.last_costs_staff == 652_800
    assert t.last_costs_bought_players == 0
    assert t.last_costs_arena_building == 0
    assert t.last_costs_youth == 200_000
    assert t.last_costs_sum == 2_642_400

    assert t.last_weeks_total == -989_272
