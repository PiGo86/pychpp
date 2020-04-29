from pychpp import ht_model, ht_xml


class HTRegion(ht_model.HTModel):
    """
    Hattrick region
    """

    _SOURCE_FILE = "regiondetails"
    _SOURCE_FILE_VERSION = "1.2"
    _REQUEST_ARGS = dict()

    _HT_ATTRIBUTES = [("ht_id", "League/Region/RegionID", ht_xml.HTXml.ht_int,),
                      ("name", "League/Region/RegionName", ht_xml.HTXml.ht_str,),
                      ("number_of_users", "League/Region/NumberOfUsers", ht_xml.HTXml.ht_int,),
                      ("number_of_online", "League/Region/NumberOfOnline", ht_xml.HTXml.ht_int,),
                      ("weather", "League/Region/WeatherID", ht_xml.HTXml.ht_int,),
                      ("tomorrow_weather", "League/Region/TomorrowWeatherID", ht_xml.HTXml.ht_int,),

                      ]

    def __init__(self, ht_id=None, **kwargs):
        """
        Initialize HTRegion instance

        :param chpp: CHPP instance of connected user
        :param ht_id: arena Hattrick ID (if none, fetch the primary club arena of connected user), defaults to None
        :type chpp: CHPP
        :type ht_id: int, optional
        """
        if ht_id is not None:
            self._REQUEST_ARGS["regionID"] = ht_id

        super().__init__(**kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__} object : {self.name} ({self.ht_id})>"
