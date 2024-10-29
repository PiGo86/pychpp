import datetime
from xml.etree import ElementTree

from pychpp.fixtures import ht_datetime


class HTXml:
    """
    Gather different method to parse xml files fetched on Hattrick
    """

    @staticmethod
    def ht_str(data: ElementTree.Element, attrib: str = None):
        if attrib is not None:
            return str(data.attrib.get(attrib, None))
        else:
            return str(data.text) if data.text is not None else None

    @staticmethod
    def ht_str_items(data: ElementTree.Element, item_tag: str):
        return [item.text for item in data.findall(item_tag)]

    @staticmethod
    def ht_int(data: ElementTree.Element, attrib: str = None):
        if attrib is not None:
            return int(data.attrib.get(attrib, None))
        else:
            return int(data.text) if data.text is not None else None

    @staticmethod
    def ht_float(data: ElementTree.Element, attrib: str = None):
        if attrib is not None:
            return float(data.attrib.get(attrib, None).replace(',', '.'))
        else:
            return float(data.text.replace(',', '.')) if data.text is not None else None

    @staticmethod
    def ht_bool(data: ElementTree.Element, attrib: str = None):
        if attrib is not None:
            value = data.attrib.get(attrib, None)
        else:
            value = data.text

        if value is None:
            return None
        elif value in ("0", "1"):
            return bool(int(value))
        else:
            return True if value.capitalize() == "True" else False

    @staticmethod
    def iter_data_items(data, item_tag):
        if data is not None:
            for item in data.findall(item_tag):
                yield item

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
    def ht_match_events(data):
        events = list()
        for event in data.findall('Event'):
            events.append({"minute": int(event.find("Minute").text),
                           "match_part": int(event.find("MatchPart").text),
                           "id": int(event.find("EventTypeID").text),
                           "variation": int(event.find("EventVariation").text),
                           "description": event.find("EventText").text,
                           "subject_team_id":
                               int(event.find("SubjectTeamID").text),
                           "subject_player_id":
                               int(event.find("SubjectPlayerID").text),
                           "object_player_id":
                               int(event.find("ObjectPlayerID").text),
                           })
        return events

    @staticmethod
    def ht_datetime_from_text(data: ElementTree.Element, attrib: str = None):
        """
        Converting strings from xml data to HTDatetime objects

        :param data: xml data representing a date and a time
        :param attrib: attr to fetch
        :return: a datetime object
        :rtype: ht_datetime.HTDatetime
        """
        if attrib is not None:
            _datetime = datetime.datetime.strptime(data.attrib.get(attrib), "%Y-%m-%d %H:%M:%S")
        else:
            _datetime = datetime.datetime.strptime(data.text, "%Y-%m-%d %H:%M:%S")
        return ht_datetime.HTDatetime(datetime=_datetime)

    @staticmethod
    def opt_ht_datetime_from_text(data: ElementTree.Element, attrib: str = None):
        """
        Converting strings from xml data to HTDatetime objects optionnaly

        :param data: xml data representing a date and a time
        :param attrib: attr to fetch
        :return: a datetime object or None
        :rtype: ht_datetime.HTDatetime | None
        """
        if attrib is not None:
            _data = data.attrib.get(attrib)
        else:
            _data = data.text

        if _data is None:
            return None
        else:
            _datetime = datetime.datetime.strptime(data.text, "%Y-%m-%d %H:%M:%S")

            # ValueError happens if text cannot be serialized
            # OverflowError happens with special datetimes
            # as 0001-01-01 9999-12-31 due to pytz limitations
            # In these cases, return None
            try:
                _ht_date = ht_datetime.HTDatetime(datetime=_datetime)
            except (ValueError, OverflowError):
                _ht_date = None

            return _ht_date

    @staticmethod
    def ht_datetime_to_text(_datetime):
        """
        Converting HTDatetime objects to string

        :param _datetime: a datetime object
        :type _datetime: datetime.datetime or ht_datetime.HTDatetime
        :return: a string representing a date and a time
        :rtype: str
        """

        # if a datetime instance is given
        # convert it to HTDatetime in CET timezone
        if isinstance(_datetime, datetime.datetime):
            _datetime = ht_datetime.HTDatetime(datetime=_datetime)

        _datetime.timezone = "CET"
        return _datetime.datetime.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def ht_date_to_text(_datetime):
        """
        Converting HTDatetime objects to string

        :param _datetime: a datetime object
        :type _datetime: datetime.datetime or ht_datetime.HTDatetime
        :return: a string representing a date and a time
        :rtype: str
        """

        # if a datetime instance is given
        # convert it to HTDatetime in CET timezone
        if isinstance(_datetime, datetime.datetime):
            _datetime = ht_datetime.HTDatetime(datetime=_datetime)

        _datetime.timezone = "CET"
        return _datetime.datetime.strftime("%Y-%m-%d")

    @staticmethod
    def to_string(data):
        return ElementTree.tostring(data, encoding='unicode')
