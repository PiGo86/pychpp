from pychpp.models.custom import CustomModel
from pychpp.models.ht_init_var import HTInitVar


class BaseHTMatch(CustomModel):
    """
    Base model for Hattrick match, youth and senior
    """
    URL_PATH = '/Club/Matches/Match.aspx'

    _r_match_id = HTInitVar('matchID', fill_with='id')
    _r_source_system = HTInitVar('SourceSystem', fill_with='source_system')

    id: int
    home_team_name: str
    away_team_name: str
    source_system: str

    def __repr__(self):
        return (f"<{self.__class__.__name__} object - "
                f"{self.home_team_name} - {self.away_team_name} ({self.id})>")


class HTCommonLightMatch(BaseHTMatch):
    """
    Base model for Hattrick common light match
    """

    @property
    def is_youth(self):
        return self.source_system == 'Youth'

    @property
    def is_hto(self):
        return self.source_system == 'HTOIntegrated'

    def details(self, **kwargs):
        return self._chpp.match(id_=self.id, source_system=self.source_system, **kwargs)
