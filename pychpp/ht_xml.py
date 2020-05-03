import datetime

from pychpp import ht_skill, ht_age


class HTXml:
    """
    Gather different method to parse xml files fetched on Hattrick
    """
    @staticmethod
    def ht_str(data):
        return str(data.text)

    @staticmethod
    def ht_int(data):
        return int(data.text)

    @staticmethod
    def ht_bool(data):
        return True if data.text.capitalize() == "True" else False

    @staticmethod
    def ht_goals(data):
        goals = list()
        for goal in data.findall('Goal'):
            goals.append({"player_id": int(goal.find("ScorerPlayerID").text),
                          "player_name": goal.find("ScorerPlayerName").text,
                          "home_goals": int(goal.find("ScorerHomeGoals").text),
                          "away_goals": int(goal.find("ScorerAwayGoals").text),
                          "minute": int(goal.find("ScorerMinute").text),
                          "match_part": int(goal.find("MatchPart").text),
                          })
        return goals

    @staticmethod
    def ht_date_from_text(data):
        """
        Converting strings from xml data to datetime objects

        :param data: xml data representing a date and a time
        :type data: ElementTree.Element
        :return: a datetime object
        :rtype: datetime.datetime
        """
        return datetime.datetime.strptime(data.text, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def ht_date_to_text(_date):
        """
        Converting strings from xml data to datetime objects

        :param _date: a datetime object
        :type _date: datetime.datetime
        :return: a string representing a date and a time
        :rtype: str
        """
        return _date.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def ht_match_list(data):
        matches_id = list()
        for match in data.findall('Match'):
            matches_id.append(int(match.find("MatchID").text))
        return matches_id

    @classmethod
    def ht_arena_capacity(cls, data):

        capacity = dict()

        if data.tag not in ("CurrentCapacity", "ExpandedCapacity"):
            raise ValueError("root tag must be equal to 'CurrentCapacity or 'ExpandedCapacity'")

        elif (data.tag == "CurrentCapacity"
              or (data.tag == "ExpandedCapacity" and data.attrib["Available"] == "True")):

            if data.find("RebuiltDate") is not None and data.find("RebuiltDate").attrib["Available"] == "True":
                capacity['rebuilt_date'] = cls.ht_date_from_text(data.find("RebuiltDate"))
            elif data.find("ExpandedDate") is not None and data.find("ExpandedDate").attrib["Available"] == "True":
                capacity['expanded_date'] = cls.ht_date_from_text(data.find("ExpandedDate"))

            capacity["terraces"] = int(data.find("Terraces").text)
            capacity["basic"] = int(data.find("Basic").text)
            capacity["roof"] = int(data.find("Roof").text)
            capacity["vip"] = int(data.find("VIP").text)
            capacity["total"] = int(data.find("Total").text)

        return capacity if capacity else None

    @staticmethod
    def ht_skills(data):
        skills = {k: ht_skill.HTSkill(name=k,
                                      level=int(data.find(v).text)
                                      if data.find(v) is not None else None)
                  for k, v in ht_skill.HTSkill.SKILLS_TAG.items()}

        return skills

    @staticmethod
    def ht_youth_skills(data):
        skills = {k: ht_skill.HTSkillYouth(name=k,
                                           level=(int(data.find(v[0]).text)
                                                  if data.find(v[0]).attrib["IsAvailable"] == "True" else None),
                                           maximum=(int(data.find(v[1]).text)
                                                    if data.find(v[1]).attrib["IsAvailable"] == "True" else None),
                                           maximum_reached=bool(data.find(v[0]).attrib["IsMaxReached"]))
                  for k, v in ht_skill.HTSkillYouth.SKILLS_TAG.items()}

        return skills

    @staticmethod
    def ht_age(data):
        return ht_age.HTAge(age=int(data.find("Age").text), age_days=int(data.find("AgeDays").text))

    @staticmethod
    def ht_last_logins(data):
        return [login.text for login in data.findall("LoginTime")]

    @staticmethod
    def ht_teams_ht_id(data):
        return [int(t.find("TeamId").text) for t in data.findall("Team")]
