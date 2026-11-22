from datetime import datetime
from typing import List, Optional

from pychpp.models.ht_model import HTField, HTInitVar, HTModel


class RequestAchievements(HTModel):
    """
    Achievements - Request arguments
    """
    SOURCE_FILE = "achievements"
    LAST_VERSION = "1.4"

    _r_user_id: Optional[int] = HTInitVar('userID', init_arg='user_id')


class Achievements(RequestAchievements):
    """
    Achievements
    """
    max_points: int = HTField('MaxPoints')
    achievements: List['Achievement'] = HTField('AchievementList', items='Achievement')


class Achievement(HTModel):
    """
    Achievements -> Achievements -> Achievement item
    """
    type_id: int = HTField('AchievementTypeID')
    title: str = HTField('AchievementTitle', version='>=1.2')
    text: str = HTField('AchievementText')
    category_id: int = HTField('CategoryID')
    category_group_id: int = HTField('CategoryGroupID', version='>=1.4')
    event_date: datetime = HTField('EventDate')
    points: int = HTField('Points')
    multilevel: bool = HTField('MultiLevel')
    rank: int = HTField('Rank', version='>=1.1')
    number_of_events: int = HTField('NumberOfEvents')
    completed: bool = HTField('Completed', version='>=1.3')
    max_points: int = HTField('MaxPoints', version='>=1.3')
    progress_value: Optional[int] = HTField('ProgressValue', version='>=1.3')
    progress_value_date: Optional[datetime] = HTField('ProgressValueDate', version='>=1.3')
    current_variation: Optional['AchievementVariation'] = HTField('CurrentVariation',
                                                                  version='>=1.3')
    next_variation: Optional['AchievementVariation'] = HTField('NextVariation',
                                                               version='>=1.3')


class AchievementVariation(HTModel):
    """
    Achievements -> Achievement -> Current/Next variation
    """
    rank: int = HTField('Rank')
    value_to_achieve: int = HTField('ValueToAchieve')
    points: int = HTField('Points')
