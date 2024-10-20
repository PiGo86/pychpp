from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestBookmarks(HTModel):
    """
    Bookmarks - Request arguments
    """
    SOURCE_FILE = 'bookmarks'
    LAST_VERSION = '1.0'

    _r_bookmark_type_id: Optional[int] = HTInitVar('bookmarkTypeID', init_arg='bookmark_type_id')


class Bookmarks(RequestBookmarks):
    """
    Bookmarks
    """
    bookmark_list: List['BookmarkItem'] = HTField('BookmarkList', items='Bookmark')


class BookmarkItem(HTModel):
    """
    Bookmarks -> Bookmark list -> Bookmark item
    """
    id: str = HTField('BookmarkID')
    type_id: int = HTField('BookmarkTypeID')
    text: str = HTField('Text')
    text_2: Optional[str] = HTField('Text2')
    object_id: str = HTField('ObjectID')
    object_id_2: Optional[str] = HTField('ObjectID2')
    object_id_3: Optional[str] = HTField('ObjectID3')
    comment: str = HTField('Comment')
