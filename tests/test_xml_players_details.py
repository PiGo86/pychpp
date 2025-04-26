from pychpp.models.xml.player_details import PlayerDetails, PlayerSkills


def test_get_player(mocked_chpp):
    player = mocked_chpp.xml_player_details(player_id=432002549)

    assert isinstance(player, PlayerDetails)
    assert isinstance(player.skills, PlayerSkills)
    assert player.owner_notes is None

    assert player.id == 432002549
    assert player.agreeability == 2
    assert player.aggressiveness == 3
    assert player.honesty == 3

    for i in ("stamina", "keeper", "defender", "playmaker", "winger",
              "scorer", "passing", "set_pieces"):
        assert getattr(player.skills, i) is None or isinstance(getattr(player.skills, i), int)

    assert player.tsi == 230
    assert player.injury_level == -1


def test_get_player_on_transfer_list_without_bidder(mocked_chpp):
    player = mocked_chpp.xml_player_details(player_id=473582922)

    assert isinstance(player, PlayerDetails)
    assert player.transfer_details.bidder_team.id is None
    assert player.transfer_details.bidder_team.name is None
