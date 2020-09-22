from pychpp import ht_model, ht_xml
from pychpp import ht_team, ht_region


class HTArena(ht_model.HTModel):
    """
    Hattrick arena
    """

    _SOURCE_FILE = "arenadetails"
    _SOURCE_FILE_VERSION = "1.5"

    _URL_PATH = "/Club/Arena/?ArenaID="

    _ht_attributes = [
        ("ht_id", "Arena/ArenaID", ht_xml.HTXml.ht_int),
        # General information
        ("name", "Arena/ArenaName", ht_xml.HTXml.ht_str),
        # Team
        ("team_ht_id", "Arena/Team/TeamID", ht_xml.HTXml.ht_int),
        ("team_name", "Arena/Team/TeamName", ht_xml.HTXml.ht_str),
        # Country
        ("country_ht_id", "Arena/League/LeagueID", ht_xml.HTXml.ht_int),
        ("country_name", "Arena/League/LeagueName", ht_xml.HTXml.ht_str),
        # Region
        ("region_ht_id", "Arena/Region/RegionID", ht_xml.HTXml.ht_int),
        ("region_name", "Arena/Region/RegionName", ht_xml.HTXml.ht_str),
        # Current capacity
        ("current_capacity", "Arena/CurrentCapacity",
         ht_xml.HTXml.ht_arena_capacity),
        # Expanded capacity
        ("expanded_capacity", "Arena/ExpandedCapacity",
         ht_xml.HTXml.ht_arena_capacity),
    ]

    def __init__(self, ht_id=None, **kwargs):
        """
        Initialization of a HTArena instance

        :param ht_id: Hattrick ID of arena
        :type ht_id: int
        :key chpp: CHPP instance of connected user
        :type chpp: chpp.CHPP
        """
        self._REQUEST_ARGS = dict()
        self._REQUEST_ARGS["arenaID"] = ht_id if ht_id is not None else ""
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__} object : " \
               f"{self.name} ({self.ht_id})>"

    @property
    def team(self):
        return ht_team.HTTeam(chpp=self._chpp,
                              ht_id=self.team_ht_id)

    @property
    def region(self):
        return ht_region.HTRegion(chpp=self._chpp,
                                  ht_id=self.region_ht_id)
