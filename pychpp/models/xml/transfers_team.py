from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestTransfersTeam(HTModel):
    """
    Transfers Team - Request arguments
    """
    SOURCE_FILE = 'transfersteam'
    LAST_VERSION = "1.2"

    _r_team_id: Optional[int] = HTInitVar('teamID', init_arg='team_id')
    _r_page_index: Optional[int] = HTInitVar('pageIndex', init_arg='page_index')


class TransfersTeam(RequestTransfersTeam):
    """
    Transfers Team
    """
    team: 'Team' = HTField('Team')
    stats: 'Stats' = HTField('Stats')
    transfers: 'Transfers' = HTField('Transfers')


class Team(HTModel):
    """
    Transfers Team -> Team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    activated_date: datetime = HTField('ActivatedDate')


class Stats(HTModel):
    """
    Transfers Team -> Stats
    """
    total_sum_of_buys: int = HTField('TotalSumOfBuys')
    total_sum_of_sales: int = HTField('TotalSumOfSales')
    number_of_buys: int = HTField('NumberOfBuys')
    number_of_sales: int = HTField('NumberOfSales')


class Transfers(HTModel):
    """
    Transfers Team -> Transfers
    """
    page_index: int = HTField('PageIndex')
    pages: int = HTField('Pages')
    start_date: datetime = HTField('StartDate')
    end_date: datetime = HTField('EndDate')
    transfer_items: List['TransfersTransferItem'] = HTField('.', items='Transfer')


class TransfersTransferItem(HTModel):
    """
    Transfers Team -> Transfers -> Transfer items -> Transfer item
    """
    id: int = HTField('TransferID')
    deadline: datetime = HTField('Deadline')
    type: str = HTField('TransferType')
    price: int = HTField('Price')
    player: 'TransfersTransferItemPlayer' = HTField('Player')
    buyer: 'TransfersTransferItemBuyer' = HTField('Buyer')
    seller: 'TransfersTransferItemSeller' = HTField('Seller')


class TransfersTransferItemPlayer(HTModel):
    """
    Transfers Team -> Transfers -> Transfer items -> Transfer item -> Player
    """
    id: int = HTField('PlayerID')
    name: str = HTField('PlayerName')
    tsi: int = HTField('TSI')


class TransfersTransferItemBuyer(HTModel):
    """
    Transfers Team -> Transfers -> Transfer items -> Transfer item -> Buyer
    """
    id: int = HTField('BuyerTeamID')
    name: str = HTField('BuyerTeamName')


class TransfersTransferItemSeller(HTModel):
    """
    Transfers Team -> Transfers -> Transfer items -> Transfer item -> Seller
    """
    id: int = HTField('SellerTeamID')
    name: str = HTField('SellerTeamName')
