from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestMatchLineup(HTModel):
    """
    Match Lineup - Request arguments
    """
    SOURCE_FILE = 'matchlineup'
    LAST_VERSION = '2.1'

    _r_match_id: int = HTInitVar('matchID', init_arg='match_id')
    _r_team_id: int = HTInitVar('teamID', init_arg='team_id')
    _r_source_system: Optional[int] = HTInitVar(
        'sourceSystem', init_arg='source_system', fill_with='source_system',
    )


class MatchLineup(RequestMatchLineup):
    """
    Match Lineup
    """
    match_id: int = HTField('MatchID')
    source_system: str = HTField('SourceSystem')
    home_team: 'Team' = HTField('HomeTeam', xml_prefix='Home')
    away_team: 'Team' = HTField('AwayTeam', xml_prefix='Away')
    match_type: int = HTField('MatchType')
    match_context_id: Optional[int] = HTField('MatchContextId')
    arena: 'Arena' = HTField('Arena')
    team: 'TeamLineup' = HTField('Team')


class Team(HTModel):
    """
    Match Lineup -> Home/Away team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')


class Arena(HTModel):
    """
    Match Lineup -> Arena
    """
    id: int = HTField('ArenaID')
    name: str = HTField('ArenaName')


class TeamLineup(HTModel):
    """
    Match Lineup -> Team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    experience_level: int = HTField('ExperienceLevel')
    style_of_play: int = HTField('StyleOfPlay')
    starting_lineup: List['TeamStartingLineupPlayerItem'] = HTField('StartingLineup',
                                                                    items='Player')
    substitutions: List['TeamSubstitutionItem'] = HTField('Substitutions', items='Substitution')
    lineup: List['TeamLineupPlayerItem'] = HTField('Lineup', items='Player')


class BaseTeamPlayerItem(HTModel):
    """
    Match Lineup -> Team -> Starting Lineup / Lineup -> Base Player item
    """
    id: int = HTField('PlayerID')
    role_id: int = HTField('RoleID')
    first_name: str = HTField('FirstName')
    last_name: str = HTField('LastName')
    nick_name: str = HTField('NickName')
    behaviour: Optional[int] = HTField('Behaviour')


class TeamStartingLineupPlayerItem(BaseTeamPlayerItem):
    """
    Match Lineup -> Team -> Starting Lineup -> Player item
    """


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
    minute: int = HTField('MatchMinute')
    match_part: int = HTField('MatchPart')
