import re

from pychpp.models.custom.ht_arena import HTArena
from pychpp.models.custom.ht_team import HTTeam

from .conftest import ARENA_PATTERN, TEAM_PATTERN


def test_get_current_user_arena(chpp):
    arena = chpp.arena()
    assert isinstance(arena, HTArena)
    assert isinstance(arena.id, int) or arena.id is None
    assert isinstance(arena.name, str)
    assert isinstance(arena.url, str)
    arena_match = re.match(ARENA_PATTERN, arena.url)
    assert arena_match is not None
    assert int(arena_match.group(1)) == arena.id


def test_get_specific_arena(mocked_chpp):
    arena = mocked_chpp.arena(295023)
    assert isinstance(arena, HTArena)
    assert arena.id == 295023
    assert arena.name == 'Le Piquant'

    arena_match = re.match(ARENA_PATTERN, arena.url)
    assert arena_match is not None
    assert int(arena_match.group(1)) == 295023

    team = arena.team.details()
    assert isinstance(team, HTTeam)
    assert team.id == 295023
    assert team.name == 'Les piments verts'

    team_match = re.match(TEAM_PATTERN, team.url)
    assert team_match is not None
    assert int(team_match.group(1)) == 295023
