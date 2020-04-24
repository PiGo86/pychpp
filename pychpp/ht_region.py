class HTRegion:
    """
    Hattrick region
    """

    _SOURCE_FILE = "regiondetails"
    _SOURCE_FILE_VERSION = "1.2"

    def __init__(self, chpp, ht_id=None):
        """
        Initialize HTRegion instance

        :param chpp: CHPP instance of connected user
        :param ht_id: arena Hattrick ID (if none, fetch the primary club arena of connected user), defaults to None
        :type chpp: CHPP
        :type ht_id: int, optional
        """
        self._chpp = chpp
        kwargs = {}

        if ht_id is not None:
            kwargs["regionID"] = ht_id

        data = chpp.request(file=self._SOURCE_FILE,
                            version=self._SOURCE_FILE_VERSION,
                            **kwargs,
                            ).find("League")

        region_data = data.find("Region")

        self._data = data

        self.ht_id = int(region_data.find("RegionID").text)
        self.name = region_data.find("RegionName").text
        self.number_of_users = int(region_data.find("NumberOfUsers").text)
        self.number_of_online = int(region_data.find("NumberOfOnline").text)
        self.weather = int(region_data.find("WeatherID").text)
        self.tomorrow_weather = int(region_data.find("TomorrowWeatherID").text)

    def __repr__(self):
        return f"<{self.__class__.__name__} object : {self.name} ({self.ht_id})>"
