from pychpp import ht_model, ht_xml
from pychpp import ht_team


class HTUser(ht_model.HTModel):
    """
    Hattrick user
    """

    _SOURCE_FILE = "managercompendium"
    _SOURCE_FILE_VERSION = "1.2"

    _URL_PATH = "/Club/Manager/?userId="

    _ht_attributes = [("ht_id", "Manager/UserId",
                       ht_xml.HTXml.ht_int,),
                      ("username", "Manager/Loginname",
                       ht_xml.HTXml.ht_str,),
                      ("supporter_tier", "Manager/SupporterTier",
                       ht_xml.HTXml.ht_str,),
                      ("last_logins", "Manager/LastLogins",
                       ht_xml.HTXml.ht_last_logins,),
                      ("language_id", "Manager/LanguageId",
                       ht_xml.HTXml.ht_int,),
                      ("language_name", "Manager/LanguageName",
                       ht_xml.HTXml.ht_str,),
                      ("country_id", "Manager/CountryId",
                       ht_xml.HTXml.ht_int,),
                      ("country_name", "Manager/CountryName",
                       ht_xml.HTXml.ht_str,),
                      ("_teams_ht_id", "Manager/Teams",
                       ht_xml.HTXml.ht_teams_ht_id,),

                      ]

    def __init__(self, ht_id=None, **kwargs):
        """
        Initialize HTUser instance

        :param ht_id: user Hattrick ID (if none, fetch the connected user),
                      defaults to None
        :key chpp: CHPP instance of connected user
        :type ht_id: int, optional
        :type chpp: CHPP
        """
        self._REQUEST_ARGS = dict()

        if ht_id is not None:
            self._REQUEST_ARGS["userId"] = ht_id

        super().__init__(**kwargs)

    def __repr__(self):
        return f"<HTUser object : {self.username} ({self.ht_id})>"

    @property
    def teams(self):
        """Teams list of current user"""
        return [ht_team.HTTeam(chpp=self._chpp, ht_id=team_ht_id)
                for team_ht_id in self._teams_ht_id]
