from pychpp.fixtures.ht_datetime import HTDatetime


def test_supporters(mocked_chpp):

    supp = mocked_chpp.xml_supporters(user_id=13481763)

    assert supp.total_supported_teams == 22

    team = supp.supported_teams[0]
    assert team.user_id == 9228073
    assert team.login_name == 'Monsieur-le-Vicomte'
    assert team.team_name == 'Montauban'
    assert team.league_id == 5
    assert team.league_name == 'France'
    assert team.league_level_unit_id == 36621
    assert team.league_level_unit_name == 'VI.633'

    last_m = team.last_match
    assert last_m.id == 739340262
    assert last_m.date == HTDatetime.from_calendar(2024, 10, 26, 21)
    assert last_m.home_team_id == 1752284
    assert last_m.home_team_name == 'as pays neslois'
    assert last_m.away_team_id == 292987
    assert last_m.away_team_name == 'Montauban'
    assert last_m.home_goals == 1
    assert last_m.away_goals == 7

    next_m = team.next_match
    assert next_m.id == 741971334
    assert next_m.date == HTDatetime.from_calendar(2024, 10, 30, 15, 45)
    assert next_m.home_team_id == 292987
    assert next_m.home_team_name == 'FC Veno'
    assert next_m.away_team_id == 292987
    assert next_m.away_team_name == 'Montauban'

    pa = team.press_announcement
    assert pa.send_date == HTDatetime.from_calendar(2022, 4, 5, 11, 59)
    assert pa.subject == 'Brice Mokemo est parti'
    assert pa.body == ("Hier, Brice Mokemo [playerid=424110937 ]a signé dans un club de DIII "
                       "hollandaise. Tous nos supporteurs sont en pleurs de te voir partir Brice. "
                       "Tu étais la star du club, notre  numéro 10 légendaire. Tu étais arrivé "
                       "à Montauban encore tout jeunot, déjà bien tapé en construction/passe "
                       "et on t'a entrainer en ailier pour, pour... devenir notre 1er (et seul "
                       "à ce jour) joueur entrainé à devenir international. On était pas peu fier."
                       " Et puis international pas qu'un peu, 25 sélections avec la NT de la "
                       "Côte d'Ivoire. S'il vous plait.\n"
                       "Festus Savimba ton fidèle DL camerounais entame une grève de la faim "
                       "pour implorer ton retour. Brice, tu nous tapais régulièrement du 12 "
                       "en notes de match, tu étais rayonnant sur ton aile. \n"
                       "Et puis un jour, Brice, tu est devenu vieux. Pas encore trop, tu "
                       "aurais pu nous faire une dernière belle saison mais, d'un commun accord, "
                       "avant que ta valeur marchande ne s'effondre, tu as été ok pour un "
                       "dernier challenge sportif. Bonne suite de carrière Brice ... snif !!!")
