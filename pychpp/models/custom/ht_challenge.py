"""High-level custom model built on top of the xml models."""

from typing import Any, List, Optional, Tuple, Iterable, TYPE_CHECKING, Dict

from pychpp.models.custom import CustomModel
from pychpp.models.custom.ht_team import HTTeam
from pychpp.models.ht_field import HTProxyField
from pychpp.models.xml.challenges import (ChallengeItem, ChallengesView, CommonRequestChallenges,
                                          ChallengesChallengeable)

if TYPE_CHECKING:
    from pychpp.chpp import CHPP


class HTChallengeManager:
    """Managing challenges on Hattrick."""

    def __init__(self, chpp: 'CHPP', team_id: Optional[int] = None,
                 is_weekend_friendly: Optional[bool] = None, **kwargs: Any):
        self._chpp = chpp
        self.team_id = team_id
        self.is_weekend_friendly = is_weekend_friendly
        self.kwargs = kwargs

    def pending_challenges(
            self, author: str = 'both',
    ) -> List[ChallengeItem] | Tuple[List[ChallengeItem], List[ChallengeItem]]:
        """Get the pending challenges of the team.

        Args:
            author: Whose challenges to return: 'own_team', 'other_teams' or 'both'.

        Returns:
            The pending challenges (or a tuple of both lists if author='both').

        """
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
            self,
            teams: Optional[Iterable['HTTeam']] = None,
            team_ids: Optional[Iterable[int]] = None,
    ) -> Dict[int, bool]:
        """Check if teams are challengeable.

        Args:
            teams: Teams to check (HTTeam objects).
            team_ids: Or team IDs to check.

        Returns:
            A dict mapping each team ID to its challengeable status.

        """
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

    def challenge(self, opponent_team_id: int, match_type: Optional[int] = None,
                  match_place: Optional[int] = None, arena_id: Optional[int] = None) -> None:
        """Challenge an opponent team.

        Args:
            opponent_team_id: Hattrick ID of the opponent team.
            match_type: Type of the match.
            match_place: Place of the match.
            arena_id: ID of a neutral arena.

        """
        self._chpp.xml_challenges(
            action_type='challenge', opponent_team_id=opponent_team_id,
            match_type=match_type, match_place=match_place,
            arena_id=arena_id, **self.kwargs,
        )

    def accept(self, training_match_ht_id) -> None:
        """Accept a challenge.

        Args:
            training_match_ht_id: Hattrick ID of the training match to accept.

        """
        self._chpp.xml_challenges(action_type='accept',
                                  training_match_id=training_match_ht_id, **self.kwargs)

    def decline(self, training_match_ht_id) -> None:
        """Decline a challenge.

        Args:
            training_match_ht_id: Hattrick ID of the training match to decline.

        """
        self._chpp.xml_challenges(action_type='decline',
                                  training_match_id=training_match_ht_id, **self.kwargs)

    def withdraw(self, training_match_ht_id) -> None:
        """Withdraw a challenge.

        Args:
            training_match_ht_id: Hattrick ID of the training match to withdraw.

        """
        self._chpp.xml_challenges(action_type='withdraw',
                                  training_match_id=training_match_ht_id, **self.kwargs)


class HTChallenges(CustomModel, CommonRequestChallenges):
    """Challenges of a team."""
    challenges_by_me: List['ChallengeItem'] = HTProxyField(ChallengesView)
    offers_by_others: List['ChallengeItem'] = HTProxyField(ChallengesView)
