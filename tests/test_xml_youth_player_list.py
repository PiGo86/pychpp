from pychpp.models.xml.youth_player_list import YouthPlayerListList, YouthPlayerListDetails


def test_youth_player_list_version_1_4(mocked_chpp):

    ypl = mocked_chpp.xml_youth_player_list(version='1.4')
    assert isinstance(ypl, YouthPlayerListList)
    assert len(ypl.list) == 14
    assert ypl.list[0].id == 301741224
    assert ypl.list[0].first_name == 'Brieuc'
    assert ypl.list[0].last_name == 'Rousselet'
    assert ypl.list[0].gender_id == 1

    ypd = mocked_chpp.xml_youth_player_list(action_type='details', version='1.4')
    assert isinstance(ypd, YouthPlayerListDetails)
    assert len(ypd.list) == 14
    player = ypd.list[0]
    assert player.id == 301741224
    assert player.gender_id == 1
    assert player.owning_youth_team.id == 2942691
    assert player.owning_youth_team.name == 'Les Petits Chapelains'
    assert player.owning_youth_team.league_id == 225490
    assert player.owning_youth_team.user_id == 1728698
    assert player.owning_youth_team.senior_team.id == 1165592
    assert player.skills is not None
