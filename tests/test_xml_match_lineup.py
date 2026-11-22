from pychpp.models.xml.match_lineup import MatchLineup


def test_match_lineup_version_2_2(mocked_chpp):

    ml = mocked_chpp.xml_match_lineup(match_id=773342689, team_id=649632)

    assert isinstance(ml, MatchLineup)
    assert ml.match_id == 773342689
    assert ml.source_system == 'Hattrick'
    assert ml.match_type == 1
    assert ml.match_context_id == 431
    assert ml.home_team.id == 1244048
    assert ml.home_team.name == 'TV Vahrendorf'
    assert ml.away_team.id == 649632
    assert ml.away_team.name == 'Undertaker United FC'
    assert ml.arena.id == 1240610
    assert ml.arena.name == 'Spielwiese Vahrendorf'

    team = ml.team
    assert team.id == 649632
    assert team.name == 'Undertaker United FC'
    assert team.experience_level == 11
    assert team.style_of_play == -10

    assert len(team.starting_lineup) == 12
    player = team.starting_lineup[0]
    assert player.id == 465876519
    assert player.role_id == 100
    assert player.first_name == 'Oday'
    assert player.last_name == 'Abou Saada'
    assert player.nick_name is None
    assert player.behaviour == 0

    assert len(team.substitutions) == 8

    # since version 2.2, a behaviour change without substitution has OrderType 4
    behaviour_change = team.substitutions[0]
    assert behaviour_change.team_id == 649632
    assert behaviour_change.subject_player_id == 465048555
    assert behaviour_change.object_player_id == 465048555
    assert behaviour_change.order_type == 4
    assert behaviour_change.new_position_id == 108
    assert behaviour_change.new_position_behaviour == 0
    assert behaviour_change.minute == 34
    assert behaviour_change.match_part == 1

    substitution = team.substitutions[3]
    assert substitution.subject_player_id == 465048555
    assert substitution.object_player_id == 464907615
    assert substitution.order_type == 1
    assert substitution.new_position_id == 108
    assert substitution.new_position_behaviour == 1
    assert substitution.minute == 46
    assert substitution.match_part == 2

    assert len(team.lineup) == 19
    lineup_player = team.lineup[0]
    assert lineup_player.id == 465876519
    assert lineup_player.role_id == 100
    assert lineup_player.first_name == 'Oday'
    assert lineup_player.last_name == 'Abou Saada'
    assert lineup_player.rating_stars == 10.5
    assert lineup_player.rating_stars_end_of_match == 8.0
    assert lineup_player.behaviour == 0
