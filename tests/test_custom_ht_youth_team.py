import re

from pychpp.models.custom.ht_youth_team import HTYouthTeam, HTYouthTeamPlayerItem
from pychpp.models.xml.youth_player_list import YouthPlayerListListPlayerItem

from .fixtures import chpp, YOUTH_PLAYER_PATTERN


def test_get_own_team_youth_player(chpp):

    youth_team = chpp.youth_team()
    assert isinstance(youth_team, HTYouthTeam)

    if youth_team.id != 0:
        light_youth_player = youth_team.players()[0]

        assert isinstance(light_youth_player, HTYouthTeamPlayerItem)

        youth_player = light_youth_player.details()

        for i in ("keeper", "defender", "playmaker", "winger", "scorer", "passing", "set_pieces"):
            assert getattr(youth_player.skills, i, None) is not None

        youth_player_match = re.match(YOUTH_PLAYER_PATTERN, youth_player.url)
        assert youth_player_match is not None
        assert int(youth_player_match.group(1)) == youth_player.id
