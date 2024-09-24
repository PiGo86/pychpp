from datetime import datetime
from typing import Optional, List

from pychpp.models.custom import CustomModel
from pychpp.models.custom.base.ht_match import HTCommonLightMatch
from pychpp.models.custom.base.ht_team import HTCommonLightTeam
from pychpp.models.ht_field import HTProxyField, HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.xml import matches_archive as ma


class HTMatchesArchive(ma.RequestMatchesArchive, CustomModel):
    """
    Hattrick Matches Archive
    """

    URL_PATH = '/Club/Matches/Archive.aspx'

    team: 'HTMATeam' = HTProxyField(ma.MatchesArchive)
    first_match_date: Optional[datetime] = HTProxyField(ma.MatchesArchive)
    last_match_date: Optional[datetime] = HTProxyField(ma.MatchesArchive)
    matches: List['HTMAItem'] = HTProxyField(ma.MatchesArchive)

    def __getitem__(self, item):
        return self.matches[item]

    def __len__(self):
        return len(self.matches)


class HTMATeam(HTCommonLightTeam, ma.Team):
    """
    Hattrick Matches Archive -> Team
    """


class HTMAItem(HTCommonLightMatch, ma.MatchItem):
    """
    Hattrick Matches Archive -> Match item
    """

    URL_PATH = '/Club/Matches/Match.aspx'

    _r_id: int = HTInitVar('matchID', fill_with='id')

    id: int = HTProxyField(ma.MatchItem)
    date: datetime = HTProxyField(ma.MatchItem)
    type_id: int = HTProxyField(ma.MatchItem)
    context_id: int = HTProxyField(ma.MatchItem)
    source_system: str = HTProxyField(ma.MatchItem)
    rule_id: int = HTProxyField(ma.MatchItem)
    cup: 'ma.MatchItemCup' = HTProxyField(ma.MatchItem)
    home_goals: int = HTProxyField(ma.MatchItem)
    away_goals: int = HTProxyField(ma.MatchItem)

    home_team: 'HTMAItemTeam' = HTField('HomeTeam',
                                        xml_prefix='Home',
                                        suppl_attrs={'source_system': 'source_system'})
    away_team: 'HTMAItemTeam' = HTField('AwayTeam',
                                        xml_prefix='Away',
                                        suppl_attrs={'source_system': 'source_system'})


class HTMAItemTeam(HTCommonLightTeam, ma.MatchItemTeam):
    """
    Hattrick Matches Archive -> Match item -> Home/Away team
    """
