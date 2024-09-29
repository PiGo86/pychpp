from typing import List

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestNationalTeams(HTModel):
    """
    National Teams - Request arguments
    """
    SOURCE_FILE = 'nationalteams'
    LAST_VERSION = '1.6'

    _r_league_office_type_id: int = HTInitVar('LeagueOfficeTypeID',
                                              init_arg='league_office_type_id')


class NationalTeams(RequestNationalTeams):
    """
    National Teams
    """
    user_supporter_tier: str = HTField('UserSupporterTier')
    league_office_type_id: int = HTField('LeagueOfficeTypeID')
    national_teams: List['NationalTeamItem'] = HTField('NationalTeams', items='NationalTeam')
    cups: List['CupItem'] = HTField('Cups', items='Cup')


class NationalTeamItem(HTModel):
    """
    National Teams -> National Teams -> National team item
    """
    id: int = HTField('NationalTeamID')
    name: str = HTField('NationalTeamName')
    dress: str = HTField('Dress')
    rating_scores: int = HTField('RatingScores')
    league_id: int = HTField('LeagueId')


class CupItem(HTModel):
    """
    National Teams -> Cups -> Cup item
    """
    id: int = HTField('CupID')
    cup_teams: List['CupItemCupTeamItem'] = HTField('CupTeams', items='CupTeam')


class CupItemCupTeamItem(HTModel):
    """
    National Teams -> Cups -> Cup item -> Cup Teams -> Cup Team item
    """
    id: int = HTField('CupNationalTeamID')
    name: str = HTField('CupNationalTeamName')
