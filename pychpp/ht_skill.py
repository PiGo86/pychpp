from pychpp.ht_error import HTSkillError


class HTCoreSkill:
    """
    Core Hattrick skill
    Used to create HTSkill and HTSkillYouth classes
    """
    SKILLS_NAME = set()
    SKILLS_TAG = set()

    def __init__(self, name):
        """See HTSkill or HTSkillYouth init"""
        if not {name} < self.SKILLS_NAME:
            raise HTSkillError(
                "Skill name must be one of : " + ", ".join(self.SKILLS_NAME))

        self.name = name

    def __repr__(self):
        """HTSkill or HTSkillYouth representation"""
        return f"<{self.__class__.__name__} object : {self.name}>"


class HTSkill(HTCoreSkill):
    """
    Hattrick senior skill
    """
    SKILLS_NAME = {"keeper", "defender", "playmaker", "winger", "scorer",
                   "passing", "set_pieces", "stamina"}
    SKILLS_TAG = {i: (i.title().replace("_", "") + "Skill")
                  for i in SKILLS_NAME}

    def __init__(self, name, level):
        """
        Initialization of a HTSkill instance :
        :param name: Name of skill (one of "keeper", "defender", "playmaker",
                     "winger", "scorer", "passing", "set_pieces")
        :param level: Level (from 0 to 30, knowing that player can be divin+1,
                      divin+2, etc...)
        :type name: str
        :type level: int, None
        :return: Hattrick skill for senior player
        :rtype: HTSkill
        """
        super().__init__(name=name)

        # Level attribute
        if level is None:
            self.level = None
        elif not isinstance(level, int) or level < 0:
            raise HTSkillError("Skill level must be positive integer")

        self.level = level

    def __str__(self):
        """Pretty print an HTSkill"""
        if self.level is None:
            return f"{self.name.title().replace('_', ' '):<12} : 'unknown' (?)"
        else:
            return f"{self.name.title().replace('_', ' '):<12} : " \
                   f"{'=' * int(self.level):<20} ({int(self.level)})"

    def __int__(self):
        """Return level (integer)"""
        return self.level


class HTSkillYouth(HTCoreSkill):
    """
    Hattrick Youth skill
    """

    SKILLS_NAME = {"keeper", "defender", "playmaker", "winger",
                   "scorer", "passing", "set_pieces"}
    SKILLS_TAG = {i: (i.title().replace("_", "") + "Skill",
                      i.title().replace("_", "") + "SkillMax")
                  for i in SKILLS_NAME}

    def __init__(self, name, level=None, maximum=None, maximum_reached=None):
        """
        Initialization of a HTSkillYouth instance :
        :param name: Name of skill (one of "keeper", "defender", "playmaker",
                     "winger", "scorer", "passing", "set_pieces")
        :param level: Level (from 0 to 8) (None if unknown)
        :param maximum: Maximum level (None if unknown)
        :param maximum_reached: If maximum is reached or not
        :type name: str
        :type level: int, None
        :type maximum: int
        :type maximum_reached: boolean
        :return: Hattrick skill for senior player
        :rtype: HTSkill
        """
        super().__init__(name=name)

        # Set maximum
        if maximum is not None and isinstance(maximum, int):
            if maximum > 8 or maximum < 0:
                raise HTSkillError(
                    "maximum must be postive and inferior than 9")
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
        Pretty print and HTSkillYouth, 4 differents cases possible :
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
        elif self.level is not None and self.maximum is None:
            diag = "=" * int(self.level) + "?" * (8 - int(self.level))
        else:
            diag = ("=" * int(self.level)
                    + " " * (self.maximum - int(self.level))
                    + "X" * (8 - self.maximum)
                    )

        return f"{header} {diag} {sumup(self.level, self.maximum)}"
