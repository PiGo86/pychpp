"""Models for the `alliances.xml` CHPP file."""

from typing import List, Optional

from pychpp.models.ht_model import HTField, HTInitVar, HTModel


class RequestAlliances(HTModel):
    """Alliances - Request arguments."""
    SOURCE_FILE = "alliances"
    LAST_VERSION = "1.5"

    _r_search_type: Optional[int] = HTInitVar('searchType', init_arg='search_type')
    _r_search_language_id: Optional[int] = HTInitVar('searchLanguageID',
                                                     init_arg='search_language_id')
    _r_search_for: str = HTInitVar('searchFor', init_arg='search_for')
    _r_page_index: Optional[int] = HTInitVar('pageIndex', init_arg='page_index')
    _r_user_id: Optional[int] = HTInitVar('userId', init_arg='user_id')


class Alliances(RequestAlliances):
    """Parsed data of the `alliances.xml` CHPP file."""
    pages: int = HTField('Pages')
    page_index: int = HTField('PageIndex')
    user_supporter_tier: str = HTField('UserSupporterTier', version='>=1.4')
    alliances: List['AllianceItem'] = HTField('Alliances', items='Alliance', xml_prefix='Alliance')


class AllianceItem(HTModel):
    """Alliances -> Alliances -> Alliance item."""
    id: int = HTField('ID')
    name: str = HTField('Name')
    description: str = HTField('Description')
