import datetime

from pychpp import ht_model
from pychpp import ht_xml
from pychpp import ht_match


class HTMatchesArchive(ht_model.HTModel):
    """
    Hattrick matches archive
    """

    _SOURCE_FILE = "matchesarchive"
    _SOURCE_FILE_VERSION = "1.4"

    _HT_ATTRIBUTES = [("team_id", "Team/TeamID", ht_xml.HTXml.ht_int),
                      ("team_name", "Team/TeamName", ht_xml.HTXml.ht_str),
                      ("first_match_date", "Team/FirstMatchDate", ht_xml.HTXml.ht_date_from_text),
                      ("last_match_date", "Team/LastMatchDate", ht_xml.HTXml.ht_date_from_text),
                      ("_matches_id_list", "Team/MatchList", ht_xml.HTXml.ht_match_list),
                      ]

    def __init__(self, ht_id=None, youth=False, first_match_date=None,
                 last_match_date=None, season=None, hto=False, **kwargs):
        super().__init__(**kwargs)

        if not isinstance(ht_id, int) and ht_id is not None:
            raise ValueError("ht_id must be None or an integer")
        elif not isinstance(youth, bool):
            raise ValueError("youth must be a boolean")
        elif not isinstance(first_match_date, datetime.datetime) and first_match_date is not None:
            raise ValueError("first_match_date must be a datetime instance")
        elif not isinstance(last_match_date, datetime.datetime) and last_match_date is not None:
            raise ValueError("last_match_date must be a datetime instance")
        elif not isinstance(season, int) and season is not None:
            raise ValueError("season must be a integer")
        elif not isinstance(hto, bool):
            raise ValueError("hto must be a boolean")

        self._REQUEST_ARGS["teamID"] = str(ht_id) if ht_id is not None else ""
        self._REQUEST_ARGS["isYouth"] = "true" if youth is True else "false"
        self._REQUEST_ARGS["FirstMatchDate"] = (ht_xml.HTXml.ht_date_to_text(first_match_date)
                                                if first_match_date is not None else "")
        self._REQUEST_ARGS["LastMatchDate"] = (ht_xml.HTXml.ht_date_to_text(last_match_date)
                                               if last_match_date is not None else "")
        self._REQUEST_ARGS["season"] = str(season) if season is not None else ""
        self._REQUEST_ARGS["HTO"] = "true" if hto is True else "false"

    def search(self):
        return [ht_match.HTMatch(chpp=self._chpp, ht_id=m_id) for m_id in self._matches_id_list]
