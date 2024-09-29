from datetime import datetime
from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class BaseRequestTraining(HTModel):
    """
    Base Training
    """
    SOURCE_FILE = 'training'
    LAST_VERSION = '2.2'

    _r_action_type: str = HTInitVar('actionType', init_arg='action_type', default='view')
    _r_team_id: int = HTInitVar('teamId', init_arg='team_id')


class RequestTrainingView(HTModel):
    """
    Base Training - View
    """
    _r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')


class RequestTrainingSetTraining(HTModel):
    """
    Base Training - Set training
    """
    _r_training_type: str = HTInitVar('trainingType', init_arg='training_type')
    _r_training_level: int = HTInitVar('trainingLevel', init_arg='training_level')
    _r_training_level_stamina: int = HTInitVar('trainingLevelStamina',
                                               init_arg='training_level_stamina')


class CommonTrainingViewSetTraining(BaseRequestTraining):
    """
    Training View or Set Training
    """
    XML_PREFIX = 'Team/'

    user_supporter_tier: str = HTField('../UserSupporterTier')
    team_id: int = HTField('TeamID')
    team_name: str = HTField('TeamName')
    training_level: int = HTField('TrainingLevel')
    new_training_level: int = HTField('NewTrainingLevel')
    training_type: int = HTField('TrainingType')
    stamina_training_part: int = HTField('StaminaTrainingPart')
    last_training: 'LastTraining' = HTField('.')
    trainer: 'Trainer' = HTField('Trainer')
    special_training: 'SpecialTraining' = HTField('SpecialTraining')
    morale: Optional[int] = HTField('Morale')
    self_confidence: Optional[int] = HTField('SelfConfidence')
    experience: 'Experience' = HTField('.')


class LastTraining(HTModel):
    """
    Training -> Last training
    """
    training_type: int = HTField('LastTrainingTrainingType')
    training_level: int = HTField('LastTrainingTrainingLevel')
    stamina_training_part: int = HTField('LastTrainingStaminaTrainingPart')


class Trainer(HTModel):
    """
    Training -> Trainer
    """
    id: int = HTField('TrainerID')
    name: str = HTField('TrainerName')
    arrival_date: datetime = HTField('ArrivalDate')


class SpecialTraining(HTModel):
    """
    Training -> Special training
    """
    players: List['SpecialTrainingPlayerItem'] = HTField('.', items='Player')
    trainer_name: Optional[str] = HTField('TrainerName')
    arrival_date: Optional[datetime] = HTField('ArrivalDate')


class SpecialTrainingPlayerItem(HTModel):
    """
    Training -> Special training -> Players -> Player item
    """
    id: Optional[int] = HTField('PlayerID')
    training_type_id: Optional[int] = HTField('SpecialTrainingTypeID')


class Experience(HTModel):
    """
    Training -> Experience
    """
    _442: int = HTField('Experience442')
    _433: int = HTField('Experience433')
    _451: int = HTField('Experience451')
    _352: int = HTField('Experience352')
    _532: int = HTField('Experience532')
    _343: int = HTField('Experience343')
    _541: int = HTField('Experience541')
    _523: int = HTField('Experience523')
    _550: int = HTField('Experience550')
    _253: int = HTField('Experience253')


class TrainingView(CommonTrainingViewSetTraining):
    """
    Training - View
    """
    pass


class TrainingSetTraining(CommonTrainingViewSetTraining):
    """
    Training - Set training
    """
    training_set: bool = HTField('TrainingSet')


class RequestTrainingStats(BaseRequestTraining):
    """
    Training - Stats - Request arguments
    """
    _r_league_id: int = HTInitVar('leagueID', init_arg='league_id')


class TrainingStats(RequestTrainingStats):
    """
    Training - Stats
    """
    league_id: int = HTField('LeagueID')
    league_name: str = HTField('LeagueName')
    training_stats: List['TrainingStatItem'] = HTField('TrainingStatList')


class TrainingStatItem(HTModel):
    """
    Training - Stats -> Stat item
    """
    # TODO: I don't know the xml output structure here
