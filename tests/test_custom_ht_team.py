import re

from pychpp.models.custom.ht_team import HTTeam
from pychpp.models.custom.ht_user import HTUser
from pychpp.models.custom.ht_youth_team import HTYouthTeam
from pychpp.models.custom.ht_arena import HTArena

from .fixtures import TEAM_PATTERN, USER_PATTERN, YOUTH_TEAM_PATTERN, ARENA_PATTERN,mocked_chpp


def test_get_secondary_team(mocked_chpp):
    team = mocked_chpp.team(id_=1755350)

    assert isinstance(team, HTTeam)
    assert team.id == 1755350
    assert team.name == "Projet NUL Bot Breton"
    assert team.short_name == 'Bot Breton'
    assert team.is_primary_club is False

    team_match = re.match(TEAM_PATTERN, team.url)
    assert team_match is not None
    assert int(team_match.group(1)) == 1755350

    user = team.user.details()
    assert isinstance(user, HTUser)
    assert user.id == 9638716
    assert user.username == "Conteur_Merlin"

    user_match = re.match(USER_PATTERN, user.url)
    assert user_match is not None
    assert int(user_match.group(1)) == 9638716

    youth_team = team.youth_team.details()
    assert isinstance(youth_team, HTYouthTeam)
    assert youth_team.id == 2745926
    assert youth_team.name == "Les Petits Pédëstres"

    youth_team_match = re.match(YOUTH_TEAM_PATTERN, youth_team.url)
    assert youth_team_match is not None
    assert int(youth_team_match.group(1)) == 2745926

    arena = team.arena.details()
    assert isinstance(arena, HTArena)
    assert arena.name == "Stade Laurent Fièvre"

    arena_match = re.match(ARENA_PATTERN, arena.url)
    assert arena_match is not None
    assert int(arena_match.group(1)) == 1751912
