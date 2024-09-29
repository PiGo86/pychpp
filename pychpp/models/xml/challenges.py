from datetime import datetime
from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class CommonRequestChallenges(HTModel):
    """
    Challenges - Common request arguments
    """
    SOURCE_FILE = 'challenges'
    LAST_VERSION = '1.6'

    _r_action_type: str = HTInitVar('actionType', init_arg='action_type')
    r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')
    r_is_weekend_friendly: Optional[int] = HTInitVar('isWeekendFriendly',
                                                     init_arg='is_weekend_friendly')


class BaseChallenges(CommonRequestChallenges):
    """
    Base Challenges
    """
    team_id: int = HTField('Team/TeamID')
    team_name: str = HTField('Team/TeamName')
    challenges_by_me: List['ChallengeItem'] = HTField('Team/ChallengesByMe', items='Challenge')
    offers_by_others: List['ChallengeItem'] = HTField('Team/OffersByOthers', items='Offer')


class ChallengeItem(HTModel):
    """
    Challenges -> Challenges by me / Offers by others -> Challenge item
    """
    training_match_id: int = HTField('TrainingMatchID')
    match_time: datetime = HTField('MatchTime')
    match_id: Optional[int] = HTField('MatchID')
    friendly_type: int = HTField('FriendlyType')
    opponent_team: 'ChallengeItemOpponent' = HTField('Opponent')
    arena: 'ChallengeArena' = HTField('Arena')
    country: 'ChallengeCountry' = HTField('Country')
    is_agreed: bool = HTField('IsAgreed')


class ChallengeItemOpponent(HTModel):
    """
    Challenges -> Challenges by me / Offers by others -> Challenge item -> Opponent
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    logo_url: str = HTField('LogoURL')


class ChallengeArena(HTModel):
    """
    Challenges -> Challenges by me / Offers by others -> Challenge item -> Opponent -> Arena
    """
    id: int = HTField('ArenaID')
    name: str = HTField('ArenaName')


class ChallengeCountry(HTModel):
    """
    Challenges -> Challenges by me / Offers by others -> Challenge item -> Opponent -> Country
    """
    id: int = HTField('CountryID')
    name: str = HTField('CountryName')


class ChallengesView(BaseChallenges):
    """
    Challenges - View
    """
    pass


class ChallengesChallengeable(BaseChallenges):
    """
    Challenges - Challengeable
    """
    _r_suggested_team_ids: str = HTInitVar('suggestedTeamIds', init_arg='suggested_team_ids')

    challengeable_result: List['ChallengesChallengeableOpponentItem'] = HTField(
        'Team/ChallengeableResult', items='Opponent',
    )


class ChallengesChallengeableOpponentItem(HTModel):
    """
    Challenges - Challengeable -> Challengeable result -> Opponent item
    """
    is_challengeable: bool = HTField('IsChallengeable')
    user_id: int = HTField('UserId')
    team_id: int = HTField('TeamId')
    team_name: str = HTField('TeamName')
    logo_url: str = HTField('LogoURL')


class ChallengesChallenge(BaseChallenges):
    """
    Challenges - Challenge
    """
    _r_opponent_team_id: int = HTInitVar('opponentTeamId', init_arg='opponent_team_id')
    _r_match_type: Optional[int] = HTInitVar('matchType', init_arg='match_type')
    _r_match_place: Optional[int] = HTInitVar('matchPlace', init_arg='match_place')
    _r_neutral_arena_id: Optional[int] = HTInitVar('neutralArenaId', init_arg='neutral_arena_id')


class BaseChallengesDecision(BaseChallenges):
    """
    Challenges - Accept, decline or withdraw a challenge
    """
    r_training_match_id: int = HTInitVar('trainingMatchId', init_arg='training_match_id')


class ChallengesAccept(BaseChallengesDecision):
    """
    Challenges - Accept a challenge
    """
    pass


class ChallengesDecline(BaseChallengesDecision):
    """
    Challenges - Decline a challenge
    """
    pass


class ChallengesWithdraw(BaseChallengesDecision):
    """
    Challenges - Withdraw a challenge
    """
    pass
