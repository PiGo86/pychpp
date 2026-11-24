# pyCHPP

pyCHPP is an object-oriented Python framework for the [Hattrick](https://www.hattrick.org) CHPP API.

It provides:

- a `CHPP` client class with one `xml_*()` method per CHPP XML file (e.g. `xml_arena_details()` fetches `arenadetails.xml`),
- high-level custom models (`HTTeam`, `HTPlayer`, `HTMatch`, ...) that allow navigating between objects (e.g. `team.players()`).

## Quick start

```python
from pychpp import CHPP

chpp = CHPP(consumer_key, consumer_secret, access_token_key, access_token_secret)

user = chpp.user()          # the authenticated user
team = chpp.team()          # the user's primary team
players = chpp.xml_players(team_id=team.team_id)
```

## Next steps

- [Installation](guide/installation.md)
- [Authentication (OAuth flow)](guide/authentication.md)
- [Error handling](guide/errors.md)
- [Examples](guide/examples.md)
- [API reference](api/index.md)
