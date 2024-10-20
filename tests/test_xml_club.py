def test_xml_club(mocked_chpp):

    club = mocked_chpp.xml_club()

    assert club.team.id == 1165592
    assert club.team.name == 'Les Poitevins de La Chapelle'

    staff = club.team.staff
    assert staff.assistant_trainer_levels == 10
    assert staff.financial_director_levels == 0
    assert staff.form_coach_levels == 0
    assert staff.medic_levels == 5
    assert staff.spokesperson_levels == 0
    assert staff.sport_psychologist_levels == 5
    assert staff.tactical_assistant_levels == 0

    youth_squad = club.team.youth_squad
    assert youth_squad.investment == 200_000
    assert youth_squad.has_promoted is False
    assert youth_squad.youth_level == 8
