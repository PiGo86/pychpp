from typing import List, Optional

from pychpp.models.ht_model import HTField, HTInitVar, HTModel


class RequestManagerCompendium(HTModel):
    """
    Manager Compendium - Request arguments
    """
    SOURCE_FILE = "managercompendium"
    LAST_VERSION = "1.5"

    _r_user_id: Optional[int] = HTInitVar(param='userID', init_arg='user_id', fill_with='id')


class ManagerCompendium(RequestManagerCompendium):
    """
    Manager Compendium
    """
    id: int = HTField(path='Manager/UserId')
    login_name: str = HTField(path='Manager/Loginname')
    supporter_tier: str = HTField(path='Manager/SupporterTier')
    last_logins: List[str] = HTField(path='Manager/LastLogins', items='LoginTime')
    language: 'Language' = HTField(path='Manager/Language')
    country: 'Country' = HTField(path='Manager/Country')
    currency: 'Currency' = HTField(path='Manager/Currency')
    teams: List['TeamItem'] = HTField(path='Manager/Teams', items='Team')
    national_teams_coach: List['NationalTeamItem'] = HTField(path='Manager/NationalTeamCoach',
                                                             items='NationalTeam')
    national_teams_assistant: List['NationalTeamItem'] = HTField(
        path='Manager/NationalTeamAssistant', items='NationalTeam',
    )
    avatar: 'Avatar' = HTField(path='Manager/Avatar')


class Language(HTModel):
    """
    Manager Compendium -> Language
    """
    id: int = HTField(path='LanguageId')
    name: str = HTField(path='LanguageName')


class Country(HTModel):
    """
    Manager Compendium -> Country
    """
    id: int = HTField(path='CountryId')
    name: str = HTField(path='CountryName')


class Currency(HTModel):
    """
    Manager Compendium -> Currency
    """
    name: str = HTField(path='CurrencyName')
    rate: float = HTField(path='CurrencyRate')


class TeamItem(HTModel):
    """
    Manager Compendium -> Teams -> Team item
    """
    id: int = HTField(path='TeamId')
    name: str = HTField(path='TeamName')
    arena: 'TeamItemArena' = HTField(path='Arena')
    league: 'TeamItemLeague' = HTField(path='League')
    country: 'TeamItemCountry' = HTField(path='Country')
    league_level_unit: 'TeamItemLeagueLevelUnit' = HTField(path='LeagueLevelUnit')
    region: 'TeamItemRegion' = HTField(path='Region')
    youth_team: Optional['TeamItemYouthTeam'] = HTField(path='YouthTeam')


class TeamItemArena(HTModel):
    """
    Manager Compendium -> Teams -> Team item -> Arena
    """
    id: int = HTField(path='ArenaId')
    name: str = HTField(path='ArenaName')


class TeamItemLeague(HTModel):
    """
    Manager Compendium -> Teams -> Team item -> League
    """
    id: int = HTField(path='LeagueId')
    name: str = HTField(path='LeagueName')
    season: int = HTField(path='Season')


class TeamItemCountry(HTModel):
    """
    Manager Compendium -> Teams -> Team item -> Country
    """
    id: int = HTField(path='CountryId')
    name: str = HTField(path='CountryName')


class TeamItemLeagueLevelUnit(HTModel):
    """
    Manager Compendium -> Teams -> Team item -> League Level Unit
    """
    id: int = HTField(path='LeagueLevelUnitId')
    name: str = HTField(path='LeagueLevelUnitName')


class TeamItemRegion(HTModel):
    """
    Manager Compendium -> Teams -> Team item -> Region
    """
    id: int = HTField(path='RegionId')
    name: str = HTField(path='RegionName')


class TeamItemYouthTeam(HTModel):
    """
    Manager Compendium -> Teams -> Team item -> Youth team
    """
    id: int = HTField(path='YouthTeamId')
    name: str = HTField(path='YouthTeamName')
    league: 'TeamItemYouthTeamLeague' = HTField(path='YouthLeague')


class TeamItemYouthTeamLeague(HTModel):
    """
    Manager Compendium -> Teams -> Team item -> Youth team -> League
    """
    id: int = HTField(path='YouthLeagueId')
    name: str = HTField(path='YouthLeagueName')


class NationalTeamItem(HTModel):
    """
    Manager Compendium -> National teams (coach or assistant) -> National team item
    """
    id: int = HTField(path='NationalTeamId')
    name: str = HTField(path='NationalTeamName')


class Avatar(HTModel):
    """
    Manager Compendium -> Avatar
    """
    background_image: str = HTField(path='BackgroundImage')
    layers: Optional[List['AvatarLayer']] = HTField(path='../..', items='Layer')


class AvatarLayer(HTModel):
    """
    Manager Compendium -> Avatar -> Layers -> Layer item
    """
    x: int = HTField(path='../..', attrib='x')
    y: int = HTField(path='../..', attrib='y')
    image: str = HTField(path='Image')
