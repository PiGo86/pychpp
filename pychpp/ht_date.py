import datetime


class HTDate:
    """
    Manage Hattrick date
    """
    @classmethod
    def from_ht(cls, date_text):
        """
        Converting strings from xml data to datetime objects

        :param date_text: string representing a date and a time
        :type date_text: str
        :return: a datetime object
        :rtype: datetime.datetime
        """
        return datetime.datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S")
