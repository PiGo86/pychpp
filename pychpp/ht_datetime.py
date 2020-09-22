import datetime as dt
import pytz


class HTDatetime:
    """
    Hattrick datetime
    Give Hattrick season, week and weekday according to calendar datetime and
    calendar time according to Hattrick season, week and weekday
    """

    _ORIGIN_DATE = dt.datetime(1997, 9, 22, 0, 0)

    _LEAGUES_MAP = {
        'Sweden': {'id': 1, 'season_offset': 0},
        'England': {'id': 2, 'season_offset': 0},
        'Germany': {'id': 3, 'season_offset': 0},
        'Italy': {'id': 4, 'season_offset': 0},
        'France': {'id': 5, 'season_offset': 0},
        'Mexico': {'id': 6, 'season_offset': 0},
        'Argentina': {'id': 7, 'season_offset': 0},
        'USA': {'id': 8, 'season_offset': 0},
        'Norway': {'id': 9, 'season_offset': -11},
        'Denmark': {'id': 11, 'season_offset': 0},
        'Finland': {'id': 12, 'season_offset': 0},
        'Netherlands': {'id': 14, 'season_offset': -11},
        'Oceania': {'id': 15, 'season_offset': -12},
        'Brazil': {'id': 16, 'season_offset': -12},
        'Canada': {'id': 17, 'season_offset': -12},
        'Chile': {'id': 18, 'season_offset': -12},
        'Colombia': {'id': 19, 'season_offset': -12},
        'India': {'id': 20, 'season_offset': -12},
        'Ireland': {'id': 21, 'season_offset': -12},
        'Japan': {'id': 22, 'season_offset': -12},
        'Peru': {'id': 23, 'season_offset': -12},
        'Poland': {'id': 24, 'season_offset': -12},
        'Portugal': {'id': 25, 'season_offset': -12},
        'Scotland': {'id': 26, 'season_offset': -12},
        'South Africa': {'id': 27, 'season_offset': -12},
        'Uruguay': {'id': 28, 'season_offset': -12},
        'Venezuela': {'id': 29, 'season_offset': -12},
        'South Korea': {'id': 30, 'season_offset': -12},
        'Thailand': {'id': 31, 'season_offset': -12},
        'Turkey': {'id': 32, 'season_offset': -12},
        'Egypt': {'id': 33, 'season_offset': -12},
        "People's Republic of China": {'id': 34, 'season_offset': -12},
        'Russia': {'id': 35, 'season_offset': -12},
        'Spain': {'id': 36, 'season_offset': -12},
        'Romania': {'id': 37, 'season_offset': -12},
        'Iceland': {'id': 38, 'season_offset': -13},
        'Austria': {'id': 39, 'season_offset': -13},
        'Belgium': {'id': 44, 'season_offset': -13},
        'Malaysia': {'id': 45, 'season_offset': -13},
        'Switzerland': {'id': 46, 'season_offset': -13},
        'Singapore': {'id': 47, 'season_offset': -13},
        'Greece': {'id': 50, 'season_offset': -15},
        'Hungary': {'id': 51, 'season_offset': -15},
        'Czech Republic': {'id': 52, 'season_offset': -15},
        'Latvia': {'id': 53, 'season_offset': -15},
        'Indonesia': {'id': 54, 'season_offset': -15},
        'Philippines': {'id': 55, 'season_offset': -15},
        'Estonia': {'id': 56, 'season_offset': -15},
        'Serbia': {'id': 57, 'season_offset': -15},
        'Croatia': {'id': 58, 'season_offset': -15},
        'Hong Kong': {'id': 59, 'season_offset': -16},
        'Chinese Taipei': {'id': 60, 'season_offset': -16},
        'Wales': {'id': 61, 'season_offset': -16},
        'Bulgaria': {'id': 62, 'season_offset': -16},
        'Israel': {'id': 63, 'season_offset': -16},
        'Slovenia': {'id': 64, 'season_offset': -16},
        'Lithuania': {'id': 66, 'season_offset': -18},
        'Slovakia': {'id': 67, 'season_offset': -18},
        'Ukraine': {'id': 68, 'season_offset': -18},
        'Bosnia and Herzegovina': {'id': 69, 'season_offset': -18},
        'Vietnam': {'id': 70, 'season_offset': -18},
        'Pakistan': {'id': 71, 'season_offset': -18},
        'Paraguay': {'id': 72, 'season_offset': -20},
        'Ecuador': {'id': 73, 'season_offset': -20},
        'Bolivia': {'id': 74, 'season_offset': -20},
        'Nigeria': {'id': 75, 'season_offset': -20},
        'Faroe Islands': {'id': 76, 'season_offset': -20},
        'Morocco': {'id': 77, 'season_offset': -20},
        'Saudi Arabia': {'id': 79, 'season_offset': -21},
        'Tunisia': {'id': 80, 'season_offset': -21},
        'Costa Rica': {'id': 81, 'season_offset': -21},
        'United Arab Emirates': {'id': 83, 'season_offset': -21},
        'Luxembourg': {'id': 84, 'season_offset': -21},
        'Iran': {'id': 85, 'season_offset': -21},
        'Dominican Republic': {'id': 88, 'season_offset': -21},
        'Cyprus': {'id': 89, 'season_offset': -21},
        'Belarus': {'id': 91, 'season_offset': -22},
        'Northern Ireland': {'id': 93, 'season_offset': -22},
        'Jamaica': {'id': 94, 'season_offset': -22},
        'Kenya': {'id': 95, 'season_offset': -22},
        'Panama': {'id': 96, 'season_offset': -22},
        'North Macedonia': {'id': 97, 'season_offset': -22},
        'Albania': {'id': 98, 'season_offset': -23},
        'Honduras': {'id': 99, 'season_offset': -23},
        'El Salvador': {'id': 100, 'season_offset': -23},
        'Malta': {'id': 101, 'season_offset': -23},
        'Kyrgyz Republic': {'id': 102, 'season_offset': -23},
        'Moldova': {'id': 103, 'season_offset': -23},
        'Georgia': {'id': 104, 'season_offset': -24},
        'Andorra': {'id': 105, 'season_offset': -24},
        'Jordan': {'id': 106, 'season_offset': -24},
        'Guatemala': {'id': 107, 'season_offset': -24},
        'Trinidad & Tobago': {'id': 110, 'season_offset': -25},
        'Nicaragua': {'id': 111, 'season_offset': -25},
        'Kazakhstan': {'id': 112, 'season_offset': -25},
        'Suriname': {'id': 113, 'season_offset': -25},
        'Liechtenstein': {'id': 117, 'season_offset': -26},
        'Algeria': {'id': 118, 'season_offset': -26},
        'Mongolia': {'id': 119, 'season_offset': -26},
        'Lebanon': {'id': 120, 'season_offset': -26},
        'Senegal': {'id': 121, 'season_offset': -26},
        'Armenia': {'id': 122, 'season_offset': -26},
        'Bahrain': {'id': 123, 'season_offset': -27},
        'Barbados': {'id': 124, 'season_offset': -27},
        'Cape Verde': {'id': 125, 'season_offset': -27},
        'Côte d’Ivoire': {'id': 126, 'season_offset': -27},
        'Kuwait': {'id': 127, 'season_offset': -28},
        'Iraq': {'id': 128, 'season_offset': -28},
        'Azerbaijan': {'id': 129, 'season_offset': -28},
        'Angola': {'id': 130, 'season_offset': -29},
        'Montenegro': {'id': 131, 'season_offset': -29},
        'Bangladesh': {'id': 132, 'season_offset': -29},
        'Yemen': {'id': 133, 'season_offset': -30},
        'Oman': {'id': 134, 'season_offset': -30},
        'Mozambique': {'id': 135, 'season_offset': -32},
        'Brunei': {'id': 136, 'season_offset': -32},
        'Ghana': {'id': 137, 'season_offset': -32},
        'Cambodia': {'id': 138, 'season_offset': -32},
        'Benin': {'id': 139, 'season_offset': -33},
        'Syria': {'id': 140, 'season_offset': -33},
        'Qatar': {'id': 141, 'season_offset': -34},
        'Tanzania': {'id': 142, 'season_offset': -34},
        'Uganda': {'id': 143, 'season_offset': -35},
        'Maldives': {'id': 144, 'season_offset': -35},
        'Uzbekistan': {'id': 145, 'season_offset': -44},
        'Cameroon': {'id': 146, 'season_offset': -44},
        'Cuba': {'id': 147, 'season_offset': -44},
        'Palestine': {'id': 148, 'season_offset': -44},
        'São Tomé e Príncipe': {'id': 149, 'season_offset': -69},
        'Comoros': {'id': 151, 'season_offset': -69},
        'Sri Lanka': {'id': 152, 'season_offset': -69},
        'Curaçao': {'id': 153, 'season_offset': -69},
        'Guam': {'id': 154, 'season_offset': -69},
        'Democratic Republic of the Congo': {'id': 155, 'season_offset': -72},
        'Federal Democratic Republic of Ethiopia': {'id': 156,
                                                    'season_offset': -72},
        'Saint Vincent and the Grenadines': {'id': 157, 'season_offset': -74},
        'Belize': {'id': 158, 'season_offset': -74},
        'Madagascar': {'id': 159, 'season_offset': -74},
        'Botswana': {'id': 160, 'season_offset': -74},
        'Hattrick International': {'id': 1000, 'season_offset': -63}
    }

    def __init__(self,
                 season=None, week=None, weekday=None,
                 year=None, month=None, day=None,
                 hour=0, minute=0, second=0,
                 datetime=None,
                 league=None,
                 timezone=None,
                 ):
        """
        Initialization of a HTDatetime instance

        :param season: Hattrick season (from season 1)
        :param week: Hattrick week in season (from 1 to 16)
        :param weekday: weekday in Hattrick week (from 1 to 7)
        :param year: calendar year (from 1997)
        :param month: calendar month (from 1 to 12)
        :param day: calendar day in month (from 1 to 31)
        :param hour: hour in day (from 0 to 23)
        :param minute: minute in hour (from 0 to 59)
        :param second: second in minute (from 0 to 59)
        :param datetime: date and time (from 1997-09-22 00:00)
        :param league: league for which HTDatetime is given
        :param timezone: timezone to use to localize HTDatetime
        :type season: int
        :type week: int
        :type weekday: int
        :type year: int
        :type month: int
        :type day: int
        :type hour: int
        :type minute: int
        :type second: int
        :type datetime: datetime.datetime
        :type league: Union[int, str]
        :type timezone: str
        """
        # Get season offset according to league, defaults to 0
        season_offset = self._get_season_offset(self._to_league_name(league))

        # Define self._league according to league, defaults to ""
        self._league = self._to_league_name(league)

        # Define timezone
        # if timezone is defined, get from it
        # elif datetime is defined and aware, get timezone from it
        # else set timezone to "CET"
        if timezone is not None:
            self._timezone = pytz.timezone(timezone)
        elif datetime is not None and datetime.tzinfo is not None:
            self._timezone = datetime.tzinfo
        else:
            self._timezone = pytz.timezone("CET")

        self.timezone_name = self._timezone.zone

        # If no argument is set, HTDate initialized with current date and time
        if all(i is None for i in (season, week, weekday,
                                   year, month, day, datetime)):
            self._datetime = dt.datetime.now(tz=self._timezone)
            self._year = self._datetime.year
            self._month = self._datetime.month
            self._day = self._datetime.day
            self._hour = self._datetime.hour
            self._minute = self._datetime.minute
            self._second = self._datetime.second
            self._season, self._week, self._weekday = (
                self._to_ht_calendar(self._year, self._month,
                                     self._day, self._timezone))
            self._season += season_offset

        # If season, week and weekday are set,
        # calculate year, month and day
        elif any((season, week, weekday)):

            if not all(isinstance(i, int) for i in (season, week, weekday)):
                raise ValueError(
                    "ht_season, ht_week and ht_weekday must be integers")
            elif (season < 1
                  or not (1 <= week <= 16)
                  or not (1 <= weekday <= 7)):
                raise ValueError(
                    "wrong value for ht_season, ht_week or ht_weekday")

            self._season = season
            self._week = week
            self._weekday = weekday
            self._year, self._month, self._day = (
                self._to_calendar(season - season_offset,
                                  week, weekday, self._timezone))
            self._hour = hour
            self._minute = minute
            self._second = second
            self._datetime = self._timezone.localize(
                dt.datetime(year=self._year,
                            month=self._month,
                            day=self._day,
                            hour=self._hour,
                            minute=self._minute,
                            second=self._second,
                            )
            )

        # If year, month and day are set,
        # calculate season, week and weekday
        elif any((year, month, day)):

            if not all(isinstance(i, int) for i in (year, month, day)):
                raise ValueError(
                    f"year, month and day must be integers :\n"
                    f"year : {year.__class__.__name__} was given\n"
                    f"month : {month.__class__.__name__} was given\n"
                    f"day : {day.__class__.__name__} was given"
                )
            elif year < 1997 or not (1 <= month <= 12) or not (1 <= day <= 31):
                raise ValueError(f"wrong value for year, month or day : "
                                 f"year : {year} "
                                 f"(must be equal or greater than 1997), "
                                 f"month : {month} "
                                 f"(must be between 1 and 12), "
                                 f"day : {day} "
                                 f"(must be between 1 and 31)."
                                 )

            self._season, self._week, self._weekday = (
                self._to_ht_calendar(year, month, day, self._timezone))
            self._season += season_offset
            self._year = year
            self._month = month
            self._day = day
            self._hour = hour
            self._minute = minute
            self._second = second
            self._datetime = self._timezone.localize(
                dt.datetime(self._year,
                            self._month,
                            self._day,
                            self._hour,
                            self._minute,
                            self._second,
                            ),
            )

        elif datetime is not None:

            if not isinstance(datetime, dt.datetime):
                raise ValueError("datetime must be a datetime instance")
            elif datetime.replace(tzinfo=None) < self._ORIGIN_DATE:
                raise ValueError("datetime must be after the 1997-09-22")

            # set datetime to the given one
            # if the given datetime is aware, set it directly or convert it to
            #   the given timezone
            # else, if it is naive, localize it according to the given timezone
            if datetime.tzinfo is not None:
                self._datetime = (datetime
                                  if timezone is None
                                  else datetime.astimezone(self._timezone))
            else:
                self._datetime = self._timezone.localize(datetime)

            self._season, self._week, self._weekday = (
                self._to_ht_calendar(datetime.year,
                                     datetime.month,
                                     datetime.day,
                                     self._timezone,
                                     )
            )
            self._season += season_offset
            self._year = self._datetime.year
            self._month = self._datetime.month
            self._day = self._datetime.day
            self._hour = self._datetime.hour
            self._minute = self._datetime.minute
            self._second = self._datetime.second

    def _to_calendar(self, season, week, weekday, timezone):
        delta_days = weekday - 1
        delta_weeks = ((season - 1) * 16) + (week - 1)
        date = (timezone.localize(self._ORIGIN_DATE)
                + dt.timedelta(days=delta_days, weeks=delta_weeks))
        year = date.year
        month = date.month
        day = date.day
        return year, month, day

    def _to_ht_calendar(self, year, month, day, timezone):
        datetime = timezone.localize(dt.datetime(year=year, month=month,
                                                 day=day))
        delta = datetime - timezone.localize(self._ORIGIN_DATE)
        ht_season = ((delta.days // 7) // 16) + 1
        ht_week = ((delta.days // 7) % 16) + 1
        ht_weekday = datetime.isoweekday()
        return ht_season, ht_week, ht_weekday

    def _get_season_offset(self, league_name):
        if not isinstance(league_name, str):
            raise ValueError("league_name must be an string")
        else:
            return self._LEAGUES_MAP.get(league_name, {}) \
                .get("season_offset", 0)

    def _to_league_name(self, league):

        if (not isinstance(league, int)
                and not isinstance(league, str)
                and league is not None):
            raise ValueError("league must be an integer, a string or None")

        if isinstance(league, int):
            t_list = [k for k, v in self._LEAGUES_MAP.items()
                      if v.get("id", None) == league
                      ]
            return t_list[0] if len(t_list) else ""

        elif isinstance(league, str):
            return league if league in self._LEAGUES_MAP else ""

        elif league is None:
            return ""

    @classmethod
    def from_ht_calendar(cls, season, week, weekday,
                         hour=0, minute=0, second=0,
                         **kwargs,
                         ):
        return cls(season=season, week=week, weekday=weekday,
                   hour=hour, minute=minute, second=second,
                   **kwargs)

    @classmethod
    def from_calendar(cls, year, month, day,
                      hour=0, minute=0, second=0,
                      **kwargs):
        return cls(year=year, month=month, day=day,
                   hour=hour, minute=minute, second=second,
                   **kwargs)

    @classmethod
    def from_datetime(cls, datetime, **kwargs):
        return cls(datetime=datetime, **kwargs)

    @property
    def season(self):
        return self._season

    @season.setter
    def season(self, value):
        self.__init__(season=value, week=self.week, weekday=self.weekday,
                      hour=self.hour, minute=self.minute, second=self.second,
                      league=self.league, timezone=self.timezone_name)

    @property
    def week(self):
        return self._week

    @week.setter
    def week(self, value):
        self.__init__(season=self.season, week=value, weekday=self.weekday,
                      hour=self.hour, minute=self.minute, second=self.second,
                      league=self.league, timezone=self.timezone_name)

    @property
    def weekday(self):
        return self._weekday

    @weekday.setter
    def weekday(self, value):
        self.__init__(season=self.season, week=self.week, weekday=value,
                      hour=self.hour, minute=self.minute, second=self.second,
                      league=self.league, timezone=self.timezone_name)

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self.__init__(year=value, month=self.month, day=self.day,
                      hour=self.hour, minute=self.minute, second=self.second,
                      league=self.league, timezone=self.timezone_name)

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value):
        self.__init__(year=self.year, month=value, day=self.day,
                      hour=self.hour, minute=self.minute, second=self.second,
                      league=self.league, timezone=self.timezone_name)

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):
        self.__init__(year=self.year, month=self.month, day=value,
                      hour=self.hour, minute=self.minute, second=self.second,
                      league=self.league, timezone=self.timezone_name)

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, value):
        self.__init__(year=self.year, month=self.month, day=self.day,
                      hour=value, minute=self.minute, second=self.second,
                      league=self.league, timezone=self.timezone_name)

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, value):
        self.__init__(year=self.year, month=self.month, day=self.day,
                      hour=self.hour, minute=value, second=self.second,
                      league=self.league, timezone=self.timezone_name)

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, value):
        self.__init__(year=self.year, month=self.month, day=self.day,
                      hour=self.hour, minute=self.minute, second=value,
                      league=self.league, timezone=self.timezone_name)

    @property
    def datetime(self):
        return self._datetime

    @datetime.setter
    def datetime(self, value):
        self.__init__(datetime=value,
                      league=self.league, timezone=self.timezone_name)

    @property
    def league(self):
        return self._league

    @league.setter
    def league(self, value):
        """
        season is modified according league change
        """
        new_league = self._to_league_name(value)
        old_league = self._to_league_name(self._league)

        new_offset = self._get_season_offset(new_league)
        old_offset = self._get_season_offset(old_league)

        self._season = self._season + (new_offset - old_offset)
        self._league = new_league

    @property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        tz = pytz.timezone(value)
        self.__init__(datetime=self.datetime.astimezone(tz),
                      league=self.league)

    def __add__(self, other):

        if isinstance(other, dt.timedelta):
            new_dt = self._datetime + other
            return HTDatetime(year=new_dt.year,
                              month=new_dt.month,
                              day=new_dt.day,
                              hour=new_dt.hour,
                              minute=new_dt.minute,
                              league=self.league,
                              )

        else:
            raise TypeError(
                f"unsupported operand type(s) for +: "
                f"'{self.__class__.__name__}' "
                f"and '{other.__class__.__name__}'"
            )

    def __sub__(self, other):

        if isinstance(other, HTDatetime):
            return self._datetime - other._datetime
        elif isinstance(other, dt.timedelta):
            return self.__add__(-other)
        else:
            raise TypeError(
                f"unsupported operand type(s) for -: "
                f"'{self.__class__.__name__}' "
                f"and '{other.__class__.__name__}'"
            )

    def __lt__(self, other):
        if isinstance(other, dt.datetime):
            return self._datetime < other
        elif isinstance(other, HTDatetime):
            return self._datetime < other._datetime

    def __le__(self, other):
        if isinstance(other, dt.datetime):
            return self._datetime <= other
        elif isinstance(other, HTDatetime):
            return self._datetime <= other._datetime

    def __gt__(self, other):
        if isinstance(other, dt.datetime):
            return self._datetime > other
        elif isinstance(other, HTDatetime):
            return self._datetime > other._datetime

    def __ge__(self, other):
        if isinstance(other, dt.datetime):
            return self._datetime >= other
        elif isinstance(other, HTDatetime):
            return self._datetime >= other._datetime

    def __eq__(self, other):
        if isinstance(other, dt.datetime):
            return self._datetime == other
        elif isinstance(other, HTDatetime):
            return self._datetime == other._datetime
        else:
            return False

    def __repr__(self):
        return f'<HTDatetime object : ' \
               f'{self._datetime.strftime("%Y-%m-%d %H:%M:%S %Z%z")} ' \
               f'(S{self._season}, W{self._week}, D{self._weekday})>'
