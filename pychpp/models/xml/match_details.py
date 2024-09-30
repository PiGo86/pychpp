from datetime import datetime
from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestMatchDetails(HTModel):
    """
    Match Details - Request arguments
    """
    SOURCE_FILE = 'matchdetails'
    LAST_VERSION = '3.1'

    _r_match_id: int = HTInitVar('matchID', init_arg='match_id')
    _r_source_system: Optional[str] = HTInitVar('sourceSystem', init_arg='source_system')
    _r_match_events: Optional[bool] = HTInitVar('matchEvents', init_arg='match_events')


class MatchDetails(RequestMatchDetails):
    """
    Match Details
    """

    source_system: str = HTField('SourceSystem')
    user_supporter_tier: str = HTField('UserSupporterTier')
    match: 'Match' = HTField('Match')


class Match(HTModel):
    """
    Match Details -> Match
    """
    id: int = HTField('MatchID')
    type: int = HTField('MatchType')
    context_id: int = HTField('MatchContextId')
    rule_id: int = HTField('MatchRuleId')
    cup_level: int = HTField('CupLevel')
    cup_level_index: int = HTField('CupLevelIndex')
    date: datetime = HTField('MatchDate')
    finished_date: datetime = HTField('FinishedDate')
    added_minutes: int = HTField('AddedMinutes')
    home_team: 'MatchHomeTeam' = HTField('HomeTeam')
    away_team: 'MatchAwayTeam' = HTField('AwayTeam')
    arena: 'MatchArena' = HTField('Arena')
    officials: 'MatchOfficials' = HTField('MatchOfficials')
    goals: List['MatchGoalItem'] = HTField('Scorers', items='Goal')
    bookings: List['MatchBookingItem'] = HTField('Bookings', items='Booking')
    injuries: List['MatchInjuryItem'] = HTField('Injuries', items='Injury')
    possession: 'MatchPossession' = HTField('.')
    events: Optional[List['MatchEventItem']] = HTField('EventList', items='Event')


class BaseMatchTeam(HTModel):
    """
    Match Details -> Match -> Base Home/Away team
    """
    dress_uri: str = HTField('DressURI')
    formation: str = HTField('Formation')
    tactic_type: int = HTField('TacticType')
    tactic_skill: int = HTField('TacticSkill')
    ratings: 'MatchTeamRatings' = HTField('.')
    team_attitude: Optional[int] = HTField('TeamAttitude')
    chances: 'MatchTeamChances' = HTField('.')


class MatchHomeTeam(BaseMatchTeam):
    """
    Match Details -> Match -> Home team
    """
    id: int = HTField('HomeTeamID')
    name: str = HTField('HomeTeamName')
    goals: int = HTField('HomeGoals')


class MatchAwayTeam(BaseMatchTeam):
    """
    Match Details -> Match -> Away team
    """
    id: int = HTField('AwayTeamID')
    name: str = HTField('AwayTeamName')
    goals: int = HTField('AwayGoals')


class MatchTeamRatings(HTModel):
    """
    Match Details -> Match -> Home/Away team -> Ratings
    """
    midfield: int = HTField('RatingMidfield')
    right_defense: int = HTField('RatingRightDef')
    mid_defense: int = HTField('RatingMidDef')
    left_defense: int = HTField('RatingLeftDef')
    right_attack: int = HTField('RatingRightDef')
    mid_attack: int = HTField('RatingMidDef')
    left_attack: int = HTField('RatingLeftDef')
    indirect_set_pieces_defense: Optional[int] = HTField('RatingIndirectSetPiecesDef')
    indirect_set_pieces_attack: Optional[int] = HTField('RatingIndirectSetPiecesAtt')


class MatchTeamChances(HTModel):
    """
    Match Details -> Match -> Home/Away team -> Chances
    """
    left: int = HTField('NrOfChancesLeft')
    center: int = HTField('NrOfChancesCenter')
    right: int = HTField('NrOfChancesRight')
    special_events: int = HTField('NrOfChancesSpecialEvents')
    other: int = HTField('NrOfChancesOther')


class MatchArena(HTModel):
    """
    Match Details -> Match -> Arena
    """
    id: int = HTField('ArenaID')
    name: str = HTField('ArenaName')
    weather_id: int = HTField('WeatherID')
    sold: 'MatchArenaSold' = HTField('.')


class MatchArenaSold(HTModel):
    """
    Match Details -> Match -> Arena -> Sold
    """
    total: int = HTField('SoldTotal')
    terraces: int = HTField('SoldTerraces')
    basic: int = HTField('SoldBasic')
    roof: int = HTField('SoldRoof')
    vip: int = HTField('SoldVIP')


class MatchOfficials(HTModel):
    """
    Match Details -> Match -> Official referees
    """
    referee: 'MatchOfficialsRefereeItem' = HTField('Referee')
    referee_assistant_1: 'MatchOfficialsRefereeItem' = HTField('RefereeAssistant1')
    referee_assistant_2: 'MatchOfficialsRefereeItem' = HTField('RefereeAssistant2')


class MatchOfficialsRefereeItem(HTModel):
    """
    Match Details -> Match -> Official referees -> Referee item
    """
    id: int = HTField('RefereeId')
    name: str = HTField('RefereeName')
    country: 'MatchOfficialsRefereeItemCountry' = HTField('.')
    team: 'MatchOfficialsRefereeItemTeam' = HTField('.')


class MatchOfficialsRefereeItemCountry(HTModel):
    """
    Match Details -> Match -> Official referees -> Referee item -> Country
    """
    id: int = HTField('RefereeCountryId')
    name: str = HTField('RefereeCountryName')


class MatchOfficialsRefereeItemTeam(HTModel):
    """
    Match Details -> Match -> Official referees -> Referee item -> Team
    """
    id: int = HTField('RefereeTeamId')
    name: str = HTField('RefereeTeamname')


class MatchGoalItem(HTModel):
    """
    Match Details -> Match -> Goals -> Goal item
    """
    player_id: int = HTField('ScorerPlayerID')
    player_name: str = HTField('ScorerPlayerName')
    team_id: int = HTField('ScorerTeamID')
    home_goals_after: int = HTField('ScorerHomeGoals')
    away_goals_after: int = HTField('ScorerAwayGoals')
    minute: int = HTField('ScorerMinute')
    match_part: int = HTField('MatchPart')


class MatchBookingItem(HTModel):
    """
    Match Details -> Match -> Bookings -> Booking item
    """
    player_id: int = HTField('BookingPlayerID')
    player_name: str = HTField('BookingPlayerName')
    team_id: int = HTField('BookingTeamID')
    type: int = HTField('BookingType')
    minute: int = HTField('BookingMinute')
    match_part: int = HTField('MatchPart')


class MatchInjuryItem(HTModel):
    """
    Match Details -> Match -> Injuries -> Injury item
    """
    player_id: int = HTField('InjuryPlayerID')
    player_name: str = HTField('InjuryPlayerName')
    team_id: int = HTField('InjuryTeamID')
    type: int = HTField('InjuryType')
    minute: int = HTField('InjuryMinute')
    match_part: int = HTField('MatchPart')


class MatchPossession(HTModel):
    """
    Match Details -> Match -> Possession
    """
    first_half_home: int = HTField('PossessionFirstHalfHome')
    first_half_away: int = HTField('PossessionFirstHalfAway')
    second_half_home: int = HTField('PossessionSecondHalfHome')
    second_half_away: int = HTField('PossessionSecondHalfAway')


class MatchEventItem(HTModel):
    """
    Match Details -> Match -> Events -> Event item
    """
    minute: int = HTField('Minute')
    match_part: int = HTField('MatchPart')
    type_id: int = HTField('EventTypeID')
    variation: int = HTField('EventVariation')
    text: str = HTField('EventText')
    subject_team_id: int = HTField('SubjectTeamID')
    subject_player_id: int = HTField('SubjectPlayerID')
    object_player_id: int = HTField('ObjectPlayerID')
