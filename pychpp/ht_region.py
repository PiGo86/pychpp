from pychpp import ht_model, ht_xml


class HTRegion(ht_model.HTModel):
    """
    Hattrick region
    """

    _SOURCE_FILE = "regiondetails"
    _SOURCE_FILE_VERSION = "1.2"

    _URL_PATH = "/World/Regions/Region.aspx?RegionID="

    _ht_attributes = [("ht_id", "League/Region/RegionID",
                       ht_xml.HTXml.ht_int,),
                      ("name", "League/Region/RegionName",
                       ht_xml.HTXml.ht_str,),
                      ("number_of_users", "League/Region/NumberOfUsers",
                       ht_xml.HTXml.ht_int,),
                      ("number_of_online", "League/Region/NumberOfOnline",
                       ht_xml.HTXml.ht_int,),
                      ("weather", "League/Region/WeatherID",
                       ht_xml.HTXml.ht_int,),
                      ("tomorrow_weather", "League/Region/TomorrowWeatherID",
                       ht_xml.HTXml.ht_int,),

                      ]

    def __init__(self, ht_id=None, **kwargs):
        """
        Initialize HTRegion instance

        :param ht_id: arena Hattrick ID (if none,
                      fetch the primary club arena of connected user),
                      defaults to None
        :key chpp: CHPP instance of connected user
        :type ht_id: int, optional
        :type chpp: CHPP
        """
        self._REQUEST_ARGS = dict()

        if ht_id is not None:
            self._REQUEST_ARGS["regionID"] = ht_id

        super().__init__(**kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__} object : " \
               f"{self.name} ({self.ht_id})>"
