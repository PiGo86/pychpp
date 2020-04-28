import datetime


class HTXml:

    @staticmethod
    def ht_str(data):
        return str(data.text)

    @staticmethod
    def ht_int(data):
        return int(data.text)

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
    def ht_date(data):
        """
        Converting strings from xml data to datetime objects

        :param data: xml data representing a date and a time
        :type data: ElementTree.Element
        :return: a datetime object
        :rtype: datetime.datetime
        """
        return datetime.datetime.strptime(data.text, "%Y-%m-%d %H:%M:%S")
