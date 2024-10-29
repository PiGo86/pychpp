# pyCHPP

pyCHPP is an object-oriented python framework created to use the API provided by the online game Hattrick (www.hattrick.org).

## Installation

pyCHPP can be installed using pip :

    pip install pychpp

## Quick start

### First connection
```python-repl
>>> from pychpp import CHPP
    
# Set consumer_key and consumer_secret provided for your app by Hattrick
>>> consumer_key = ''
>>> consumer_secret = ''
    
# Initialize CHPP instance
>>> chpp = CHPP(consumer_key, consumer_secret)
    
# Get url, request_token and request_token_secret to request API access
# You can set callback_url and scope
>>> auth = chpp.get_auth(callback_url="www.mycallbackurl.com", scope="")
  
# auth['url'] contains the url to which the user can grant the application
# access to the Hattrick API
# Once the user has entered their credentials,
# a code is returned by Hattrick (directly or to the given callback url)
>>> code = ""

# Get access token from Hattrick
# access_token['key'] and access_token['secret'] have to be stored
# in order to be used later by the app
>>> access_token = chpp.get_access_token(
                        request_token=auth["request_token"],
                        request_token_secret=auth["request_token_secret"],
                        code=code,
                        )
```
### Further connections
```python-repl
# Once you have obtained access_token for a user
# You can use it to call Hattrick API
>>> chpp = CHPP(consumer_key,
            consumer_secret,
            access_token['key'],
            access_token['secret'],
            )

# Now you can use chpp methods to get datas from Hattrick API
# For example :
>>> current_user = chpp.user()
>>> all_teams = current_user.teams

>>> best_team_ever = chpp.team(1165592)
>>> best_team_ever
<HTTeam object - Les Poitevins de La Chapelle (1165592)>

>>> best_team_arena = best_team_ever.arena.details()
>>> best_team_arena
<HTArena object - Stade de La Chapelle (1162154)>
>>> best_team_arena.name
'Stade de La Chapelle'

>>> worth_team_ever = chpp.team(1750803)
>>> worth_team_ever
<HTTeam object - Capdenaguet (1750803)>

>>> player = chpp.player(6993859)
>>> player
<HTPlayer object - Pedro Zurita (6993859)>
>>> player.career_goals
1167

>>> match = chpp.match(68599186)
>>> match
<HTMatch object - Skou United - FC Barentin (68599186)>
>>> match.date
<HTDatetime object - 2006-02-23 20:00:00 CET+0100 (S28, W8, D4)>
```

## Philosophy
From 0.4.0 version, pyCHPP is build on two class families :
- under `pychpp/models/xml`, you will find a class by CHPP XML file. These classes can be instantiated with a CHPP object, thanks to functions prefixed with `xml_`. For example, `arenadetails.xml` file can be fetched through a CHPP instance with the `xml_arena_details` method.
```python-repl
>>> xml_arena = chpp.xml_arena_details(arena_id=294762)
>>> xml_arena
<ArenaDetails object - Stade Dimitri Liénard (294762)>
```
- under `pychpp/models/custom`, pyCHPP moves further away from vanilla xml files, in order to offer a more consistent experience (in our opinion) and to add some convenient methods and attributes (as url), and to allow navigation between objects. For example, you can instantiate a HTTeam object through a CHPP instance by calling the `team` method. From this `HTTeam` instance, you can get the list of this team players by calling its `players` method.
```python-repl
>>> team = chpp.team(294762)
>>> team
<HTTeam object - FC Mistral Gagnant (294762)>
>>> players = team.players()
>>> players[3]
<HTTeamPlayersItem object - Massimiliano Carotta (453279129)>
>>> players[3].first_name
'Massimiliano'
>>> players[3].last_name
'Carotta'
```

## Customization

The easiest way to use pyCHPP is to use the builtin methods of the CHPP object.

However, for more advanced use, it is also possible to customize the framework's built-in templates.

For example, if you need to perform a query on the arenadetails.xml file, but in reality only need the Arena/ArenaID, Arena/ArenaName and Arena/ArenaImage data, one way to proceed is to create a custom class inheriting from the RequestArenaDetails class, and use HTProxyField as follows:
```python
from pychpp.models.xml.arena_details import RequestArenaDetailsDefault, ArenaDetailsDefault
from pychpp.models.ht_field import HTProxyField


class MyCustomArenaClass(RequestArenaDetailsDefault):
    id: int = HTProxyField(ArenaDetailsDefault)
    name: str = HTProxyField(ArenaDetailsDefault)
    image: str = HTProxyField(ArenaDetailsDefault)
```

Then, to use this new class:
```python-repl
>>> from pychpp.chpp import CHPPBase
>>> chpp = CHPPBase(consumer_key, 
                    consumer_secret,
                    access_token['key'],
                    access_token['secret'],
                    )
>>> arena = MyCustomArenaClass(chpp=chpp, arena_id=1747365)
>>> arena
<MyCustomArenaClass object - La grande taule (1747365)>
>>> arena.id
1747365
>>> arena.name
'La grande taule'
>>> arena.image
'//res.hattrick.org/arenas/18/175/1748/1747365/custom-220-100.jpg'
```
In this way, only the data you're really interested in is parsed, which can in some cases be interesting from a performance point of view.

## List of supported CHPP XML files
![57/57](https://progress-bar.xyz/100/?title=57%20on%2057)

The following table shows the CHPP XML files that are currently supported:

|      pyCHPP class      |        CHPP XML files        |
|:----------------------:|:----------------------------:|
|      Achievements      |      `achievements.xml`      |
|       Alliances        |       `alliances.xml`        |
|    AllianceDetails     |    `alliancedetails.xml`     |
|         Arena          |      `arenadetails.xml`      |
|        Avatars         |        `avatars.xml`         |
|       Bookmarks        |       `bookmarks.xml`        |
|       Challenges       |       `challenges.xml`       |
|          Club          |          `club.xml`          |
|       CupMatches       |       `cupmatches.xml`       |
|      CurrentBids       |      `currentbids.xml`       |
|        Economy         |        `economy.xml`         |
|          Fans          |          `fans.xml`          |
|   HallOfFamePlayers    |       `hofplayers.xml`       |
|     LadderDetails      |     `ladderdetails.xml`      |
|       LadderList       |       `ladderlist.xml`       |
|     LeagueDetails      |     `leaguedetails.xml`      |
|     LeagueFixtures     |     `leaguefixtures.xml`     |
|      LeagueLevels      |      `leaguelevels.xml`      |
|          Live          |          `live.xml`          |
|   ManagerCompendium    |   `managercompendium.xml`    |
|      MatchDetails      |      `matchdetails.xml`      |
|      MatchLineup       |      `matchlineup.xml`       |
|      MatchOrders       |      `matchorders.xml`       |
|     MatchesArchive     |     `matchesarchive.xml`     |
|        Matches         |        `matches.xml`         |
|  NationalTeamDetails   |  `nationalteamdetails.xml`   |
|  NationalTeamMatches   |  `nationalteammatches.xml`   |
|     NationalTeams      |     `nationalteams.xml`      |
|    NationalPlayers     |    `nationalplayers.xml`     |
|     PlayerDetails      |     `playerdetails.xml`      |
|      PlayerEvents      |      `playerevents.xml`      |
|        Players         |        `players.xml`         |
|     RegionDetails      |     `regiondetails.xml`      |
|         Search         |         `search.xml`         |
|      StaffAvatars      |      `staffavatars.xml`      |
|       StaffList        |       `stafflist.xml`        |
|       Supporters       |       `supporters.xml`       |
|      TeamDetails       |      `teamdetails.xml`       |
|   TournamentDetails    |   `tournamentdetails.xml`    |
|   TournamentFixtures   |   `tournamentfixtures.xml`   |
| TournamentLeagueTables | `tournamentleaguetables.xml` |
|     TournamentList     |     `tournamentlist.xml`     |
|        Training        |        `training.xml`        |
|     TrainingEvents     |     `trainingevents.xml`     |
|     TransferSearch     |     `transfersearch.xml`     |
|    TransfersPlayer     |    `transfersplayer.xml`     |
|     TransfersTeam      |     `transfersteam.xml`      |
|      Translations      |      `translations.xml`      |
|        WorldCup        |        `worldcup.xml`        |
|      WorldDetails      |      `worlddetails.xml`      |
|     WorldLanguages     |     `worldlanguages.xml`     |
|      YouthAvatars      |      `youthavatars.xml`      |
|   YouthLeagueDetails   |   `youthleaguedetails.xml`   |
|  YouthLeagueFixtures   |  `youthleaguefixtures.xml`   |
|   YouthPlayerDetails   |   `youthplayerdetails.xml`   |
|    YouthPlayerList     |    `youthplayerlist.xml`     |
|    YouthTeamDetails    |    `youthteamdetails.xml`    |

## License
pyCHPP is licensed under the Apache License 2.0.
