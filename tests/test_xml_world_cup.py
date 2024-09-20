from pychpp.models.xml.world_cup import WorldCupViewGroups, ViewGroupsRoundItem, WorldCupViewMatches, \
    ViewGroupsTeamItem, ViewMatchesMatchItem, ViewMatchesRoundItem

from .fixtures import mocked_chpp

def test_get_world_cup_rounds(mocked_chpp):
    wc_groups = mocked_chpp.xml_world_cup(action_type='viewGroups', season=76)

    assert isinstance(wc_groups, WorldCupViewGroups)
    assert wc_groups.cup_id == 137
    assert wc_groups.season == 76

    assert isinstance(wc_groups.scores[0], ViewGroupsTeamItem)

    assert len(wc_groups.rounds) == 6
    assert isinstance(wc_groups.rounds[0], ViewGroupsRoundItem)


def test_get_world_cup_matches(mocked_chpp):
    wc_matches = mocked_chpp.xml_world_cup(action_type='viewMatches',
                                           season=76,
                                           cup_series_unit_id=1697,
                                           )

    assert isinstance(wc_matches, WorldCupViewMatches)
    assert wc_matches.cup_id == 137
    assert wc_matches.season == 76
    assert wc_matches.cup_series_unit_id == 1697
    assert wc_matches.match_round == 0

    assert len(wc_matches.matches) == 6
    assert isinstance(wc_matches.matches[0], ViewMatchesMatchItem)
    assert wc_matches.matches[0].home_team.id == 3002
    assert wc_matches.matches[0].home_team.name == "Deutschland"
    assert wc_matches.matches[0].id == 669657311

    assert len(wc_matches.rounds) == 6
    assert isinstance(wc_matches.rounds[0], ViewMatchesRoundItem)
