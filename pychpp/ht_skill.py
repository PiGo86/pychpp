youth_skills_names = {"Keeper", "Defender", "Playmaker", "Winger", "Scorer", "Passing", "SetPieces"}
senior_skills_names = youth_skills_names | {"Stamina"}
youth_skills_tag = {i: (i + "Skill", i + "SkillMax") for i in youth_skills_names}
senior_skills_tag = {i: (i + "Skill") for i in youth_skills_names}


class HTCoreSkill:
    """
    Core Hattrick skill
    Used to create HTSkill and HTSkillYouth classes
    """
    def __init__(self, name):
        # Name attribute
        if not {name} < senior_skills_names:
            raise HTSkillError("Skill name must be one of : " + ", ".join(senior_skills_names))

        self.name = name

    def __repr__(self):
        """Represent an HTSkill or HTSkillYouth"""
        return f"<{self.__class__.__name__} object : {self.name}>"


class HTSkill(HTCoreSkill):
    """
    Class that defines a skill with :
    :ivar name: Name of skill (one of Keeper, Defender, Playmaker, Winger, Scorer, Passing, SetPieces)
    :type name: str
    :ivar level: Level (from 0 to 30, knowing that player can be divin+1, divin+2, etc...)
    :type level: int 
    
    Initialize instance with parameter  :
    :param name: Name of the skill
    :type name: str
    :param level: Level
    :type level: int
    :returns: Hattrick single skill
    :rtype: HTSkill
    """

    def __init__(self, name, level):

        super().__init__(name=name)

        # Level attribute
        if level is None:
            self.level = None
        elif not isinstance(level, int) or level < 0:
            raise HTSkillError("Skill level must be positive integer")

        self.level = level

    def __str__(self):
        """Print an HTSkill"""
        if self.level is None:
            return f"{self.name:<12} : 'unknown' (?)"
        else:
            return f"{self.name:<12} : {'=' * int(self.level):<20} ({int(self.level)})"


class HTSkillYouth(HTCoreSkill):
    """
    Class HTSkillYouth inherits from HTSkill.
    It has 1 other attribute :
    :ivar maximum: Maximum level skill can reach.
    :type maximum: int

    Need one further parameter to initialize instance  :
    :param maximum: Maximum level. If unknown then None
    :type maximum: int
    :returns: Hattrick single youth skill
    :rtype: HTSkillYouth
    """

    def __init__(self, name, level=None, maximum=None, maximum_reached=None):

        super().__init__(name=name)

        # Set maximum
        if maximum is not None and isinstance(maximum, int):
            if maximum > 8 or maximum < 0:
                raise HTSkillError("maximum must be postive and inferior than 9")
            self.maximum = maximum
        else:
            self.maximum = None

        # Current level if available
        if level is None:
            self.level = None
        elif not isinstance(level, int):
            raise HTSkillError("Level must be integer")
        else:
            if maximum is not None and level > maximum:
                raise HTSkillError("Level can't be superior than maximum")
            self.level = level

        # Maximum reached
        if not isinstance(maximum_reached, bool):
            raise HTSkillError("maximum_reached must be boolean")
        else:
            self.maximum_reached = maximum_reached

    def __str__(self):
        """
        Represent an HTSkillYouth, 4 different cases possibles :
         - (?/?)
         - (2/?)
         - (?/2)
         - (2/2)
        """

        def sumup(level, maximum):
            level = "?" if level is None else round(level, 1)
            maximum = "?" if maximum is None else maximum
            return f"({level}/{maximum})"

        header = f"{self.name:<12} : "

        if self.level is None and self.maximum is None:
            diag = "?" * 8
        elif self.level is None:
            diag = "?" * self.maximum + "X" * (8 - self.maximum)
        elif self.maximum is None:
            diag = "=" * int(self.level) + "?" * (8 - int(self.level))
        else:
            diag = "=" * int(self.level) + " " * (self.maximum - int(self.level)) + "X" * (8 - self.maximum)

        return f"{header} {diag} {sumup(self.level, self.maximum)}"


class HTSkillError(Exception):
    pass
