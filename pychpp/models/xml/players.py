from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestPlayers(HTModel):
    """
    Players - Request arguments
    """
    SOURCE_FILE = 'players'
    LAST_VERSION = '2.6'

    _r_action_type: Optional[str] = HTInitVar('actionType', init_arg='action_type')
    _r_order_by: Optional[str] = HTInitVar('orderBy', init_arg='order_by')
    _r_team_id: Optional[int] = HTInitVar('teamID', init_arg='team_id')
    _r_include_match_info: Optional[bool] = HTInitVar('includeMatchInfo',
                                                      init_arg='include_match_info')


class BasePlayers(RequestPlayers):
    """
    Players
    """
    user_supporter_tier: str = HTField('UserSupporterTier')
    is_youth: bool = HTField('IsYouth')
    action_type: str = HTField('ActionType')
    is_playing_match: bool = HTField('IsPlayingMatch')


class PlayersView(BasePlayers):
    """
    Players - View
    """
    team: 'PlayersViewTeam' = HTField('Team')


class PlayersViewOldies(BasePlayers):
    """
    Players - View oldies
    """
    team: 'PlayersViewOldiesTeam' = HTField('Team')


class PlayersViewOldCoaches(BasePlayers):
    """
    Players - View old coaches
    """
    team: 'PlayersViewOldCoachesTeam' = HTField('Team')


class BasePlayersTeam(HTModel):
    """
    Players -> Team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')


class PlayersViewTeam(BasePlayersTeam):
    """
    Players - View -> Team
    """
    players: List['PlayersViewTeamPlayerItem'] = HTField('PlayerList', items='Player')


class PlayersViewOldiesTeam(BasePlayersTeam):
    """
    Players - View oldies -> Team
    """
    players: List['PlayersViewOldiesTeamPlayerItem'] = HTField('PlayerList', items='Player')


class PlayersViewOldCoachesTeam(BasePlayersTeam):
    """
    Players - View oldies -> Team
    """
    players: List['PlayersViewOldCoachesTeamPlayerItem'] = HTField('PlayerList', items='Player')


class BasePlayersTeamPlayerItem(HTModel):
    """
    Base Players -> Team -> Players -> Player item
    """

    id: int = HTField('PlayerID')
    first_name: str = HTField('FirstName')
    nick_name: str = HTField('NickName')
    last_name: str = HTField('LastName')
    number: int = HTField('PlayerNumber')
    age: int = HTField('Age')
    age_days: int = HTField('AgeDays')
    tsi: int = HTField('TSI')
    form: int = HTField('PlayerForm')
    statement: Optional[str] = HTField('Statement')
    experience: int = HTField('Experience')
    leadership: int = HTField('Leadership')
    salary: int = HTField('Salary')
    is_abroad: bool = HTField('IsAbroad')
    agreeability: int = HTField('Agreeability')
    aggressiveness: int = HTField('Aggressiveness')
    honesty: int = HTField('Honesty')
    league_goals: Optional[int] = HTField('LeagueGoals')
    cup_goals: Optional[int] = HTField('CupGoals')
    friendlies_goals: Optional[int] = HTField('FriendliesGoals')
    career_goals: int = HTField('CareerGoals')
    career_hattricks: int = HTField('CareerHattricks')
    specialty: int = HTField('Specialty')
    transfer_listed: bool = HTField('TransferListed')
    national_team_id: int = HTField('NationalTeamID')
    country_id: int = HTField('CountryID')
    caps: int = HTField('Caps')
    caps_u20: int = HTField('CapsU20')
    cards: int = HTField('Cards')
    injury_level: int = HTField('InjuryLevel')
    last_match: Optional['BasePlayersTeamPlayerItemLastMatch'] = HTField('LastMatch')


class PlayersViewTeamPlayerItem(BasePlayersTeamPlayerItem):
    """
    Players - View -> Team -> Players -> Player item
    """

    arrival_date: datetime = HTField('ArrivalDate')
    owner_notes: Optional[str] = HTField('OwnerNotes')
    loyalty: int = HTField('Loyalty')
    mother_club_bonus: bool = HTField('MotherClubBonus')
    matches_current_team: Optional[int] = HTField('MatchesCurrentTeam')
    goals_current_team: Optional[int] = HTField('GoalsCurrentTeam')
    player_skills: 'PlayersViewTeamPlayerItemPlayerSkills' = HTField('.')
    category_id: Optional[int] = HTField('PlayerCategoryID')
    trainer_data: Optional['CommonTeamPlayerItemTrainerData'] = HTField('TrainerData')


class PlayersViewTeamPlayerItemPlayerSkills(HTModel):
    """
    Players - View -> Team -> Players -> Player item -> Skills
    """
    stamina: int = HTField('StaminaSkill')
    keeper: Optional[int] = HTField('KeeperSkill')
    playmaker: Optional[int] = HTField('PlaymakerSkill')
    scorer: Optional[int] = HTField('ScorerSkill')
    passing: Optional[int] = HTField('PassingSkill')
    winger: Optional[int] = HTField('WingerSkill')
    defender: Optional[int] = HTField('DefenderSkill')
    set_pieces: Optional[int] = HTField('SetPiecesSkill')


class BasePlayersTeamPlayerItemLastMatch(HTModel):
    """
    Base Players -> Team -> Players -> Player item -> Last match
    """
    date: datetime = HTField('Date')
    id: int = HTField('MatchId')
    position_code: int = HTField('PositionCode')
    played_minutes: int = HTField('PlayedMinutes')
    rating: float = HTField('Rating')
    rating_end_of_game: float = HTField('RatingEndOfGame')


class CommonTeamPlayerItemTrainerData(HTModel):
    """
    Players - View or View old coaches -> Team -> Players -> Player Item -> Trainer Data
    """
    type: Optional[int] = HTField('TrainerType')
    skill_level: Optional[int] = HTField('TrainerSkillLevel')


class PlayersViewOldiesTeamPlayerItem(BasePlayersTeamPlayerItem):
    """
    Players - View oldies -> Team -> Players -> Player Item
    """
    owning_team: 'PlayersViewOldiesTeamPlayerItemOwningTeam' = HTField('OwningTeam')


class PlayersViewOldiesTeamPlayerItemOwningTeam(HTModel):
    """
    Players - View oldies -> Team -> Players -> Player Item -> Owning team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    league_name: str = HTField('LeagueName')


class PlayersViewOldCoachesTeamPlayerItem(BasePlayersTeamPlayerItem):
    """
    Players - View old coaches -> Team -> Players -> Player Item
    """
    trainer_data: 'CommonTeamPlayerItemTrainerData' = HTField('TrainerData')
