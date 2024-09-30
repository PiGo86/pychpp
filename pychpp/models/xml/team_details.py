from datetime import datetime
from typing import List, Optional

from pychpp.models.ht_model import HTField, HTInitVar, HTModel


class RequestTeamDetails(HTModel):
    """
    Team Details - Request arguments
    """

    SOURCE_FILE = 'teamdetails'
    LAST_VERSION = '3.7'

    _r_team_id: Optional[int] = HTInitVar('teamID', init_arg='team_id')
    _r_user_id: Optional[int] = HTInitVar('userID', init_arg='user_id')
    _r_include_domestics_flags: Optional[bool] = HTInitVar('includeDomesticFlags',
                                                           init_arg='include_domestics_flags')
    _r_include_flags: Optional[bool] = HTInitVar('includeFlags', init_arg='include_flags')
    _r_include_supporters: Optional[bool] = HTInitVar('includeSupporters',
                                                      init_arg='include_supporters')


class TeamDetails(RequestTeamDetails):
    """
    Team Details
    """
    user: 'User' = HTField('User')
    teams: List['TeamItem'] = HTField('Teams', items='Team')


class User(HTModel):
    """
    Team Details -> User
    """
    id: int = HTField('UserID')
    language: 'UserLanguage' = HTField('Language')
    supporter_tier: str = HTField('SupporterTier')
    login_name: str = HTField('Loginname')
    name: str = HTField('Name')
    icq: str = HTField('ICQ')
    signup_date: datetime = HTField('SignupDate')
    activation_date: datetime = HTField('ActivationDate')
    last_login_date: datetime = HTField('LastLoginDate')
    has_manager_license: bool = HTField('HasManagerLicense')
    national_teams: Optional[List['NationalTeamItem']] = HTField('NationalTeams',
                                                                 items='NationalTeam')


class UserLanguage(HTModel):
    """
    Team Details -> User -> Language
    """
    id: int = HTField('LanguageID')
    name: str = HTField('LanguageName')


class NationalTeamItem(HTModel):
    """
    Team Details -> National teams -> National team item
    """
    id: int = HTField('NationalTeamID')
    name: str = HTField('NationalTeamName')
    staff_type_id: int = HTField('NationalTeamStaffType')


class TeamItem(HTModel):
    """
    Team Details -> Teams -> Team item
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    short_name: str = HTField('ShortTeamName')
    is_primary_club: bool = HTField('IsPrimaryClub')
    founded_date: datetime = HTField('FoundedDate')
    is_deactivated: bool = HTField('IsDeactivated', version='>=3.7')
    arena: 'TeamItemArena' = HTField('Arena')
    league: 'TeamItemLeague' = HTField('League')
    country: 'TeamItemCountry' = HTField('Country')
    region: 'TeamItemRegion' = HTField('Region')
    trainer: 'TeamItemTrainer' = HTField('Trainer')
    homepage: str = HTField('HomePage')
    cup: 'TeamItemCup' = HTField('Cup')
    power_rating: 'TeamItemPowerRating' = HTField('PowerRating')
    friendly_team_id: int = HTField('FriendlyTeamID')
    league_level_unit: 'TeamItemLeagueLevelUnit' = HTField('LeagueLevelUnit')
    number_of_victories: int = HTField('NumberOfVictories')
    number_of_undefeated: int = HTField('NumberOfUndefeated')
    fan_club: 'TeamItemFanClub' = HTField('Fanclub')
    logo_url: str = HTField('LogoURL')
    guestbook: Optional['TeamItemGuestbook'] = HTField('Guestbook')
    press_announcement: Optional['TeamItemPressAnnouncement'] = HTField('PressAnnouncement')
    colors: Optional['TeamItemColors'] = HTField('TeamColors')
    dress_uri: str = HTField('DressURI')
    dress_alternate_uri: str = HTField('DressAlternateURI')
    bot_status: 'TeamItemBotStatus' = HTField('BotStatus')
    team_rank: int = HTField('TeamRank')
    youth_team: 'TeamItemYouthTeam' = HTField('.')
    number_of_visits: int = HTField('NumberOfVisits')
    flags: Optional['TeamItemFlags'] = HTField('Flags')
    trophies: List['TeamItemTrophyItem'] = HTField('TrophyList', items='Trophy')
    supported_teams: Optional['TeamItemSupportedTeams'] = HTField('SupportedTeams')
    supporters: Optional['TeamItemSupporters'] = HTField('MySupporters')
    possible_to_challenge_midweek: bool = HTField('PossibleToChallengeMidweek')
    possible_to_challenge_weekend: bool = HTField('PossibleToChallengeWeekend')


class TeamItemArena(HTModel):
    """
    Team Details -> Teams -> Team item -> Arena
    """
    id: int = HTField('ArenaID')
    name: str = HTField('ArenaName')


class TeamItemLeague(HTModel):
    """
    Team Details -> Teams -> Team item -> League
    """
    id: int = HTField('LeagueID')
    name: str = HTField('LeagueName')


class TeamItemCountry(HTModel):
    """
    Team Details -> Teams -> Team item -> Country
    """
    id: int = HTField('CountryID')
    name: str = HTField('CountryName')


class TeamItemRegion(HTModel):
    """
    Team Details -> Teams -> Team item -> Region
    """
    id: int = HTField('RegionID')
    name: str = HTField('RegionName')


class TeamItemTrainer(HTModel):
    """
    Team Details -> Teams -> Team item -> Trainer
    """
    id: int = HTField('PlayerID')


class TeamItemCup(HTModel):
    """
    Team Details -> Teams -> Team item -> Cup
    """
    still_in_cup: Optional[bool] = HTField('StillInCup')
    id: Optional[int] = HTField('CupID')
    name: Optional[str] = HTField('CupName')
    league_level: Optional[int] = HTField('CupLeagueLevel')
    level: Optional[int] = HTField('CupLevel')
    level_index: Optional[int] = HTField('CupLevelIndex')
    match_round: Optional[int] = HTField('MatchRound')
    match_rounds_left: Optional[int] = HTField('MatchRoundsLeft')


class TeamItemPowerRating(HTModel):
    """
    Team Details -> Teams -> Team item -> Power rating
    """
    global_ranking: int = HTField('GlobalRanking')
    league_ranking: int = HTField('LeagueRanking')
    region_ranking: int = HTField('RegionRanking')
    value: int = HTField('PowerRating')


class TeamItemLeagueLevelUnit(HTModel):
    """
    Team Details -> Teams -> Team item -> League level unit
    """
    id: Optional[int] = HTField('LeagueLevelUnitID')
    name: Optional[str] = HTField('LeagueLevelUnitName')
    level: Optional[int] = HTField('LeagueLevel')


class TeamItemFanClub(HTModel):
    """
    Team Details -> Teams -> Team item -> Fan club
    """
    id: int = HTField('FanclubID')
    name: str = HTField('FanclubName')
    size: int = HTField('FanclubSize')


class TeamItemGuestbook(HTModel):
    """
    Team Details -> Teams -> Team item -> Guestbook
    """
    number_of_items: int = HTField('NumberOfGuestbookItems')


class BasePress(HTModel):
    """
    Team Details -> Base press announcement
    """
    subject: str = HTField('Subject')
    body: str = HTField('Body')
    send_date: datetime = HTField('SendDate')


class TeamItemPressAnnouncement(BasePress):
    """
    Team Details -> Teams -> Team item -> Press announcement
    """
    pass


class TeamItemColors(HTModel):
    """
    Team Details -> Teams -> Team item -> Colors
    """
    background_color: Optional[str] = HTField('BackgroundColor')
    color: Optional[str] = HTField('Color')


class TeamItemBotStatus(HTModel):
    """
    Team Details -> Teams -> Team item -> Bot status
    """
    is_bot: bool = HTField('IsBot')
    bot_since: Optional[datetime] = HTField('BotSince')


class TeamItemYouthTeam(HTModel):
    """
    Team Details -> Teams -> Team item -> Youth team
    """
    id: int = HTField('YouthTeamID')
    name: str = HTField('YouthTeamName')


class TeamItemFlags(HTModel):
    """
    Team Details -> Teams -> Team item -> Flags
    """
    home_flags: List['TeamItemFlagsHomeOrAwayFlagsItem'] = HTField('HomeFlags', items='Flag')
    away_flags: List['TeamItemFlagsHomeOrAwayFlagsItem'] = HTField('AwayFlags', items='Flag')


class TeamItemFlagsHomeOrAwayFlagsItem(HTModel):
    """
    Team Details -> Teams -> Team item -> Flags -> Home or away flags -> Flag item
    """
    league_id: int = HTField('LeagueId')
    league_name: str = HTField('LeagueName')
    country_code: str = HTField('CountryCode')


class TeamItemTrophyItem(HTModel):
    """
    Team Details -> Teams -> Team item -> Trophies -> Trophy item
    """
    type_id: int = HTField('TrophyTypeId')
    season: int = HTField('TrophySeason')
    league_level: int = HTField('LeagueLevel')
    league_level_unit_id: int = HTField('LeagueLevelUnitId')
    league_level_unit_name: str = HTField('LeagueLevelUnitName')
    gained_date: datetime = HTField('GainedDate')
    image_url: Optional[str] = HTField('ImageUrl')
    cup_league_level: Optional[int] = HTField('CupLeagueLevel')
    cup_level: Optional[int] = HTField('CupLevel')
    cup_level_index: Optional[int] = HTField('CupLevelIndex')


class TeamItemSupportedTeams(HTModel):
    """
    Team Details -> Teams -> Team item -> Supported teams
    """
    total_items: int = HTField('.', attrib='TotalItems')
    max_items: int = HTField('.', attrib='MaxItems')
    teams: List['TeamItemSupportedTeamsTeamItem'] = HTField('.', items='SupportedTeam')


class TeamItemSupportedTeamsOrSupportersBaseTeamItem(HTModel):
    """
    Team Details -> Teams -> Team item -> Supported teams or Supporters -> Base team item
    """
    id: int = HTField('TeamId')
    name: str = HTField('TeamName')
    user_id: int = HTField('UserId')
    login_name: str = HTField('LoginName')
    league_id: int = HTField('LeagueID')
    league_name: str = HTField('LeagueName')
    league_level_unit_id: int = HTField('LeagueLevelUnitID')
    league_level_unit_name: str = HTField('LeagueLevelUnitName')


class TeamItemSupportedTeamsTeamItem(TeamItemSupportedTeamsOrSupportersBaseTeamItem):
    """
    Team Details -> Teams -> Team item -> Supported teams -> Team item
    """
    last_match: 'TeamItemSupportedTeamsTeamItemLastMatch' = HTField('LastMatch')
    next_match: 'TeamItemSupportedTeamsTeamItemNextMatch' = HTField('NextMatch')
    press_announcement: 'TeamItemSupportedTeamsTeamItemPress' = HTField('PressAnnouncement')


class TeamItemSupportedTeamsTeamItemLastMatch(HTModel):
    """
    Team Details -> Teams -> Team item -> Supported teams -> Team item -> Last Match
    """
    id: int = HTField('LastMatchId')
    date: datetime = HTField('LastMatchDate')
    home_team_id: int = HTField('LastMatchHomeTeamId')
    home_team_name: str = HTField('LastMatchHomeTeamName')
    home_goals: int = HTField('LastMatchHomeGoals')
    away_team_id: int = HTField('LastMatchAwayTeamId')
    away_team_name: str = HTField('LastMatchAwayTeamName')
    away_goals: int = HTField('LastMatchAwayGoals')


class TeamItemSupportedTeamsTeamItemNextMatch(HTModel):
    """
    Team Details -> Teams -> Team item -> Supported teams -> Team item -> Next Match
    """
    id: int = HTField('NextMatchId')
    date: datetime = HTField('NextMatchDate')
    home_team_id: int = HTField('NextMatchHomeTeamId')
    home_team_name: str = HTField('NextMatchHomeTeamName')
    away_team_id: int = HTField('NextMatchAwayTeamId')
    away_team_name: str = HTField('NextMatchAwayTeamName')


class TeamItemSupportedTeamsTeamItemPress(BasePress):
    """
    Team Details -> Teams -> Team item -> Supported teams -> Team item -> Press announcement
    """
    pass


class TeamItemSupporters(HTModel):
    """
    Team Details -> Teams -> Team item -> Supporters
    """
    total_items: int = HTField('.', attrib='TotalItems')
    max_items: int = HTField('.', attrib='MaxItems')
    teams: List['TeamItemSupportersTeamItem'] = HTField('.', items='SupportedTeam')


class TeamItemSupportersTeamItem(TeamItemSupportedTeamsOrSupportersBaseTeamItem):
    """
    Team Details -> Teams -> Team item -> Supporters -> Team item
    """
    pass
