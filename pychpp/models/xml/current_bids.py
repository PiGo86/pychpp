from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestCurrentBids(HTModel):
    """
    Current Bids - Request arguments
    """
    SOURCE_FILE = 'currentbids'
    LAST_VERSION = '1.0'

    _r_action_type: Optional[str] = HTInitVar('actionType', init_arg='action_type')
    _r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')
    _r_transfer_id: Optional[int] = HTInitVar('transferId', init_arg='transfer_id')
    _r_tracking_type_id: Optional[int] = HTInitVar('trackingTypeId', init_arg='tracking_type_id')


class CurrentBids(RequestCurrentBids):
    """
    Current Bids
    """
    team_id: int = HTField('TeamId')
    selling_bids: Optional[List['BidItem']] = HTField('BidItems[@TrackingTypeID="1"]',
                                                      items='BidItem')
    buying_bids: Optional[List['BidItem']] = HTField('BidItems[@TrackingTypeID="2"]',
                                                     items='BidItem')
    mother_club_bids: Optional[List['BidItem']] = HTField('BidItems[@TrackingTypeID="3"]',
                                                          items='BidItem')
    previous_team_bids: Optional[List['BidItem']] = HTField('BidItems[@TrackingTypeID="4"]',
                                                            items='BidItem')
    hot_listed_bids: Optional[List['BidItem']] = HTField('BidItems[@TrackingTypeID="5"]',
                                                         items='BidItem')
    losing_bids: Optional[List['BidItem']] = HTField('BidItems[@TrackingTypeID="8"]',
                                                     items='BidItem')
    finished_bids: Optional[List['BidItem']] = HTField('BidItems[@TrackingTypeID="9"]',
                                                       items='BidItem')
    prospects_bids: Optional[List['BidItem']] = HTField('BidItems[@TrackingTypeID="10"]',
                                                        items='BidItem')


class BidItem(HTModel):
    """
    Current Bids -> Bids -> Bid item
    """
    transfer_id: int = HTField('TransferId')
    player_id: int = HTField('PlayerId')
    player_name: str = HTField('PlayerName')
    highest_bid: 'HighestBid' = HTField('HighestBid')
    deadline: datetime = HTField('Deadline')


class HighestBid(HTModel):
    """
    Current Bids -> Bids -> Bid item -> Highest Bid
    """
    amount: int = HTField('Amount')
    team_id: int = HTField('TeamId')
    team_name: str = HTField('TeamName')
