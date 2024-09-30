from datetime import datetime
from typing import List

from pychpp.models.ht_model import HTField, HTInitVar, HTModel


class RequestAchievements(HTModel):
    """
    Achievements - Request arguments
    """
    SOURCE_FILE = "achievements"
    LAST_VERSION = "1.2"

    _r_user_id: int = HTInitVar('userID', init_arg='user_id')


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
    title: str = HTField('AchievementTitle')
    text: str = HTField('AchievementText')
    category_id: int = HTField('CategoryID')
    event_date: datetime = HTField('EventDate')
    points: int = HTField('Points')
    multilevel: bool = HTField('MultiLevel')
    rank: int = HTField('Rank')
    number_of_events: int = HTField('NumberOfEvents')
