from pychpp.fixtures.ht_datetime import HTDatetime


def test_tournament_list(mocked_chpp):

    tl = mocked_chpp.xml_tournament_list(1758305)

    tournament = tl.tournaments[0]
    assert tournament.id == 5292015
    assert tournament.name == 'Coupe des Hauts de France et du reste du monde'
    assert tournament.type == 3
    assert tournament.season == 20
    assert tournament.logo_url == ('http://res.hattrick.org/tournamentlogo/53/530/5293/5292015'
                                   '/5292015.png')
    assert tournament.trophy_type == 1
    assert tournament.number_of_teams == 12
    assert tournament.number_of_groups == 2
    assert tournament.last_match_round == 5
    assert tournament.first_match_round_date == HTDatetime.from_calendar(2024, 9, 23, 18)
    assert tournament.next_match_round_date == HTDatetime.from_calendar(2024, 10, 28, 18)
    assert tournament.is_matches_ongoing is False
    assert tournament.creator.id == 4123541
    assert tournament.creator.login_name == 'tigersspp'
