from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestNationalPlayers(HTModel):
    """
    National Players - Request arguments
    """
    SOURCE_FILE = 'nationalplayers'
    LAST_VERSION = '1.5'

    _r_action_type: Optional[str] = HTInitVar('actionType', init_arg='action_type')
    _r_team_id: int = HTInitVar('teamID', init_arg='team_id')
    _r_match_type_category: Optional[str] = HTInitVar('MatchTypeCategory',
                                                      init_arg='match_type_category')
    _r_show_all: Optional[bool] = HTInitVar('ShowAll', init_arg='show_all')


class NationalPlayersView(RequestNationalPlayers):
    """
    National Players - View
    """
    user_supporter_tier: str = HTField('UserSupporterTier')
    action_type: str = HTField('ActionType')
    team_id: int = HTField('TeamID')
    team_name: str = HTField('TeamName')
    players: List['ViewPlayerItem'] = HTField('Players', items='Player')


class ViewPlayerItem(HTModel):
    """
    National Players - View -> Players -> Player item
    """
    id: int = HTField('PlayerID')
    name: str = HTField('PlayerName')
    cards: int = HTField('Cards')
    specialty: int = HTField('Specialty')
    avatar: 'Avatar' = HTField('Avatar')


class Avatar(HTModel):
    """
    National Players - View -> Players -> Player item -> Avatar
    """
    background_image: str = HTField('BackgroundImage')
    layer: 'Layer' = HTField('Layer')


class Layer(HTModel):
    """
    National Players - View -> Players -> Player item -> Avatar -> Layer
    """
    x: int = HTField('.', attrib='x')
    y: int = HTField('.', attrib='y')
    image: str = HTField('Image')


class NationalPlayersStats(RequestNationalPlayers):
    """
    National Players - Supporter Stats
    """
    user_is_supporter: bool = HTField('UserIsSupporter')
    user_has_clubhouse: bool = HTField('UserHasClubhouse')
    action_type: str = HTField('ActionType')
    team_id: int = HTField('TeamID')
    team_name: str = HTField('TeamName')
    stats: 'Stats' = HTField('Stats')


class Stats(HTModel):
    """
    National Players - Supporter Stats -> Stats
    """
    match_type_category: str = HTField('MatchTypeCategory')
    show_all: bool = HTField('ShowAll')
    more_records_available: bool = HTField('MoreRecordsAvailable')
    players: List['PlayerItemStats'] = HTField('Players', items='Player')


class PlayerItemStats(HTModel):
    """
    National Players - Supporter Stats -> Stats -> Players -> Player item
    """
    id: int = HTField('PlayerID')
    name: str = HTField('PlayerName')
    nr_of_matches: int = HTField('NrOfMatches')
