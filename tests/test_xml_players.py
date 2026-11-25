"""Tests for the `players.xml` CHPP file parsing."""

from pychpp.models.xml.players import PlayersView, PlayersViewOldies


def test_players_version_2_8(mocked_chpp):
    players = mocked_chpp.xml_players(team_id=1165592, version='2.8')

    assert isinstance(players, PlayersView)

    assert players.team.id == 1165592
    assert players.team.name == "Les Poitevins de La Chapelle"
    assert len(players.team.players) == 27

    player = players.team.players[0]
    assert player.id == 430759322
    assert player.first_name == "Frédérik"
    assert player.last_name == "Rivière"
    assert player.gender_id == 1
    assert player.assists_current_team == 1
    assert player.career_assists == 1


def test_players_view_oldies_version_2_8(mocked_chpp):
    players = mocked_chpp.xml_players(action_type='viewOldies', team_id=1165592,
                                      version='2.8')

    assert isinstance(players, PlayersViewOldies)

    assert players.team.id == 1165592
    assert len(players.team.players) == 1

    player = players.team.players[0]
    assert player.id == 430759337
    assert player.first_name == "Bastien"
    assert player.last_name == "Collot"
    assert player.gender_id == 1
    assert player.assists_current_team == 0
    assert player.career_assists == 0
