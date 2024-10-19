from pychpp.fixtures.ht_datetime import HTDatetime


def test_get_alliance_details(mocked_chpp):

    alliance_xml = mocked_chpp.xml_alliance_details(action_type='view', alliance_id=118840)

    assert alliance_xml.user_supporter_tier == 'none'
    assert alliance_xml.action_type == 'view'

    alliance = alliance_xml.alliance
    assert alliance.id == 118840
    assert alliance.name == 'Ligue Mondiale des Ambitieux'
    assert alliance.abbreviation == 'LMA'
    assert alliance.description == (
        "La Ligue Mondiale des Ambitieux regroupe des managers "
        "qui veulent gravir les échelons et gagner des trophées.\n\n"
        "L'ambiance est conviviale, respectueuse de chacun.\n\n"
        "L'échange et le partage sont de mise afin d'apprendre de chacun.\n\n"
        "Chaque saison nous organisons une coupe au format unique offrant au final "
        "4 coupes pour que tout le monde s'amuse.\n\n"
        "Cette fédération se veut être un espace d'échange apaisé et accueille "
        "des débutants et des membres du Championnat 😃\n\n"
        "Vous pouvez postuler si vous êtes un gentil ambitieux "
        "qui souhaite discuter et échanger.😉\n\n"
        "A noter que nous n'acceptons pas chaque demande mais filtrons les adhérents "
        "afin de garantir l'ambiance de notre communauté.\n\n"
        "Sebleger."
    )
    assert alliance.logo_url == ('https://res.hattrick.org/federationlogo/2/12/119/118840/'
                                 '118840.png')
    assert alliance.top_role == 'Fondateur'
    assert alliance.top_user_id == 12375275
    assert alliance.top_login_name == 'Sebleger'
    assert alliance.creation_date == HTDatetime.from_calendar(2021, 10, 10, 19, 4, 21)
    assert alliance.home_page_url == 'https://www.youtube.com/c/HattrickGuideduDébutant'
    assert alliance.number_of_members == 240

    languages = alliance.languages
    assert languages[0].id == 5
    assert languages[0].name == 'Français'
