from pychpp.models.custom import CustomModel
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.xml import youth_player_details as ypd


class BaseCommonHTPlayer(CustomModel):
    """
    Base model for Hattrick player, youth and senior
    """
    id: int
    first_name: str
    last_name: str

    def __repr__(self):
        return (f"<{self.__class__.__name__} object - "
                f"{self.first_name} {self.last_name} ({self.id})>")


class HTCommonLightPlayer(BaseCommonHTPlayer):
    """
    Base model for common Hattrick light player
    """
    is_youth: bool

    @property
    def url(self):
        if not self._url:
            if self.is_youth:
                self._url = self._BASE_URL + (f"/Club/Players/YouthPlayer.aspx"
                                              f"?youthPlayerID={self.id}")
            else:
                self._url = self._BASE_URL + (f"/Club/Players/Player.aspx"
                                              f"?playerID={self.id}")
        return self._url

    def details(self, **kwargs):
        if self.is_youth:
            return self._chpp.youth_player(id_=self.id, **kwargs)
        else:
            return self._chpp.player(id_=self.id, **kwargs)


class HTLightPlayer(BaseCommonHTPlayer):
    """
    Base model for Hattrick light player
    """
    URL_PATH = '/Club/Players/Player.aspx'

    # not used for fetching data, but to allow url property to work correctly
    _r_id = HTInitVar(param='playerID', init_arg='id_', fill_with='id')

    def details(self, **kwargs):
        return self._chpp.player(id_=self.id, **kwargs)


class HTLightYouthPlayer(BaseCommonHTPlayer):
    """
    Base model for Hattrick light youth player
    """
    URL_PATH = '/Club/Players/YouthPlayer.aspx'

    # not used for fetching data, but to allow url property to work correctly
    _r_id = HTInitVar(param='youthPlayerID', init_arg='id_', fill_with='id')

    def details(self, **kwargs):
        return self._chpp.youth_player(id_=self.id, **kwargs)


class HTYouthPlayerSkills(CustomModel, ypd.Skills):
    """
    Hattrick youth player skills
    """
    def __str__(self):
        """
        Pretty print of HTSkillYouth, 4 different cases possible :
         - (?/?)
         - (X/?)
         - (?/Y)
         - (X/Y)
        """

        def sumup(level_, max_level_):
            level_ = "?" if level_ is None else round(level_, 1)
            max_level_ = "?" if max_level_ is None else max_level_
            return f"({level_}/{max_level_})"

        skill_print = ""

        for skill_name in ('keeper', 'defender', 'playmaker', 'winger',
                           'scorer', 'passing', 'set_pieces'):

            header = f"{skill_name.replace('_', ' ').title():<10} : "

            skill: ypd.SkillsSkillItem = getattr(self, skill_name)
            level = skill.skill.level if skill.skill.is_available else None
            max_level = skill.skill_max.level if skill.skill_max.is_available else None

            if level is None and max_level is None:
                diag = "?" * 8
            elif level is None:
                diag = "?" * max_level + "X" * (8 - max_level)
            elif level is not None and max_level is None:
                diag = "=" * level + "?" * (8 - level)
            else:
                diag = ("=" * level
                        + " " * (max_level - level)
                        + "X" * (8 - max_level)
                        )

            skill_print += "\n" if skill_print else ""
            skill_print += f"{header} {diag} {sumup(level, max_level)}"

        return skill_print


class HTAge(CustomModel):
    years: int
    days: int

    def _age_in_days(self):
        return self.years * 112 + self.days

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self._age_in_days() < other._age_in_days()
        else:
            return TypeError(f"can not compare {other.__class__.__name__}"
                             f" instance with HTAge instance")

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self._age_in_days() <= other._age_in_days()
        else:
            return TypeError(f"can not compare {other.__class__.__name__}"
                             f" instance with HTAge instance")

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._age_in_days() == other._age_in_days()
        else:
            return TypeError(f"can not compare {other.__class__.__name__}"
                             f" instance with HTAge instance")

    def __str__(self):
        """Pretty print an HTAge"""
        return f"{self.years} years and {self.days} days"

    def __repr__(self):
        """HTAge representation"""
        return f"<HTAge object : {self.__str__()}>"
