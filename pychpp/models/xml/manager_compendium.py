from typing import List, Optional

from pychpp.models import ht_model
from pychpp.models.ht_model import HTField, HTInitVar, HTAliasField


class ManagerCompendium(ht_model.HTModel):
    """
    Manager Compendium
    """

    SOURCE_FILE = "managercompendium"
    LAST_VERSION = "1.5"
    URL_PATH = "/Club/Manager"

    ht_id: int = HTInitVar(param='userId')

    login_name: str = HTField(path='Manager/Loginname')
    username: str = HTAliasField(target='login_name')
    supporter_tier: str = HTField(path='Manager/SupporterTier')
    last_logins: List[str] = HTField(path='Manager/LastLogins', items='LoginTime')
    language: 'Language' = HTField(path='Manager/Language')
    country: 'Country' = HTField(path='Manager/Country')
    currency: 'Currency' = HTField(path='Manager/Currency')
    teams: List['TeamItem'] = HTField(path='Manager/Teams', items='Team')
    national_teams_coach: List['NationalTeamItem'] = HTField(path='Manager/NationalTeamCoach', items='NationalTeam')
    national_teams_assistant: List['NationalTeamItem'] = HTField(path='Manager/NationalTeamAssistant', items='NationalTeam')
    avatar: 'Avatar' = HTField(path='Manager/Avatar')


class Language(ht_model.HTModel):
    """
    managercompendium -> Language
    """
    id: int = HTField(path='LanguageId')
    name: str = HTField(path='LanguageName')


class Country(ht_model.HTModel):
    """
    managercompendium -> Country
    """
    id: int = HTField(path='CountryId')
    name: str = HTField(path='CountryName')


class Currency(ht_model.HTModel):
    """
    managercompendium -> Currency
    """
    name: str = HTField(path='CurrencyName')
    rate: float = HTField(path='CurrencyRate')


class TeamItem(ht_model.HTModel):
    """
    managercompendium -> Teams -> Team item
    """
    id: int = HTField(path='TeamId')
    name: str = HTField(path='TeamName')
    arena: 'TeamItemArena' = HTField(path='Arena')
    league: 'TeamItemLeague' = HTField(path='League')
    country: 'TeamItemCountry' = HTField(path='Country')
    league_level_unit: 'TeamItemLeagueLevelUnit' = HTField(path='LeagueLevelUnit')
    region: 'TeamItemRegion' = HTField(path='Region')
    youth_team: Optional['TeamItemYouthTeam'] = HTField(path='YouthTeam')


class TeamItemArena(ht_model.HTModel):
    """
    managercompendium -> Teams -> Team item -> Arena
    """
    id: int = HTField(path='ArenaId')
    name: str = HTField(path='ArenaName')


class TeamItemLeague(ht_model.HTModel):
    """
    managercompendium -> Teams -> Team item -> League
    """
    id: int = HTField(path='LeagueId')
    name: str = HTField(path='LeagueName')
    season: int = HTField(path='Season')


class TeamItemCountry(ht_model.HTModel):
    """
    managercompendium -> Teams -> Team item -> Country
    """
    id: int = HTField(path='CountryId')
    name: str = HTField(path='CountryName')


class TeamItemLeagueLevelUnit(ht_model.HTModel):
    """
    managercompendium -> Teams -> Team item -> League Level Unit
    """
    id: int = HTField(path='LeagueLevelUnitId')
    name: str = HTField(path='LeagueLevelUnitName')


class TeamItemRegion(ht_model.HTModel):
    """
    managercompendium -> Teams -> Team item -> Region
    """
    id: int = HTField(path='RegionId')
    name: str = HTField(path='RegionName')


class TeamItemYouthTeam(ht_model.HTModel):
    """
    managercompendium -> Teams -> Team item -> Youth team
    """
    id: int = HTField(path='YouthTeamId')
    name: str = HTField(path='YouthTeamName')
    league: 'TeamItemYouthTeamLeague' = HTField(path='YouthLeague')


class TeamItemYouthTeamLeague(ht_model.HTModel):
    """
    managercompendium -> Teams -> Team item -> Youth team -> League
    """
    id: int = HTField(path='YouthLeagueId')
    name: str = HTField(path='YouthLeagueName')


class NationalTeamItem(ht_model.HTModel):
    """
    managercompendium -> National teams (coach or assistant) -> National team item
    """
    id: int = HTField(path='NationalTeamId')
    name: str = HTField(path='NationalTeamName')


class Avatar(ht_model.HTModel):
    """
    managercompendium -> Avatar
    """
    background_image: str = HTField(path='BackgroundImage')
    layers: List['AvatarLayer'] = HTField(path='../..', items='Layer')


class AvatarLayer(ht_model.HTModel):
    """
    managercompendium -> Avatar -> Layers -> Layer item
    """
    x: int = HTField(path='../..', attrib='x')
    y: int = HTField(path='../..', attrib='y')
    image: str = HTField(path='Image')
