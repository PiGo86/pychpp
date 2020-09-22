import xml.etree.ElementTree
from pychpp.ht_error import HTAgeError


class HTAge:
    """
    Hattrick Age
    """
    def __init__(self, age=None, age_days=None):
        """
        Initialization of a HTAge instance
        There are 2 ways to initialize instance.

        First one with integers
        :param age: Years
        :param age_days: Days
        :type age: int
        :type age_days: int

        Second one with ElementTree.Element
        :param age: Element with tag "Age"
        :type age: ElementTree.Element
        :param age_days: Element with tag "AgeDays"
        :type age_days: ElementTree.Element

        :returns: Hattrick age
        :rtype: HTAge
        """
        if isinstance(age, int) and isinstance(age_days, int):
            self.days = age * 112 + age_days
            self.age = age
            self.age_days = age_days
        elif (isinstance(age, xml.etree.ElementTree.Element)
              and isinstance(age_days, xml.etree.ElementTree.Element)):
            if age.tag != "Age" or age_days.tag != "AgeDays":
                raise HTAgeError("age must have tag 'Age' "
                                 "and age_days must have tag 'AgeDays'")
            else:
                self.days = int(age.text) * 112 + int(age_days.text)
                self.age = int(age.text)
                self.age_days = int(age_days.text)
        else:
            raise HTAgeError("age & age_days must be either int or Element")

    def __str__(self):
        """Pretty print an HTAge"""
        return f"{self.age} years and {self.age_days} days"

    def __repr__(self):
        """HTAge representation"""
        return f"<HTAge object : {self.__str__()}>"
