def test_translations(mocked_chpp):

    tr = mocked_chpp.xml_translations(language_id=5)

    assert tr.id == 5
    assert tr.name == 'Français'

    assert tr.texts.skill_names[4].type == 'Winger'
    assert tr.texts.skill_names[4].type_name == 'Ailier'
    assert tr.texts.skill_levels[0].value == 0
    assert tr.texts.skill_levels[0].value_name == 'inexistant'
    assert tr.texts.skill_sub_levels[1].value == 0.25
    assert tr.texts.skill_sub_levels[1].value_name == 'bas'
    assert tr.texts.player_specialties.label == 'Spécialité\xa0'
    assert tr.texts.player_specialties.list[2].value == 2
    assert tr.texts.player_specialties.list[2].label == 'Rapide'
    assert tr.texts.player_agreeability.list[-1].value == 5
    assert tr.texts.player_agreeability.list[-1].label == 'type adulé par ses coéquipiers'
    assert tr.texts.player_agressiveness.list[3].value == 3
    assert tr.texts.player_agressiveness.list[3].label == 'caractériel'
    assert tr.texts.player_honesty.list[4].value == 4
    assert tr.texts.player_honesty.list[4].label == 'intègre'
    assert tr.texts.tactic_types.list[7].value == 7
    assert tr.texts.tactic_types.list[7].label == 'Jeu créatif'
    assert tr.texts.match_positions.list[0].type == 'Keeper'
    assert tr.texts.match_positions.list[0].label == 'Gardien'
    assert tr.texts.rating_sectors.list[1].type == 'RightDefense'
    assert tr.texts.rating_sectors.list[1].label == 'Déf. latérale droite '
    assert tr.texts.team_attitude.list[2].value == 1
    assert tr.texts.team_attitude.list[2].label == 'Match le plus important'
    assert tr.texts.team_spirit.list[3].value == 3
    assert tr.texts.team_spirit.list[3].label == 'irrité'
    assert tr.texts.confidence.list[4].value == 4
    assert tr.texts.confidence.list[4].label == 'convenable'
    assert tr.texts.training_types.list[5].value == 5
    assert tr.texts.training_types.list[5].label == 'Ailier'
    assert tr.texts.sponsors.list[6].value == 6
    assert tr.texts.sponsors.list[6].label == 'délirants de joie'
    assert tr.texts.fan_mood.list[7].value == 7
    assert tr.texts.fan_mood.list[7].label == 'heureux'
    assert tr.texts.fan_match_expectations.list[8].value == 8
    assert tr.texts.fan_match_expectations.list[8].label == 'On va gagner'
    assert tr.texts.fan_season_expectations.list[0].value == 0
    assert tr.texts.fan_season_expectations.list[0].label == ('On n’a pas le niveau dans '
                                                              'cette division.')
    assert tr.texts.league_names[1].id == 2
    assert tr.texts.league_names[1].local_name == 'England'
    assert tr.texts.league_names[1].language_name == 'Angleterre'
