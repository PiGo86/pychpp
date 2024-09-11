from pychpp.models.custom import CustomModel
from pychpp.models.xml.league_details import LeagueDetails

class HTLeagueUnit(LeagueDetails, CustomModel):
    """
    Hattrick League Level Unit
    """

    URL_PATH = '/World/Series/'