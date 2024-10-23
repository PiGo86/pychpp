from pychpp.fixtures.ht_datetime import HTDatetime


def test_xml_live(mocked_chpp):

    live = mocked_chpp.xml_live(include_starting_lineup=True, use_live_events_and_texts=True)

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
