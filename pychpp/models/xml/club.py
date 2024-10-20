from typing import Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestClub(HTModel):
    """
    Club - Request arguments
    """
    SOURCE_FILE = 'club'
    LAST_VERSION = '1.5'

    _r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')


class Club(RequestClub):
    """
    Club
    """
    team: 'Team' = HTField('Team')


class Team(HTModel):
    """
    Club -> Team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    staff: 'TeamStaff' = HTField('Staff')
    youth_squad: 'TeamYouthSquad' = HTField('YouthSquad')


class TeamStaff(HTModel):
    """
    Club -> Team -> Staff
    """
    assistant_trainer_levels: int = HTField('AssistantTrainerLevels')
    financial_director_levels: int = HTField('FinancialDirectorLevels')
    form_coach_levels: int = HTField('FormCoachLevels')
    medic_levels: int = HTField('MedicLevels')
    spokesperson_levels: int = HTField('SpokespersonLevels')
    sport_psychologist_levels: int = HTField('SportPsychologistLevels')
    tactical_assistant_levels: int = HTField('TacticalAssistantLevels')


class TeamYouthSquad(HTModel):
    """
    Club -> Team -> Youth Squad
    """
    investment: int = HTField('Investment')
    has_promoted: bool = HTField('HasPromoted')
    youth_level: int = HTField('YouthLevel')
