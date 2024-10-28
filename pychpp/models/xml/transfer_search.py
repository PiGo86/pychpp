from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestTransferSearch(HTModel):
    """
    Transfer Search - Request arguments
    """
    SOURCE_FILE = 'transfersearch'
    LAST_VERSION = '1.1'

    _r_age_min: int = HTInitVar('ageMin', init_arg='age_min')
    _r_age_days_min: Optional[int] = HTInitVar('ageDaysMin', init_arg='age_days_min')
    _r_age_max: int = HTInitVar('ageMax', init_arg='age_max')
    _r_age_days_max: Optional[int] = HTInitVar('ageDaysMax', init_arg='age_days_max')
    _r_skill_type_1: int = HTInitVar('skillType1', init_arg='skill_type_1')
    _r_min_skill_value_1: int = HTInitVar('minSkillValue1', init_arg='min_skill_value_1')
    _r_max_skill_value_1: int = HTInitVar('maxSkillValue1', init_arg='max_skill_value_1')
    _r_skill_type_2: Optional[int] = HTInitVar('skillType2', init_arg='skill_type_2')
    _r_min_skill_value_2: Optional[int] = HTInitVar('minSkillValue2', init_arg='min_skill_value_2')
    _r_max_skill_value_2: Optional[int] = HTInitVar('maxSkillValue2', init_arg='max_skill_value_2')
    _r_skill_type_3: Optional[int] = HTInitVar('skillType3', init_arg='skill_type_3')
    _r_min_skill_value_3: Optional[int] = HTInitVar('minSkillValue3', init_arg='min_skill_value_3')
    _r_max_skill_value_3: Optional[int] = HTInitVar('maxSkillValue3', init_arg='max_skill_value_3')
    _r_skill_type_4: Optional[int] = HTInitVar('skillType4', init_arg='skill_type_4')
    _r_min_skill_value_4: Optional[int] = HTInitVar('minSkillValue4', init_arg='min_skill_value_4')
    _r_max_skill_value_4: Optional[int] = HTInitVar('maxSkillValue4', init_arg='max_skill_value_4')
    _r_specialty: Optional[int] = HTInitVar('Specialty', init_arg='specialty')
    _r_native_country_id: Optional[int] = HTInitVar('nativeCountryId',
                                                    init_arg='native_country_id')
    _r_tsi_min: Optional[int] = HTInitVar('tsiMin', init_arg='tsi_min')
    _r_tsi_max: Optional[int] = HTInitVar('tsiMax', init_arg='tsi_max')
    _r_price_min: Optional[int] = HTInitVar('priceMin', init_arg='price_min')
    _r_price_max: Optional[int] = HTInitVar('priceMax', init_arg='price_max')
    _r_page_size: Optional[int] = HTInitVar('pageSize', init_arg='page_size')
    _r_page_index: Optional[int] = HTInitVar('pageIndex', init_arg='page_index')


class TransferSearch(RequestTransferSearch):
    """
    Transfer Search
    """
    XML_PREFIX = 'TransferSearch/'

    item_count: int = HTField('ItemCount')
    page_size: int = HTField('PageSize')
    page_index: int = HTField('PageIndex')
    transfer_results: List['TransferResultItem'] = HTField('TransferResults',
                                                           items='TransferResult')


class TransferResultItem(HTModel):
    """
    Transfer Search -> Transfer Results -> Transfer Result item
    """
    id: int = HTField('PlayerId')
    first_name: str = HTField('FirstName')
    nick_name: str = HTField('NickName')
    last_name: str = HTField('LastName')
    native_country_id: int = HTField('NativeCountryID')
    asking_price: int = HTField('AskingPrice')
    deadline: datetime = HTField('Deadline')
    highest_bid: int = HTField('HighestBid')
    bidder_team: 'BidderTeam' = HTField('BidderTeam')
    details: 'Details' = HTField('Details')


class BidderTeam(HTModel):
    """
    Transfer Search -> Transfer Results -> Transfer Result item -> Bidder Team
    """
    id: Optional[int] = HTField('TeamID')
    name: Optional[str] = HTField('TeamName')


class Details(HTModel):
    """
    Transfer Search -> Transfer Results -> Transfer Result item -> Details
    """
    age: int = HTField('Age')
    age_days: int = HTField('AgeDays')
    salary: int = HTField('Salary')
    tsi: int = HTField('TSI')
    player_form: int = HTField('PlayerForm')
    experience: int = HTField('Experience')
    leadership: int = HTField('Leadership')
    specialty: int = HTField('Specialty')
    cards: Optional[int] = HTField('Cards')
    injury_level: Optional[int] = HTField('InjuryLevel')
    stamina_skill: int = HTField('StaminaSkill')
    keeper_skill: int = HTField('KeeperSkill')
    playmaker_skill: int = HTField('PlaymakerSkill')
    scorer_skill: int = HTField('ScorerSkill')
    passing_skill: int = HTField('PassingSkill')
    winger_skill: int = HTField('WingerSkill')
    defender_skill: int = HTField('DefenderSkill')
    set_pieces_skill: int = HTField('SetPiecesSkill')
    seller_team: 'SellerTeam' = HTField('SellerTeam')


class SellerTeam(HTModel):
    """
    Transfer Search -> Transfer Results -> Transfer Result item -> Details -> Seller Team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    league_id: int = HTField('LeagueId')
