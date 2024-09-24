from pychpp.models.xml.transfers_team import TransfersTeam, TransfersTransferItem
from pychpp.fixtures.ht_datetime import HTDatetime


def test_get_team_transfers(mocked_chpp):

    transfers_team = mocked_chpp.xml_transfers_team(team_id=940, page_index=1)

    assert isinstance(transfers_team, TransfersTeam)

    assert transfers_team.team.id == 940
    assert transfers_team.team.name == "FC Vanilla"
    assert transfers_team.team.activated_date == (
        HTDatetime.from_calendar(2003, 2, 1, 3, 15, 0))
    assert transfers_team.stats.total_sum_of_buys == 572_579_730
    assert transfers_team.stats.total_sum_of_sales == 569_274_290
    assert transfers_team.stats.number_of_buys == 65
    assert transfers_team.stats.number_of_sales == 144

    assert transfers_team.transfers.page_index == 1
    assert transfers_team.transfers.pages == 9
    assert transfers_team.transfers.start_date == HTDatetime.from_calendar(
        2008, 10, 11, 16, 5, 0,
    )
    assert transfers_team.transfers.end_date == HTDatetime.from_calendar(
        2009, 10, 31, 9, 44, 0,
    )

    assert isinstance(transfers_team.transfers.transfer_items, list)
    assert len(transfers_team.transfers.transfer_items) == 25

    transfer_item = transfers_team.transfers.transfer_items[10]
    assert isinstance(transfer_item, TransfersTransferItem)
    assert transfer_item.id == 177997172
    assert transfer_item.deadline == HTDatetime.from_calendar(2009, 6, 26,
                                                              21, 21, 0)
    assert transfer_item.type == "S"
    assert transfer_item.price == 10_000_000
    assert transfer_item.player.id == 0
    assert transfer_item.player.name == "André da Costa"
    assert transfer_item.player.tsi == 10_260
    assert transfer_item.buyer.id == 494228
    assert transfer_item.buyer.name == "LOS CARA DEPERCHAS"
    assert transfer_item.seller.id == 940
    assert transfer_item.seller.name == "FC Vanilla"
