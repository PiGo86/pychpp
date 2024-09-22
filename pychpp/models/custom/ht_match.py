from pychpp.models.custom.base.ht_match import BaseHTMatch
from pychpp.models.custom.base.ht_team import HTCommonLightTeam
from pychpp.models.ht_field import HTField
from pychpp.models.xml.match_details import (RequestMatchDetails, Match, MatchHomeTeam,
                                             MatchAwayTeam)


class HTMatch(BaseHTMatch, RequestMatchDetails, Match):
    """
    Hattrick Match
    """
    URL_PATH = '/Club/Matches/Match.aspx'
    XML_PREFIX = 'Match/'

    source_system: str = HTField('../SourceSystem')

    home_team: 'HTMatchHomeTeam' = HTField('.',
                                           xml_prefix='HomeTeam/',
                                           suppl_attrs={'source_system': 'source_system'},
                                           )
    away_team: 'HTMatchAwayTeam' = HTField('.',
                                           xml_prefix='AwayTeam/',
                                           suppl_attrs={'source_system': 'source_system'},
                                           )


class HTMatchTeam(HTCommonLightTeam):
    """
    Hattrick Match -> Team
    """


class HTMatchHomeTeam(HTMatchTeam, MatchHomeTeam):
    pass


class HTMatchAwayTeam(HTMatchTeam, MatchAwayTeam):
    pass
