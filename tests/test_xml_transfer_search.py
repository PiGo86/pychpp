from pychpp.fixtures.ht_datetime import HTDatetime


def test_transfer_search(mocked_chpp):

    ts = mocked_chpp.xml_transfer_search(age_min=20, age_max=22,
                                         skill_type_1=8,
                                         min_skill_value_1=7, max_skill_value_1=9)

    assert ts.item_count == -1
    assert ts.page_size == 25
    assert ts.page_index == 0

    pl = ts.transfer_results[0]
    assert pl.id == 480249808
    assert pl.first_name == 'Gianrico'
    assert pl.nick_name is None
    assert pl.last_name == 'Borgato'
    assert pl.native_country_id == 4
    assert pl.asking_price == 1_500_000
    assert pl.deadline == HTDatetime.from_calendar(2024, 10, 28, 21, 31, 33)
    assert pl.highest_bid == 0
    assert pl.bidder_team.id is None
    assert pl.bidder_team.name is None

    details = pl.details
    assert details.age == 22
    assert details.age_days == 22
    assert details.salary == 7_900
    assert details.tsi == 5_610
    assert details.player_form == 6
    assert details.experience == 2
    assert details.leadership == 5
    assert details.specialty == 0
    assert details.cards == 0
    assert details.injury_level == -1
    assert details.stamina_skill == 8
    assert details.keeper_skill == 1
    assert details.playmaker_skill == 8
    assert details.scorer_skill == 7
    assert details.passing_skill == 5
    assert details.winger_skill == 3
    assert details.defender_skill == 5
    assert details.set_pieces_skill == 4

    seller = details.seller_team
    assert seller.id == 1735412
    assert seller.name == 'A. C. Adelscott'
    assert seller.league_id == 4
