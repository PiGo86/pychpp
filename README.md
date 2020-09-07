# pyCHPP

pyCHPP is an object-oriented python framework created to use the API provided by the online game Hattrick (www.hattrick.org).

## Installation

pyCHPP can be installed using pip :

    pip install pychpp

## Usage

### First connection
```python
from pychpp import CHPP
    
# Set consumer_key and consumer_secret provided for your app by Hattrick
consumer_key = ''
consumer_secret = ''
    
# Initialize CHPP instance
chpp = CHPP(consumer_key, consumer_secret)
    
# Get url, request_token and request_token_secret to request API access
# You can set callback_url and scope
auth = chpp.get_auth(callback_url="www.mycallbackurl.com", scope="")
  
# auth['url'] contains the url to which the user can grant the application
# access to the Hattrick API
# Once the user has entered their credentials,
# a code is returned by Hattrick (directly or to the given callback url)
code = ""

# Get access token from Hattrick
# access_token['key'] and access_token['secret'] have to be stored
# in order to be used later by the app
access_token = chpp.get_access_token(
                request_token=auth["request_token"],
                request_token_secret=auth["request_token_secret"],
                code=code,
                )
```
### Further connections
```python
# Once you have obtained access_token for a user
# You can use it to call Hattrick API
chpp = CHPP(consumer_key,
            consumer_secret,
            access_token['key'],
            access_token['secret'],
            )
    
# Now you can use chpp methods to get datas from Hattrick API
# For example :
current_user = chpp.user()
all_teams = current_user.teams

best_team_ever = chpp.team(ht_id=1165592)
best_team_ever # <HTTeam object : Les Poitevins de La Chapelle (1165592)>

best_team_arena = best_team_ever.arena
best_team_arena # <HTArena object : Stade de La Chapelle (1162154)>
best_team_arena.name # 'Stade de La Chapelle'

worth_team_ever = chpp.team(ht_id=1750803)
worth_team_ever # <HTTeam object : Capdenaguet (1750803)>

player = chpp.player(ht_id=6993859)
player # <HTPlayer object : Pedro Zurita (6993859)>
player.career_goals # 1163

match = chpp.match(ht_id=68599186)
match # <HTMatch object : Skou United - FC Barentin (68599186)>
match.date # datetime.datetime(2006, 2, 23, 20, 0)
```

## Mapping table between classes and CHPP XML files
The following table shows the relationships between pyCHPP classes and CHPP XML files :

|pyCHPP class|CHPP XML files|
|:---:|:---:|
|HTArena|`arenadetails.xml`|
|HTChallengeManager|`challenges.xml`|
|HTLeague|`leaguedetails.xml`|
|HTMatch|`matchdetails.xml`|
|HTMatchLineup|`matchlineup.xml`|
|HTMatchesArchive|`matchesarchive.xml`|
|HTPlayer|`playerdetails.xml`|
|HTRegion|`regiondetails.xml`|
|HTTeam|`teamdetails.xml`|
|HTUser|`managercompendium.xml`|
|HTWorld|`worlddetails.xml`|
|HTYouthPlayer|`youthplayerdetails.xml`|
|HTYouthTeam|`youthteamdetails.xml`|

## License
pyCHPP is licensed under the Apache License 2.0.