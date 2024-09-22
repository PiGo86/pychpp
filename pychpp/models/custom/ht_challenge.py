from typing import List, Tuple, Union, Iterable, TYPE_CHECKING, Dict

from pychpp.models.custom import CustomModel
from pychpp.models.custom.ht_team import HTTeam
from pychpp.models.ht_field import HTProxyField
from pychpp.models.xml.challenges import (ChallengeItem, ChallengesView, CommonRequestChallenges,
                                          ChallengesChallengeable)

if TYPE_CHECKING:
    from pychpp.chpp import CHPP


class HTChallengeManager:
    """
    Managing challenges on Hattrick
    """

    def __init__(self, chpp: 'CHPP', team_id: int = None,
                 is_weekend_friendly: bool = None, **kwargs):
        self._chpp = chpp
        self.team_id = team_id
        self.is_weekend_friendly = is_weekend_friendly
        self.kwargs = kwargs

    def pending_challenges(
            self, author: str = 'both',
    ) -> Union[List[ChallengeItem], Tuple[List[ChallengeItem], List[ChallengeItem]]]:

        challenges = HTChallenges(self._chpp, action_type='view', team_id=self.team_id,
                                  is_week_friendly=self.is_weekend_friendly, **self.kwargs)

        if author == 'own_team':
            return challenges.challenges_by_me

        elif author == 'other_teams':
            return challenges.offers_by_others

        elif author == 'both':
            return challenges.challenges_by_me, challenges.offers_by_others

        else:
            raise ValueError("if set, author argument must be equal to "
                             "'own_team', 'other_teams', 'both'")

    def are_challengeable(
            self, teams: Iterable['HTTeam'] = None, team_ids: Iterable[int] = None,
    ) -> Dict[int, bool]:
        if teams is not None:
            result = ChallengesChallengeable(
                chpp=self._chpp, action_type='challengeable',
                suggested_team_ids=','.join(str(t.id) for t in teams)
            ).challengeable_result

        elif team_ids is not None:
            result = ChallengesChallengeable(
                chpp=self._chpp, action_type='challengeable',
                suggested_team_ids=','.join(str(id_) for id_ in team_ids)
            ).challengeable_result

        else:
            raise ValueError("one of 'teams' or 'team_ids' arguments have to be set")

        return {item.team_id: item.is_challengeable for item in result}

    def challenge(self, opponent_team_id: int, match_type: int = None,
                  match_place: int = None, arena_id: int = None) -> None:
        self._chpp.xml_challenges(
            action_type='challenge', opponent_team_id=opponent_team_id,
            match_type=match_type, match_place=match_place,
            arena_id=arena_id, **self.kwargs,
        )

    def accept(self, training_match_ht_id) -> None:
        self._chpp.xml_challenges(action_type='accept',
                                  training_match_id=training_match_ht_id, **self.kwargs)

    def decline(self, training_match_ht_id) -> None:
        self._chpp.xml_challenges(action_type='decline',
                                  training_match_id=training_match_ht_id, **self.kwargs)

    def withdraw(self, training_match_ht_id) -> None:
        self._chpp.xml_challenges(action_type='withdraw',
                                  training_match_id=training_match_ht_id, **self.kwargs)


class HTChallenges(CustomModel, CommonRequestChallenges):
    challenges_by_me: List['ChallengeItem'] = HTProxyField(ChallengesView)
    offers_by_others: List['ChallengeItem'] = HTProxyField(ChallengesView)
