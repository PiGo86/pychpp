"""Light model used as a base for the custom models."""

from pychpp.models.custom import CustomModel
from pychpp.models.ht_init_var import HTInitVar
from typing import Any


class BaseCommonHTTeam(CustomModel):
    """Common base model for Hattrick team (senior and youth)."""
    id: int
    name: str

    def __repr__(self):
        return (f"<{self.__class__.__name__} object - "
                f"{self.name} ({self.id})>")


class HTCommonLightTeam(BaseCommonHTTeam):
    """Base model for Hattrick light team (senior and youth)."""
    source_system: str

    @property
    def is_youth(self):
        """Whether the team is a youth team."""
        return self.source_system == 'Youth'

    @property
    def is_hto(self):
        """Whether the team is a HTO integrated team."""
        return self.source_system == 'HTOIntegrated'

    @property
    def url(self):
        """Url of this team on hattrick.org."""
        if not self._url:
            if self.is_youth:
                self._url = self._BASE_URL + (f"/Club/Youth/"
                                              f"?youthTeamID={self.id}")
            else:
                self._url = self._BASE_URL + (f"/Club/"
                                              f"?teamID={self.id}")
        return self._url

    def details(self, **kwargs: Any):
        """Get the full details of this team (youth or senior)."""
        if self.is_youth:
            return self._chpp.youth_team(id_=self.id, **kwargs)
        else:
            return self._chpp.team(id_=self.id, **kwargs)


class BaseHTTeam(BaseCommonHTTeam):
    """Base model for Hattrick team."""
    URL_PATH = '/Club/'


class HTLightTeam(BaseHTTeam):
    """Hattrick light team."""

    _r_id = HTInitVar(param='teamID', init_arg='id_', fill_with='id')

    def details(self):
        """Get the full details of this team."""
        return self._chpp.team(id_=self.id)


class BaseHTYouthTeam(BaseCommonHTTeam):
    """Base model for Hattrick youth team."""
    URL_PATH = '/Club/Youth/'


class HTLightYouthTeam(BaseHTYouthTeam):
    """Hattrick light youth team."""

    _r_id = HTInitVar(param='youthTeamID', init_arg='id_', fill_with='id')

    def details(self, **kwargs: Any):
        """Get the full details of this youth team."""
        return self._chpp.youth_team(id_=self.id, **kwargs)
