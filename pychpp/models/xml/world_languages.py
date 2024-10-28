from typing import List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_model import HTModel


class RequestWorldLanguages(HTModel):
    """
    World Languages - Request arguments
    """
    SOURCE_FILE = 'worldlanguages'
    LAST_VERSION = '1.2'


class WorldLanguages(RequestWorldLanguages):
    """
    World Languages
    """
    language_list: List['LanguageItem'] = HTField('LanguageList', items='Language')


class LanguageItem(HTModel):
    """
    World Languages -> Language List -> Language item
    """
    id: int = HTField('LanguageID')
    name: str = HTField('LanguageName')
