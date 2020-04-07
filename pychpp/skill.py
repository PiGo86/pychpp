import xml

all_skills = {"Keeper", "Defender", "Playmaker", "Winger", "Scorer", "Passing", "SetPieces"}
tag_skill = {i + "Skill" for i in all_skills}
tag_skillMax = {i + "SkillMax" for i in all_skills}


class HTSkill:
    """
    Class that defines a skill with :
    :ivar name: Name of skill (one of Keeper, Defender, Playmaker, Winger, Scorer, Passing, SetPieces)
    :type name: str
    :ivar level: Level (from 0 to 30, knowing that player can be divin+1, divin+2, etc...)
    :type level: int 
    
    Initialize instance with parameter  :
    :param xml_skill: Element with tag 'Skill' + skillname (ex: SkillPlaymaker)
    :type xml_skill: ElementTree.Element
    :returns: Hattrick single skill
    :rtype: HTSkill
    """

    def __init__(self, xml_skill):
        # Check on xml_skill
        if not isinstance(xml_skill, xml.etree.ElementTree.Element) or \
                not {xml_skill.tag} < tag_skill:
            raise HTSkillError("xml_skill must be and ElementTree.Element with a skill tag containing numeric value")

        # Name attribute
        self.name = xml_skill.tag.split("Skill")[0]

        # Level attribute
        if xml_skill.text is None or \
                not xml_skill.text.isnumeric():
            raise HTSkillError("skill value not defined")
        self.level = int(xml_skill.text)

    def __repr__(self):
        """Represent an HTSkill"""
        return f"{self.name:<12} : {'=' * int(self.level):<20} ({int(self.level)})"


class HTSkillYouth(HTSkill):
    """
    Class HTSkillYouth inherits from HTSkill.
    It has 1 other attribute :
    :ivar maximum: Maximum level skill can reach.
    :type name: int

    Need one further parameter to be initialize instance  :
    :param xml_skillMax: Element with tag 'SkillMax' + skillname (ex: SkillPlaymaker)
    :type xml_skillMax: ElementTree.Element
    :returns: Hattrick single skill
    :rtype: HTSkillYouth
    """

    def __init__(self, xml_skill, xml_skillMax):
        """
        Initialize a SkillYouth object with :
            - xml_skill (type ElementTree.Element)
            - xml_skillMax (type ElementTree.Element)
        """

        # Check on xml_skillMax
        if not isinstance(xml_skillMax, xml.etree.ElementTree.Element) or \
                not {xml_skillMax.tag} < tag_skillMax:
            raise HTSkillError("xml_skill must be and ElementTree.Element with a skillMax tag")

        if not xml_skill.tag.split("Skill")[0] == xml_skillMax.tag.split("Skill")[0]:
            raise HTSkillError("xml_skill & xml_skillMax don't match !")

        # Name attribute
        self.name = xml_skill.tag.split("Skill")[0]

        # Maximum if available
        if xml_skillMax.attrib["IsAvailable"] == "False":
            self.maximum = None
        else:
            maximum = int(xml_skillMax.text)
            if maximum < 0 or maximum > 8:
                raise HTSkillError('Maximum must be between 0 and 8')
            else:
                self.maximum = maximum

        # Current level if available
        if xml_skill.attrib["IsAvailable"] == "False":
            self.level = None
        else:
            level = int(xml_skill.text)
            if xml_skillMax.attrib["IsAvailable"] == "True":
                if level > self.maximum:
                    raise HTSkillError('Level can\'t be superior than maximum')
            self.level = int(xml_skill.text)

    def max_reached(self):
        if self.maximum is not None and int(self.level) == int(self.maximum):
            return True
        else:
            return False

    def __repr__(self):
        """
        Represent an HTSkillYouth, 4 differents cases possibles :
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