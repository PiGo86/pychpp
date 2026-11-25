"""Tests for the `nationalprospectplayers.xml` CHPP file parsing."""

from pychpp.models.xml.national_prospect_players import NationalProspectPlayers


def test_national_prospect_players_version_1_0(mocked_chpp):
    npp = mocked_chpp.xml_national_prospect_players(team_id=3001, version='1.0')

    assert isinstance(npp, NationalProspectPlayers)
    assert npp.user_supporter_tier == 'none'
    assert npp.team_id == 3001
    assert npp.team_name == 'England'
    assert len(npp.players) == 226

    player = npp.players[0]
    assert player.id == 462575853
    assert player.name == 'Abdul-Hamid Mujtaba'
    assert player.category_id == 4
    assert player.specialty == 5
    assert player.avatar.background_image == '/Img/Avatar/backgrounds/card1.png'
    assert len(player.avatar.layers) == 7
    assert player.avatar.layers[0].x == 9
    assert player.avatar.layers[0].y == 10
    assert player.avatar.layers[0].image == '/Img/Avatar/backgrounds/bg_blue.png'
