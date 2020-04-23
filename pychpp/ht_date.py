import datetime


class HTDate:

    @classmethod
    def from_ht(cls, date_text):
        return datetime.datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S")
