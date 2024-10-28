from pychpp.fixtures.ht_datetime import HTDatetime


def test_transfers_player(mocked_chpp):

    tp = mocked_chpp.xml_transfers_player(427947863)

    assert tp.start_date == HTDatetime.from_calendar(2018, 10, 17, 23, 55)
    assert tp.end_date == HTDatetime.from_calendar(2018, 9, 9, 18, 34)
    assert tp.player.id == 427947863
    assert tp.player.name == 'Batıkan Gündoğan'

    tr = tp.transfers[1]
    assert tr.id == 330572184
    assert tr.deadline == HTDatetime.from_calendar(2018, 9, 9, 18, 34)
    assert tr.buyer.id == 121595
    assert tr.buyer.name == 'Linares Club de Fútbol'
    assert tr.seller.id == 588379
    assert tr.seller.name == "L'os pepettes"
    assert tr.price == 18_550_000
