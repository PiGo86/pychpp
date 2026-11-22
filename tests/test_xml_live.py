from pychpp.fixtures.ht_datetime import HTDatetime


def test_xml_live(mocked_chpp):

    live = mocked_chpp.xml_live(include_starting_lineup=True, use_live_events_and_texts=True,
                                version='2.3')

    match = live.matches[0]
    assert match.source_system == 'Hattrick'
    assert match.id == 741937041
    assert match.type == 9
    assert match.date == HTDatetime.from_calendar(2024, 10, 23, 20, 50, 0)

    ht = match.home_team
    assert ht.id == 2151226
    assert ht.name == 'F.C. Jotes Marrakech'
    assert ht.short_name == 'Marrakech'
    assert ht.starting_lineup[2].id == 467576196
    assert ht.starting_lineup[2].role_id == 104
    assert ht.starting_lineup[2].name == 'Valentin Chernomazov'
    assert ht.starting_lineup[2].behaviour == 0

    at = match.away_team
    assert at.id == 238555
    assert at.name == 'Gaborussia Dortmund'
    assert at.short_name == 'Gaborussia'
    assert at.starting_lineup[0].id == 473565884
    assert at.starting_lineup[0].role_id == 100
    assert at.starting_lineup[0].name == 'Eugenio Ienco'
    assert at.starting_lineup[0].behaviour == 0

    subst = match.substitutions[0]
    assert subst.team_id == 238555
    assert subst.subject_player_id == 473565884
    assert subst.object_player_id == 484617223
    assert subst.order_type == 1
    assert subst.new_position_id == 100
    assert subst.new_position_behaviour == 0
    assert subst.match_minute == 43

    event = match.events[1]
    assert event.index == 6
    assert event.minute == 6
    assert event.subject_player_id == 0
    assert event.subject_team_id == 238555
    assert event.object_player_id == 1040402
    assert event.key == '481_2'
    assert event.match_part == 1
    assert event.text[0:21] == "Comme vous le savez, "
    assert match.home_goals == 2
    assert match.away_goals == 2
    assert match.last_shown_event_index == 70
    assert match.next_event_minute == 53
    assert match.next_event_match_part == 2


def test_xml_live_version_2_4(mocked_chpp):

    live = mocked_chpp.xml_live(match_id=773342689, include_starting_lineup=True,
                                use_live_events_and_texts=True)

    match = live.matches[0]
    assert match.source_system == 'Hattrick'
    assert match.id == 773342689
    assert match.type == 1
    assert match.date == HTDatetime.from_calendar(2026, 11, 21, 18, 0, 0)

    ht = match.home_team
    assert ht.id == 1244048
    assert ht.name == 'TV Vahrendorf'
    assert ht.short_name == 'Vahrendorf'
    assert ht.starting_lineup[0].id == 461685865
    assert ht.starting_lineup[0].role_id == 100
    assert ht.starting_lineup[0].name == 'Tiziano Marchiol'
    assert ht.starting_lineup[0].behaviour == 0

    at = match.away_team
    assert at.id == 649632
    assert at.name == 'Undertaker United FC'
    assert at.short_name == 'U-U-FC'
    assert at.starting_lineup[0].id == 465876519
    assert at.starting_lineup[0].role_id == 100
    assert at.starting_lineup[0].name == 'Oday Abou Saada'
    assert at.starting_lineup[0].behaviour == 0
    assert at.starting_lineup[1].name == 'Marc Rönn'
    assert at.starting_lineup[1].behaviour == 3

    # since version 2.4, a behaviour change without substitution has OrderType 4
    behaviour_change = match.substitutions[0]
    assert behaviour_change.team_id == 649632
    assert behaviour_change.subject_player_id == 465048555
    assert behaviour_change.object_player_id == 465048555
    assert behaviour_change.order_type == 4
    assert behaviour_change.new_position_id == 108
    assert behaviour_change.new_position_behaviour == 0
    assert behaviour_change.match_minute == 34
    assert behaviour_change.match_part is None

    substitution = match.substitutions[3]
    assert substitution.team_id == 649632
    assert substitution.subject_player_id == 465048555
    assert substitution.object_player_id == 464907615
    assert substitution.order_type == 1
    assert substitution.new_position_id == 108
    assert substitution.new_position_behaviour == 1
    assert substitution.match_minute == 46

    event = match.events[0]
    assert event.index == 0
    assert event.minute == -2
    assert event.match_part == 0
    assert event.subject_team_id == 70000
    assert event.subject_player_id == 1240610
    assert event.object_player_id == 66935
    assert event.key == '32_3'

    event = match.events[5]
    assert event.index == 5
    assert event.minute == 0
    assert event.match_part == 0
    assert event.subject_player_id == 0
    assert event.subject_team_id == 0
    assert event.object_player_id == 0
    assert event.key == '598_3'
    assert event.text[0:5] == "C'est"

    assert match.home_goals == 1
    assert match.away_goals == 0
    assert match.last_shown_event_index == 18
    assert match.next_event_minute == 46
    assert match.next_event_match_part == 2
