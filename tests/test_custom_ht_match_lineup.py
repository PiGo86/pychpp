import re

from pychpp.models.custom.ht_arena import HTArena
from pychpp.models.custom.ht_match import HTMatch
from pychpp.models.custom.ht_match_lineup import HTMatchLineup, HTMLEndingLineupPlayersItem, \
    HTMLStartingLineupPlayersItem, HTMLSubstitutionItem, HTMLLineupPlayersItem
from pychpp.models.custom.ht_player import HTPlayer

from .conftest import MATCH_LINEUP_PATTERN, PLAYER_PATTERN, YOUTH_PLAYER_PATTERN


def test_get_match_lineup(mocked_chpp):
    match_lineup = mocked_chpp.match_lineup(match_id=660688698, team_id=86324)

    assert isinstance(match_lineup, HTMatchLineup)
    assert isinstance(match_lineup.match.details(), HTMatch)

    assert match_lineup.match.id == 660688698
    assert match_lineup.home_team.name == "Gazela.f.c"
    assert match_lineup.away_team.id == 86324
    assert match_lineup.away_team.name == "Apanha Bolas FC"
    assert match_lineup.arena.id == 1420520
    assert match_lineup.match.type == 1

    ml_match = re.match(MATCH_LINEUP_PATTERN, match_lineup.url)
    assert ml_match is not None
    assert int(ml_match.group(1)) == 660688698

    assert isinstance(match_lineup.arena.details(), HTArena)

    # Ending lineup
    assert len(match_lineup.team_lineup.ending_lineup_players) == 20

    player_1 = match_lineup.team_lineup.ending_lineup_players[10]
    assert isinstance(player_1, HTMLEndingLineupPlayersItem)
    assert isinstance(player_1.details(), HTPlayer)
    assert player_1.id == 453276953
    assert player_1.first_name == "Urho"
    assert player_1.role_id == 113
    assert player_1.role_name == "LEFT_FORWARD"
    assert re.match(PLAYER_PATTERN, player_1.url)

    player_2 = match_lineup.team_lineup.ending_lineup_players[15]
    assert player_2.role_id == 120
    assert player_2.role_name == "SUBSTITUTION_EXTRA"

    assert re.match(PLAYER_PATTERN,
                    match_lineup.team_lineup.ending_lineup_players[15].url)

    # Starting lineup
    assert len(match_lineup.team_lineup.starting_lineup_players) == 13

    player_1 = match_lineup.team_lineup.starting_lineup_players[2]
    assert isinstance(player_1, HTMLStartingLineupPlayersItem)
    assert player_1.id == 453372830
    assert player_1.first_name == "Gaspar"
    assert player_1.role_id == 105
    assert player_1.role_name == "LEFT_BACK_DEFENDER"

    player_2 = match_lineup.team_lineup.starting_lineup_players[10]
    assert player_2.role_id == 113
    assert player_2.role_name == "LEFT_FORWARD"
    assert re.match(PLAYER_PATTERN, player_2.url)

    # Substitutions
    substitutions = match_lineup.team_lineup.substitutions
    assert len(substitutions) == 2
    sub = substitutions[1]
    assert isinstance(sub, HTMLSubstitutionItem)
    assert sub.team_id == 86324
    assert sub.subject_player_id == 453372834
    assert sub.object_player_id == 453372838
    assert sub.order_type == 1
    assert sub.new_position_id == 108
    assert sub.new_position_behaviour == 0
    assert sub.minute == 73
    assert sub.match_part == 2

    ml2 = mocked_chpp.match_lineup(match_id=685566813, team_id=1750803)

    assert ml2.match.id == 685566813
    assert ml2.home_team.name == "Capdenaguet"
    assert ml2.away_team.id == 1165592
    assert ml2.away_team.name == "Les Poitevins de La Chapelle"
    assert ml2.arena.id == 960796
    assert ml2.match.type == 5

    assert ml2.team_lineup.formations == [(0, "451"),
                                          (50, "442"),
                                          (50, "433"),
                                          (50, "523"),
                                          ]

    # specific case : injured player is not replaced
    ml3 = mocked_chpp.match_lineup(match_id=690094305, team_id=296272)

    assert ml3.team_lineup.formations == [(0, "433"),
                                          (63, "333"),
                                          ]

    ml4 = mocked_chpp.match_lineup(match_id=690183773, team_id=2053693)

    assert ml4.team_lineup.formations == [(0, "253"),
                                          (8, "153"),
                                          ]

    # test swap substitution
    ml5 = mocked_chpp.match_lineup(match_id=685860616, team_id=113143)

    assert ml5.team_lineup.formations == [(0, "352")]

    # other unreplaced player
    ml6 = mocked_chpp.match_lineup(match_id=690328642, team_id=773670)

    assert ml6.team_lineup.formations == [(0, "532"), (81, "432")]

    # goalkeeper replaced by field player
    ml7 = mocked_chpp.match_lineup(match_id=693127128, team_id=291394)

    assert ml7.team_lineup.formations == [(0, "352"),
                                          (77, "252"),
                                          (81, "152"),
                                          ]

    # substitute player become captain and is swapped
    ml8 = mocked_chpp.match_lineup(match_id=695301077, team_id=294798)

    assert ml8.team_lineup.formations == [(0, "343"),
                                          (75, "253"),
                                          ]


def test_get_youth_match_lineup(mocked_chpp):
    match_lineup = mocked_chpp.match_lineup(match_id=136016609,
                                            team_id=499165,
                                            source_system='Youth',
                                            )

    youth_player = match_lineup.team_lineup.ending_lineup_players[0]
    assert isinstance(youth_player, HTMLLineupPlayersItem)
    assert youth_player.id == 353745299
    assert youth_player.first_name == "Fritz"
    assert youth_player.last_name == "Unterbuchner"
    match_yp = re.match(YOUTH_PLAYER_PATTERN, youth_player.url)
    assert match_yp is not None
    assert int(match_yp.group(1)) == 353745299
