from datetime import datetime
from typing import Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestPlayerDetails(HTModel):
    """
    Player Details - Request arguments
    """
    SOURCE_FILE = 'playerdetails'
    LAST_VERSION = '3.0'

    _r_action_type: Optional[str] = HTInitVar('actionType', init_arg='action_type')
    _r_player_id: int = HTInitVar('playerID', init_arg='player_id')
    _r_include_match_info: Optional[bool] = HTInitVar('includeMatchInfo',
                                                      init_arg='include_match_info')
    _r_team_id: Optional[int] = HTInitVar('teamID', init_arg='team_id')
    _r_bid_amount: Optional[int] = HTInitVar('bidAmount', init_arg='bid_amount')
    _r_max_bid_amount: Optional[int] = HTInitVar('maxBidAmount', init_arg='max_bid_amount')


class PlayerDetails(RequestPlayerDetails):
    """
    Player Details
    """
    XML_PREFIX = 'Player/'

    user_supporter_tier: str = HTField('../UserSupporterTier')

    id: int = HTField('PlayerID')
    first_name: str = HTField('FirstName')
    nick_name: str = HTField('NickName')
    last_name: str = HTField('LastName')
    number: int = HTField('PlayerNumber')
    category_id: Optional[int] = HTField('PlayerCategoryID')
    owner_notes: Optional[str] = HTField('OwnerNotes')
    age: int = HTField('Age')
    age_days: int = HTField('AgeDays')
    next_birthday: datetime = HTField('NextBirthDay')
    arrival_date: datetime = HTField('ArrivalDate')
    form: int = HTField('PlayerForm')
    cards: int = HTField('Cards')
    injury_level: int = HTField('InjuryLevel')
    statement: Optional[str] = HTField('Statement')
    language: Optional[str] = HTField('PlayerLanguage')
    language_id: Optional[int] = HTField('PlayerLanguageID')
    trainer_data: 'TrainerData' = HTField('TrainerData')
    agreeability: int = HTField('Agreeability')
    aggressiveness: int = HTField('Aggressiveness')
    honesty: int = HTField('Honesty')
    experience: int = HTField('Experience')
    loyalty: int = HTField('Loyalty')
    mother_club_bonus: bool = HTField('MotherClubBonus')
    mother_club: 'MotherClub' = HTField('MotherClub')
    leadership: int = HTField('Leadership')
    specialty: int = HTField('Specialty')
    native_country_id: int = HTField('NativeCountryID')
    native_league_id: int = HTField('NativeLeagueID')
    native_league_name: str = HTField('NativeLeagueName')
    tsi: int = HTField('TSI')
    owning_team: 'OwningTeam' = HTField('OwningTeam')
    salary: int = HTField('Salary')
    is_abroad: bool = HTField('IsAbroad')
    skills: 'PlayerSkills' = HTField('PlayerSkills')
    caps: int = HTField('Caps')
    caps_u20: int = HTField('CapsU20')
    career_goals: int = HTField('CareerGoals')
    career_hattricks: int = HTField('CareerHattricks')
    league_goals: Optional[int] = HTField('LeagueGoals')
    cup_goals: Optional[int] = HTField('CupGoals')
    friendlies_goals: Optional[int] = HTField('FriendliesGoals')
    matches_current_team: Optional[int] = HTField('MatchesCurrentTeam')
    goals_current_team: Optional[int] = HTField('GoalsCurrentTeam')
    national_team: 'NationalTeam' = HTField('.')
    transfer_listed: bool = HTField('TransferListed')
    transfer_details: 'TransferDetails' = HTField('TransferDetails')
    last_match: Optional['LastMatch'] = HTField('LastMatch')


class TrainerData(HTModel):
    """
    Player Details -> Trainer Data
    """
    type: Optional[int] = HTField('TrainerType')
    skill_level: Optional[int] = HTField('TrainerSkillLevel')


class MotherClub(HTModel):
    """
    Player Details -> Mother club
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')


class OwningTeam(HTModel):
    """
    Player Details -> Owning team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    league_id: int = HTField('LeagueID')


class PlayerSkills(HTModel):
    """
    Player Details -> Player skills
    """
    stamina: int = HTField('StaminaSkill')
    keeper: Optional[int] = HTField('KeeperSkill')
    playmaker: Optional[int] = HTField('PlaymakerSkill')
    scorer: Optional[int] = HTField('ScorerSkill')
    passing: Optional[int] = HTField('PassingSkill')
    winger: Optional[int] = HTField('WingerSkill')
    defender: Optional[int] = HTField('DefenderSkill')
    set_pieces: Optional[int] = HTField('SetPiecesSkill')


class NationalTeam(HTModel):
    """
    Player Details -> National team
    """
    id: Optional[int] = HTField('NationalTeamID')
    name: Optional[str] = HTField('NationalTeamName')


class TransferDetails(HTModel):
    """
    Player Details -> Transfer details
    """
    asking_price: Optional[int] = HTField('AskingPrice')
    deadline: Optional[datetime] = HTField('Deadline')
    highest_bid: Optional[int] = HTField('HighestBid')
    max_bid: Optional[int] = HTField('MaxBid')
    bidder_team: Optional['TransferDetailsBidderTeam'] = HTField('BidderTeam')


class TransferDetailsBidderTeam(HTModel):
    """
    Player Details -> Transfer details -> Bidder team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')


class LastMatch(HTModel):
    """
    Player Details -> Last match
    """
    date: datetime = HTField('Date')
    id: int = HTField('MatchId')
    position_code: int = HTField('PositionCode')
    played_minutes: int = HTField('PlayedMinutes')
    rating: float = HTField('Rating')
    rating_end_of_game: float = HTField('RatingEndOfGame')
