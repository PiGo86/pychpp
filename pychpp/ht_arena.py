from pychpp import ht_team
from pychpp.ht_date import HTDate


class HTArena:
    """
    Hattrick arena
    """

    _SOURCE_FILE = "arenadetails"
    _SOURCE_FILE_VERSION = "1.5"

    def __init__(self, chpp, ht_id=None):
        """
        Initialization of a HTArena instance

        :param chpp: CHPP instance of connected user
        :param ht_id: Hattrick ID of arena
        :type chpp: CHPP
        :type ht_id: int
        """
        self._chpp = chpp
        kwargs = {}

        if ht_id is not None:
            kwargs["arenaID"] = ht_id

        data = chpp.request(file=self._SOURCE_FILE,
                            version=self._SOURCE_FILE_VERSION,
                            **kwargs,
                            ).find("Arena")

        self._data = data

        self.ht_id = int(data.find("ArenaID").text)
        self.name = data.find("ArenaName").text

        cap_data = data.find("CurrentCapacity")
        rebuilt_date = (HTDate.from_ht(cap_data.find("RebuiltDate").text)
                        if cap_data.find("RebuiltDate").attrib["Available"] == "True"
                        else None
                        )

        self.capacity = {"rebuilt_date": rebuilt_date,
                         "terraces": int(cap_data.find("Terraces").text),
                         "basic": int(cap_data.find("Basic").text),
                         "roof": int(cap_data.find("Roof").text),
                         "vip": int(cap_data.find("VIP").text),
                         "total": int(cap_data.find("Total").text),
                         }

        exp_data = data.find("ExpandedCapacity")

        if exp_data.attrib["Available"] == "True":
            self.expanded_capacity = {"expansion_date": HTDate.from_ht(exp_data.find("ExpansionDate").text),
                                      "terraces": int(exp_data.find("Terraces").text),
                                      "basic": int(exp_data.find("Basic").text),
                                      "roof": int(exp_data.find("Roof").text),
                                      "vip": int(exp_data.find("VIP").text),
                                      "total": int(exp_data.find("Total").text),
                                      }
        else:
            self.expanded_capacity = None

    def __repr__(self):
        return f"<{self.__class__.__name__} object : {self.name} ({self.ht_id})>"

    @property
    def team(self):
        return ht_team.HTTeam(chpp=self._chpp,
                              ht_id=int(self._data.find("Team").find("TeamID").text))
