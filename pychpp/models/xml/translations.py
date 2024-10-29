from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestTranslations(HTModel):
    """
    Translations - Request arguments
    """
    SOURCE_FILE = 'translations'
    LAST_VERSION = '1.2'

    _r_language_id: Optional[int] = HTInitVar('languageId', init_arg='language_id')


class Translations(RequestTranslations):
    """
    Translations
    """
    id: int = HTField('Language', attrib='Id')
    name: str = HTField('Language')
    texts: 'Texts' = HTField('Texts')


class Texts(HTModel):
    """
    Translations -> Texts
    """
    skill_names: List['SkillNameItem'] = HTField('SkillNames', items='Skill')
    skill_levels: List['SkillLevelItem'] = HTField('SkillLevels', items='Level')
    skill_sub_levels: List['SkillSubLevelItem'] = HTField('SkillSubLevels', items='SubLevel')
    player_specialties: 'TranslationListItemValue' = HTField('PlayerSpecialties')
    player_agreeability: 'TranslationListLevelValue' = HTField('PlayerAgreeability')
    player_agressiveness: 'TranslationListLevelValue' = HTField('PlayerAgressiveness')
    player_honesty: 'TranslationListLevelValue' = HTField('PlayerHonesty')
    tactic_types: 'TranslationListItemValue' = HTField('TacticTypes')
    match_positions: 'TranslationListItemType' = HTField('MatchPositions')
    rating_sectors: 'TranslationListItemType' = HTField('RatingSectors')
    team_attitude: 'TranslationListLevelValue' = HTField('TeamAttitude')
    team_spirit: 'TranslationListLevelValue' = HTField('TeamSpirit')
    confidence: 'TranslationListLevelValue' = HTField('Confidence')
    training_types: 'TranslationListItemValue' = HTField('TrainingTypes')
    sponsors: 'TranslationListLevelValue' = HTField('Sponsors')
    fan_mood: 'TranslationListLevelValue' = HTField('FanMood')
    fan_match_expectations: 'TranslationListLevelValue' = HTField('FanMatchExpectations')
    fan_season_expectations: 'TranslationListLevelValue' = HTField('FanSeasonExpectations')
    league_names: List['LeagueItem'] = HTField('LeagueNames', items='League')


class SkillNameItem(HTModel):
    """
    Translations -> Skill Names -> Skill item
    """
    type: str = HTField('.', attrib='Type')
    type_name: str = HTField('.')


class SkillLevelItem(HTModel):
    """
    Translations -> Skill Levels -> Skill item
    """
    value: int = HTField('.', attrib='Value')
    value_name: str = HTField('.')


class SkillSubLevelItem(HTModel):
    """
    Translations -> Skill Levels -> Skill item
    """
    value: float = HTField('.', attrib='Value')
    value_name: str = HTField('.')


class TranslationListItemValue(HTModel):
    """
    Translations -> Translation list - Item-Value
    """
    label: str = HTField('.', attrib='Label')
    list: List['LevelOrItemValue'] = HTField('.', items='Item')


class TranslationListItemType(HTModel):
    """
    Translations -> Translation list - Item-Type
    """
    label: str = HTField('.', attrib='Label')
    list: List['LevelOrItemType'] = HTField('.', items='Item')


class TranslationListLevelValue(HTModel):
    """
    Translations -> Translation list - Level-Value
    """
    label: str = HTField('.', attrib='Label')
    list: List['LevelOrItemValue'] = HTField('.', items='Level')


class LevelOrItemValue(HTModel):
    """
    Translations -> Translation list -> Translation list item - Level or Item with Value
    """
    value: int = HTField('.', attrib='Value')
    label: str = HTField('.')


class LevelOrItemType(HTModel):
    """
    Translations -> Translation list -> Translation list item - Level or Item with Type
    """
    type: str = HTField('.', attrib='Type')
    label: str = HTField('.')


class LeagueItem(HTModel):
    """
    Translations -> League Names -> League item
    """
    id: int = HTField('LeagueId')
    local_name: str = HTField('LocalLeagueName')
    language_name: str = HTField('LanguageLeagueName')
