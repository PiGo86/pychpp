"""High-level custom model built on top of the xml models."""

from pychpp.models.custom.base.ht_match import BaseHTMatch
from pychpp.models.custom.base.ht_team import HTCommonLightTeam
from pychpp.models.ht_field import HTField
from pychpp.models.xml.match_details import (RequestMatchDetails, Match, MatchHomeTeam,
                                             MatchAwayTeam)


class HTMatch(BaseHTMatch, RequestMatchDetails, Match):
    """Hattrick match.

    Attributes:
        id: Hattrick ID of the match.
        type: Type of the match.
        date: Date of the match.
        home_team: Home team of the match.
        away_team: Away team of the match.
        arena: Arena where the match is played.
        source_system: Source system of the match ('senior', 'youth', ...).
        goals: Goals of the match.
        events: Events of the match.

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
    """Hattrick Match -> Team."""


class HTMatchHomeTeam(HTMatchTeam, MatchHomeTeam):
    """Home team of a match."""
    pass


class HTMatchAwayTeam(HTMatchTeam, MatchAwayTeam):
    """Away team of a match."""
    pass
