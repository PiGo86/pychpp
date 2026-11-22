from pychpp.fixtures.ht_datetime import HTDatetime
from pychpp.models.xml.player_details import PlayerDetails, PlayerSkills


def test_get_player(mocked_chpp):
    player = mocked_chpp.xml_player_details(player_id=432002549, version='3.0')

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
    player = mocked_chpp.xml_player_details(player_id=473582922, version='3.0')

    assert isinstance(player, PlayerDetails)
    assert player.transfer_details.bidder_team.id is None
    assert player.transfer_details.bidder_team.name is None


def test_get_player_version_3_3(mocked_chpp):
    player = mocked_chpp.xml_player_details(player_id=432002549, version='3.3')

    assert isinstance(player, PlayerDetails)

    assert player.id == 432002549
    assert player.gender_id == 1
    assert player.assists_current_team == 0
    assert player.career_assists == 4

    # skills not shown for a player not owned -> no transfer estimate
    assert player.transfer_compare_average is None
    assert player.transfer_compare_average_date is None

    # FamilyRelation container present but empty (no known relation)
    assert player.family_relation is not None
    assert player.family_relation.related_player_id is None
    assert player.family_relation.related_player_source_id is None
    assert player.family_relation.related_player_name is None
    assert player.family_relation.relationship_type_id is None

    assert len(player.trophies) == 11
    trophy = player.trophies[0]
    assert trophy.trophy_type_id == 17
    assert trophy.team_id == 924535
    assert trophy.team_name == "FC Ausgefall Verléierer"
    assert trophy.trophy_season == 66
    assert trophy.league_level == 4
    assert trophy.league_level_unit_id == 115334
    assert trophy.league_level_unit_name == "IV.31"
    assert trophy.gained_date == HTDatetime.from_calendar(2024, 5, 20, 12, 5)


def test_get_own_player_version_3_3(mocked_chpp):
    player = mocked_chpp.xml_player_details(player_id=430759322, version='3.3')

    assert isinstance(player, PlayerDetails)

    assert player.id == 430759322
    assert player.gender_id == 1
    assert player.assists_current_team == 1
    assert player.career_assists == 1

    # own player -> skills shown -> transfer estimate available
    assert player.transfer_compare_average == 1911121
    assert player.transfer_compare_average_date == HTDatetime.from_calendar(2023, 2, 20, 12, 15)

    # TrophyList present but empty (club without Gold supporter)
    assert player.trophies == []
    assert player.family_relation is not None
    assert player.family_relation.related_player_id is None
