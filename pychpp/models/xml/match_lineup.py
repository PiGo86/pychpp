from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class MatchLineup(HTModel):
    """
    Match Lineup
    """
    SOURCE_FILE = 'matchlineup'
    LAST_VERSION = '2.1'

    _r_match_id = HTInitVar('matchID', init_arg='match_id')
    _r_team_id = HTInitVar('teamID', init_arg='team_id')
    _r_source_system = HTInitVar('sourceSystem', init_arg='source_system')

    id: int = HTField('MatchID')
    source_system: str = HTField('SourceSystem')
    home_team: 'HomeTeam' = HTField('HomeTeam')
    away_team: 'AwayTeam' = HTField('AwayTeam')
    type: int = HTField('MatchType')
    context_id: int = HTField('MatchContextId')
    arena: 'Arena' = HTField('Arena')
    team: 'Team' = HTField('Team')


class HomeTeam(HTModel):
    """
    Match Lineup -> Home team
    """
    id: int = HTField('HomeTeamID')
    name: str = HTField('HomeTeamName')


class AwayTeam(HTModel):
    """
    Match Lineup -> Away team
    """
    id: int = HTField('AwayTeamID')
    name: str = HTField('AwayTeamName')


class Arena(HTModel):
    """
    Match Lineup -> Arena
    """
    id: int = HTField('ArenaID')
    name: str = HTField('ArenaName')


class Team(HTModel):
    """
    Match Lineup -> Team
    """
    id: int = HTField('TeamID')
    name: str  =HTField('TeamName')
    experience_level: int = HTField('ExperienceLevel')
    style_of_play: int = HTField('StyleOfPlay')
    starting_lineup: List['TeamStartingLineupPlayerItem'] = HTField('StartingLineup', items='Player')
    substitutions: List['TeamSubstitutionItem'] = HTField('Substitutions', items='Substitution')
    lineup: List['TeamLineupPlayerItem'] = HTField('Lineup', items='Player')


class BaseTeamPlayerItem(HTModel):
    """
    Match Lineup -> Team -> Starting Lineup / Lineup -> Base Player item
    """
    id: int = HTField('PlayerID')
    role: int = HTField('RoleID')
    first_name: str = HTField('FirstName')
    last_name: str = HTField('LastName')
    nick_name: str  =HTField('NickName')
    behaviour: Optional[int] = HTField('Behaviour')


class TeamStartingLineupPlayerItem(BaseTeamPlayerItem):
    """
    Match Lineup -> Team -> Starting Lineup -> Player item
    """
    pass


class TeamLineupPlayerItem(BaseTeamPlayerItem):
    """
    Match Lineup -> Team -> Starting Lineup -> Player item
    """
    rating_stars: Optional[float] = HTField('RatingStars')
    rating_stars_end_of_match: Optional[float] = HTField('RatingStarsEndOfMatch')


class TeamSubstitutionItem(HTModel):
    """
    Match Lineup -> Team -> Substitutions -> Substitution item
    """
    team_id: int = HTField('TeamID')
    subject_player_id: int = HTField('SubjectPlayerID')
    object_player_id: int = HTField('ObjectPlayerID')
    order_type: int = HTField('OrderType')
    new_position_id: int = HTField('NewPositionId')
    new_position_behaviour: int = HTField('NewPositionBehaviour')
    match_minute: int = HTField('MatchMinute')
    match_part: int = HTField('MatchPart')
