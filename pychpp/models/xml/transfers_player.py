from datetime import datetime
from typing import List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestTransfersPlayer(HTModel):
    """
    Transfers Player - Request arguments
    """
    SOURCE_FILE = 'transfersplayer'
    LAST_VERSION = '1.1'

    _r_player_id: int = HTInitVar('playerID', init_arg='player_id')


class TransfersPlayer(RequestTransfersPlayer):
    """
    Transfers Player
    """
    XML_PREFIX = 'Transfers/'

    start_date: datetime = HTField('StartDate')
    end_date: datetime = HTField('EndDate')
    player: 'Player' = HTField('Player')
    transfers: List['TransferItem'] = HTField('.', items='Transfer')


class Player(HTModel):
    """
    Transfers Player -> Player
    """
    id: int = HTField('PlayerID')
    name: str = HTField('PlayerName')


class TransferItem(HTModel):
    """
    Transfers Player -> Transfers -> Transfer item
    """
    id: int = HTField('TransferID')
    deadline: datetime = HTField('Deadline')
    buyer: 'Team' = HTField('Buyer', xml_prefix='Buyer')
    seller: 'Team' = HTField('Seller', xml_prefix='Seller')
    price: int = HTField('Price')
    tsi: int = HTField('TSI')


class Team(HTModel):
    """
    Transfers Player -> Transfers -> Transfer item -> Buyer/Seller
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
