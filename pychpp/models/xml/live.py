from datetime import datetime
from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestLive(HTModel):
    """
    Live - Request arguments
    """
    SOURCE_FILE = 'live'
    LAST_VERSION = '2.3'

    _r_action_type: Optional[str] = HTInitVar('actionType', init_arg='action_type')
    _r_match_id: Optional[int] = HTInitVar('matchID', init_arg='match_id')
    _r_source_system: Optional[str] = HTInitVar('sourceSystem', init_arg='source_system')
    _r_include_starting_lineup: Optional[bool] = HTInitVar('includeStartingLineup',
                                                           init_arg='include_starting_lineup')
    _r_use_live_events_and_textx: Optional[bool] = HTInitVar('useLiveEventsAndTexts',
                                                             init_arg='use_live_events_and_texts')
    _r_last_shown_indexes: Optional[str] = HTInitVar('lastShownIndexes',
                                                     init_arg='last_shown_indexes')


class Live(RequestLive):
    """
    Live
    """
    matches: Optional[List['MatchItem']] = HTField('MatchList', items='Match')


class MatchItem(HTModel):
    """
    Live -> Matches -> Match item
    """
    id: int = HTField('MatchID')
    type: int = HTField('MatchType')
    source_system: str = HTField('SourceSystem')
    date: datetime = HTField('MatchDate')
    home_team: 'HomeTeam' = HTField('HomeTeam')
    away_team: 'AwayTeam' = HTField('AwayTeam')
    substitutions: Optional[List['SubstitutionItem']] = HTField('Substitutions',
                                                                items='Substitution')
    events: List['EventItem'] = HTField('EventList', items='Event')
    home_goals: int = HTField('HomeGoals')
    away_goals: int = HTField('AwayGoals')
    last_shown_event_index: int = HTField('LastShownEventIndex')
    next_event_minute: int = HTField('NextEventMinute')
    next_event_match_part: int = HTField('NextEventMatchPart')


class HomeTeam(HTModel):
    """
    Live -> Matches -> Match item -> Home team
    """
    id: int = HTField('HomeTeamID')
    name: str = HTField('HomeTeamName')
    short_name: str = HTField('HomeTeamShortName')
    starting_lineup: Optional[List['PlayerItem']] = HTField('StartingLineup', items='Player')


class AwayTeam(HTModel):
    """
    Live -> Matches -> Match item -> Away team
    """
    id: int = HTField('AwayTeamID')
    name: str = HTField('AwayTeamName')
    short_name: str = HTField('AwayTeamShortName')
    starting_lineup: Optional[List['PlayerItem']] = HTField('StartingLineup', items='Player')


class PlayerItem(HTModel):
    """
    Live -> Matches -> Match item -> Home/Away team -> Starting Lineup -> Player item
    """
    id: int = HTField('PlayerID')
    role_id: int = HTField('RoleID')
    name: str = HTField('PlayerName')
    behaviour: Optional[int] = HTField('Behaviour')


class SubstitutionItem(HTModel):
    """
    Live -> Matches -> Match item -> Substitutions -> Substitution item
    """
    team_id: int = HTField('TeamID')
    subject_player_id: int = HTField('SubjectPlayerID')
    object_player_id: int = HTField('ObjectPlayerID')
    order_type: int = HTField('OrderType')
    new_position_id: int = HTField('NewPositionId')
    new_position_behaviour: int = HTField('NewPositionBehaviour')
    match_minute: int = HTField('MatchMinute')


class EventItem(HTModel):
    """
    Live -> Matches -> Match item -> Event -> Event item
    """
    index: int = HTField('.', attrib='Index')
    minute: int = HTField('Minute')
    match_part: int = HTField('MatchPart')
    key: str = HTField('EventKey')
    text: str = HTField('EventText')
    subject_team_id: int = HTField('SubjectTeamID')
    subject_player_id: int = HTField('SubjectPlayerID')
    object_player_id: int = HTField('ObjectPlayerID')
