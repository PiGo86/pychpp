from typing import Optional, List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestSearch(HTModel):
    """
    Search - Request arguments
    """
    SOURCE_FILE = 'search'
    LAST_VERSION = '1.2'

    _r_search_type: Optional[int] = HTInitVar('searchType', init_arg='search_type')
    _r_search_string: Optional[str] = HTInitVar('searchString', init_arg='search_string')
    _r_search_string_2: Optional[int] = HTInitVar('searchString2', init_arg='search_string_2')
    _r_search_id: Optional[int] = HTInitVar('searchID', init_arg='search_id')
    _r_search_league_id: Optional[int] = HTInitVar('searchLeagueID', init_arg='search_league_id')
    _r_page_index: Optional[int] = HTInitVar('pageIndex', init_arg='page_index')


class Search(RequestSearch):
    """
    Search
    """
    search_params: 'SearchParams' = HTField('SearchParams')
    page_index: int = HTField('PageIndex')
    pages: int = HTField('Pages')
    search_results: List['ResultItem'] = HTField('SearchResults', items='Result')


class SearchParams(HTModel):
    """
    Search -> Search params
    """
    type: int = HTField('SearchType')
    string: str = HTField('SearchString')
    string_2: str = HTField('SearchString2')
    id: int = HTField('SearchID')
    league_id: int = HTField('SearchLeagueID')


class ResultItem(HTModel):
    """
    Search -> Search results -> Result item
    """
    id: int = HTField('ResultID')
    name: str = HTField('ResultName')
