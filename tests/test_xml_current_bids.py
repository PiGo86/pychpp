from pychpp.fixtures.ht_datetime import HTDatetime


def test_current_bids(mocked_chpp):

    bids = mocked_chpp.xml_current_bids()

    assert bids.team_id == 1165592

    assert bids.selling_bids == []
    assert bids.mother_club_bids == []
    assert bids.previous_team_bids == []
    assert bids.hot_listed_bids == []
    assert bids.losing_bids == []
    assert bids.finished_bids == []
    assert bids.prospects_bids == []

    buying = bids.buying_bids
    assert len(buying) == 1

    bid = buying[0]
    assert bid.transfer_id == 375038517
    assert bid.player_id == 464753259
    assert bid.player_name == 'Władysław Szarafin'
    assert bid.highest_bid.amount == 10_000
    assert bid.highest_bid.team_id == 1165592
    assert bid.highest_bid.team_name == 'Les Poitevins de La Chapelle'
    assert bid.deadline == HTDatetime.from_calendar(2024, 10, 21, 23, 4, 45)
