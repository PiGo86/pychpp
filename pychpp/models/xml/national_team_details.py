"""Models for the `nationalteamdetails.xml` CHPP file."""

from typing import List, Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestNationalTeamDetails(HTModel):
    """National Team Details - Request arguments."""
    SOURCE_FILE = 'nationalteamdetails'
    LAST_VERSION = '2.0'

    _r_team_id: int = HTInitVar('teamID', init_arg='team_id')


class NationalTeamDetails(RequestNationalTeamDetails):
    """National Team Details."""
    user_supporter_tier: str = HTField('UserSupporterTier')
    is_playing_match: bool = HTField('IsPlayingMatch')
    id: int = HTField('Team/TeamID')
    name: str = HTField('Team/TeamName')
    short_name: str = HTField('Team/ShortTeamName')
    national_coach: 'NationalCoach' = HTField('Team/NationalCoach')
    assistant_coach: Optional['AssistantCoach'] = HTField('Team/AssistantCoach', version='>=2.0')
    scouts: Optional[List['Scout']] = HTField('Team/Scouts', items='Scout', version='>=2.0')
    league: 'League' = HTField('Team/League')
    home_page: str = HTField('Team/HomePage')
    logo: str = HTField('Team/Logo')
    dress_uri: str = HTField('Team/DressURI')
    dress_alternate_uri: str = HTField('Team/DressAlternateURI')
    experience: 'Experience' = HTField('Team/.')
    morale: Optional[int] = HTField('Team/Morale')
    self_confidence: Optional[int] = HTField('Team/SelfConfidence')
    supporters_popularity: Optional[int] = HTField('Team/SupportersPopularity')
    rating_score: int = HTField('Team/RatingScore')
    fanclub_size: int = HTField('Team/FanClubSize')
    rank: int = HTField('Team/Rank')


class NationalCoach(HTModel):
    """National Team Details -> National Coach."""
    id: int = HTField('NationalCoachUserID')
    login_name: str = HTField('NationalCoachLoginname')


class AssistantCoach(HTModel):
    """National Team Details -> Assistant Coach (empty if the team has no assistant coach)."""
    id: Optional[int] = HTField('UserID')
    login_name: Optional[str] = HTField('Loginname')


class Scout(HTModel):
    """National Team Details -> Scouts -> Scout item."""
    id: Optional[int] = HTField('UserID')
    login_name: Optional[str] = HTField('Loginname')


class League(HTModel):
    """National Team Details -> League."""
    id: int = HTField('LeagueID')
    name: str = HTField('LeagueName')


class Experience(HTModel):
    """National Team Details -> Experience."""
    _433: int = HTField('Experience433')
    _451: int = HTField('Experience451')
    _352: int = HTField('Experience352')
    _532: int = HTField('Experience532')
    _343: int = HTField('Experience343')
    _541: int = HTField('Experience541')
    _523: int = HTField('Experience523')
    _550: int = HTField('Experience550')
    _253: int = HTField('Experience253')
    _442: int = HTField('Experience442')
