from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestMatchOrders(HTModel):
    """
    Match Orders - Request arguments
    """
    SOURCE_FILE = 'matchorders'
    LAST_VERSION = '3.1'

    _r_action_type: Optional[str] = HTInitVar('actionType', init_arg='action_type')
    _r_match_id: int = HTInitVar('matchID', init_arg='match_id')
    _r_team_id: Optional[int] = HTInitVar('teamid', init_arg='team_id')
    _r_source_system: Optional[str] = HTInitVar('sourceSystem', init_arg='source_system')
    _r_lineup: Optional[str] = HTInitVar('lineup', init_arg='lineup')


class CommonMatchOrders(RequestMatchOrders):
    """
    Match Orders
    """
    id: int = HTField('MatchID')
    source_system: str = HTField('SourceSystem')


class MatchOrdersView(CommonMatchOrders):
    """
    Match Orders - View
    """
    match_data: Optional['MatchDataView'] = HTField('MatchData')


class MatchDataView(HTModel):
    """
    Match Orders - View -> Match Data
    """
    available: bool = HTField('.', attrib='Available')
    home_team: 'Team' = HTField('HomeTeam', xml_prefix='Home')
    away_team: 'Team' = HTField('AwayTeam', xml_prefix='Away')
    arena: 'Arena' = HTField('Arena')
    date: datetime = HTField('MatchDate')
    type: int = HTField('MatchType')
    attitude: Optional[int] = HTField('Attitude')
    tactic_type: int = HTField('TacticType')
    coach_modifier: Optional[int] = HTField('CoachModifier')
    lineup: 'Lineup' = HTField('Lineup')
    player_orders: List['PlayerOrderItem'] = HTField('PlayerOrders', items='PlayerOrder')


class Team(HTModel):
    """
    Match Orders - View -> Match Data -> Home/Away Team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')


class Arena(HTModel):
    """
    Match Orders - View -> Match Data -> Arena
    """
    id: int = HTField('ArenaID')
    name: str = HTField('ArenaName')


class Lineup(HTModel):
    """
    Match Orders - View -> Match Data -> Lineup
    """
    positions: List['PositionPlayerItem'] = HTField('Positions', items='Player')
    bench: List['BenchPlayerItem'] = HTField('Bench', items='Player')
    kickers: List['KickerPlayerItem'] = HTField('Kickers', items='Player')
    set_pieces: Optional['SetPieces'] = HTField('SetPieces')
    captain: Optional['Captain'] = HTField('Captain')


class BasePlayer(HTModel):
    """
    Match Orders - View -> Match Data -> Lineup -> Base player
    """
    id: int = HTField('PlayerID')
    first_name: str = HTField('FirstName')
    nick_name: str = HTField('NickName')
    last_name: str = HTField('LastName')


class PositionPlayerItem(BasePlayer):
    """
    Match Orders - View -> Match Data -> Lineup -> Positions -> Player item
    """
    role_id: int = HTField('RoleID')
    behaviour: int = HTField('Behaviour')


class BenchPlayerItem(BasePlayer):
    """
    Match Orders - View -> Match Data -> Lineup -> Bench -> Player item
    """
    role_id: int = HTField('RoleID')


class KickerPlayerItem(HTModel):
    """
    Match Orders - View -> Match Data -> Lineup -> Kickers -> Player item
    """
    id: int = HTField('PlayerID')
    role_id: int = HTField('RoleID')


class SetPieces(BasePlayer):
    """
    Match Orders - View -> Match Data -> Lineup -> Set Pieces
    """


class Captain(BasePlayer):
    """
    Match Orders - View -> Match Data -> Lineup -> Captain
    """


class PlayerOrderItem(HTModel):
    """
    Match Orders - View -> Match Data -> Player Orders -> Player order item
    """
    id: int = HTField('PlayerOrderID')
    match_minute_criteria: int = HTField('MatchMinuteCriteria')
    goal_diff_criteria: int = HTField('GoalDiffCriteria')
    red_card_criteria: int = HTField('RedCardCriteria')
    subject_player_id: int = HTField('SubjectPlayerID')
    object_player_id: int = HTField('ObjectPlayerID')
    order_type: int = HTField('OrderType')
    new_position_id: int = HTField('NewPositionId')
    new_position_behaviour: int = HTField('NewPositionBehaviour')
    extra_integer: int = HTField('PlayerOrderExtraInteger')


class MatchOrdersSetMatchOrder(CommonMatchOrders):
    """
    Match Orders - Set match order
    """
    METHOD = 'POST'
    match_data: Optional['MatchDataSetMatchOrder'] = HTField('MatchData')


class MatchDataSetMatchOrder(HTModel):
    """
    Match Orders - Set match order -> Match Data
    """
    orders_set: bool = HTField('.', attrib='OrdersSet')
    reason: Optional[str] = HTField('Reason')


class MatchOrdersPredictRatings(CommonMatchOrders):
    """
    Match Orders - Predict Ratings
    """
    match_data: Optional['MatchDataPredictRatings'] = HTField('MatchData')


class MatchDataPredictRatings(HTModel):
    """
    Match Orders - Predict Ratings -> Match Data
    """
    tactic_type: int = HTField('TacticType')
    tactic_skill: int = HTField('TacticSkill')
    rating_midfield: int = HTField('RatingMidfield')
    rating_right_def: int = HTField('RatingRightDef')
    rating_mid_def: int = HTField('RatingMidDef')
    rating_left_def: int = HTField('RatingLeftDef')
    rating_right_att: int = HTField('RatingRightAtt')
    rating_mid_att: int = HTField('RatingMidAtt')
    rating_left_att: int = HTField('RatingLeftAtt')
