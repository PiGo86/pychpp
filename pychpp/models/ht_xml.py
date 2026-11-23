"""Helpers to parse and format the xml data returned by the CHPP API."""

import datetime
from xml.etree import ElementTree

from pychpp.fixtures import ht_datetime


class HTXml:
    """Gather the different methods used to parse the xml files fetched on Hattrick."""

    @staticmethod
    def ht_str(data: ElementTree.Element, attrib: str = None):
        """Return the text of an xml element, or one of its attributes, as a string.

        Args:
            data: Xml element to read.
            attrib: Name of the attribute to read instead of the text.

        """
        if attrib is not None:
            return str(data.attrib.get(attrib, None))
        else:
            return str(data.text) if data.text is not None else None

    @staticmethod
    def ht_str_items(data: ElementTree.Element, item_tag: str):
        """Return the texts of all the children of an xml element with the given tag.

        Args:
            data: Xml element to read.
            item_tag: Tag of the children to read.

        """
        return [item.text for item in data.findall(item_tag)]

    @staticmethod
    def ht_int(data: ElementTree.Element, attrib: str = None):
        """Return the text of an xml element as an int ('Not available' becomes None).

        Args:
            data: Xml element to read.
            attrib: Name of the attribute to read instead of the text.

        """
        if attrib is not None:
            return int(data.attrib.get(attrib, None))
        else:
            if data.text == 'Not available' or data.text is None:
                return None
            else:
                return int(data.text)

    @staticmethod
    def ht_float(data: ElementTree.Element, attrib: str = None):
        """Return the text of an xml element as a float (comma replaced by dot).

        Args:
            data: Xml element to read.
            attrib: Name of the attribute to read instead of the text.

        """
        if attrib is not None:
            return float(data.attrib.get(attrib, None).replace(',', '.'))
        else:
            return float(data.text.replace(',', '.')) if data.text is not None else None

    @staticmethod
    def ht_bool(data: ElementTree.Element, attrib: str = None):
        """Return the text of an xml element as a bool.

        Args:
            data: Xml element to read.
            attrib: Name of the attribute to read instead of the text.

        """
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
        """Iterate over the children of an xml element with the given tag.

        Args:
            data: Xml element to read.
            item_tag: Tag of the children to iterate over.

        Yields:
            The matching child elements.

        """
        if data is not None:
            for item in data.findall(item_tag):
                yield item

    @staticmethod
    def ht_goals(data):
        """Parse the goals of a match xml node.

        Args:
            data: Xml node containing the Goal elements.

        Returns:
            A list of dicts describing each goal.

        """
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
        """Parse the events of a match xml node.

        Args:
            data: Xml node containing the Event elements.

        Returns:
            A list of dicts describing each event.

        """
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
        """Convert a string from xml data to a HTDatetime object.

        Args:
            data: Xml data representing a date and a time.
            attrib: Name of the attribute to fetch instead of the text.

        Returns:
            A HTDatetime object.

        """
        if attrib is not None:
            _datetime = datetime.datetime.strptime(data.attrib.get(attrib), "%Y-%m-%d %H:%M:%S")
        else:
            _datetime = datetime.datetime.strptime(data.text, "%Y-%m-%d %H:%M:%S")
        return ht_datetime.HTDatetime(datetime=_datetime)

    @staticmethod
    def opt_ht_datetime_from_text(data: ElementTree.Element, attrib: str = None):
        """Convert a string from xml data to a HTDatetime object, or None if empty.

        Args:
            data: Xml data representing a date and a time.
            attrib: Name of the attribute to fetch instead of the text.

        Returns:
            A HTDatetime object, or None if the data is empty or cannot be parsed.

        """
        if attrib is not None:
            data_ = data.attrib.get(attrib)
        else:
            data_ = data.text

        if data_ is None:
            return None
        else:
            if ':' in data_:
                datetime_ = datetime.datetime.strptime(data_, "%Y-%m-%d %H:%M:%S")
            else:
                datetime_ = datetime.datetime.strptime(data_, "%Y-%m-%d")

            # ValueError happens if text cannot be serialized
            # OverflowError happens with special datetimes
            # as 0001-01-01 9999-12-31 due to pytz limitations
            # In these cases, return None
            try:
                ht_date_ = ht_datetime.HTDatetime(datetime=datetime_)
            except (ValueError, OverflowError):
                ht_date_ = None

            return ht_date_

    @staticmethod
    def ht_datetime_to_text(_datetime):
        """Convert a datetime object to a string.

        Args:
            _datetime: A datetime or HTDatetime object.

        Returns:
            A string representing a date and a time, e.g. "2006-02-23 20:00:00".

        """
        # if a datetime instance is given
        # convert it to HTDatetime in CET timezone
        if isinstance(_datetime, datetime.datetime):
            _datetime = ht_datetime.HTDatetime(datetime=_datetime)

        _datetime.timezone = "CET"
        return _datetime.datetime.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def ht_date_to_text(_datetime):
        """Convert a datetime object to a date string.

        Args:
            _datetime: A datetime or HTDatetime object.

        Returns:
            A string representing a date, e.g. "2006-02-23".

        """
        # if a datetime instance is given
        # convert it to HTDatetime in CET timezone
        if isinstance(_datetime, datetime.datetime):
            _datetime = ht_datetime.HTDatetime(datetime=_datetime)

        _datetime.timezone = "CET"
        return _datetime.datetime.strftime("%Y-%m-%d")

    @staticmethod
    def to_string(data):
        """Serialize an xml element to a string.

        Args:
            data: Xml element to serialize.

        """
        return ElementTree.tostring(data, encoding='unicode')
