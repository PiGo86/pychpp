# Examples

## High-level custom models

```python
>>> current_user = chpp.user()
>>> all_teams = current_user.teams

>>> team = chpp.team(1165592)
>>> team
<HTTeam object - Les Poitevins de La Chapelle (1165592)>

>>> team.arena.details()
<HTArena object - Stade de La Chapelle (1162154)>

>>> player = chpp.player(6993859)
>>> player.career_goals
1167

>>> match = chpp.match(68599186)
>>> match.date
<HTDatetime object - 2006-02-23 20:00:00 CET+0100 (S28, W8, D4)>
```

Custom models allow navigating between objects, e.g. `team.players()` returns
the team's players.

## Raw XML models

Each CHPP XML file has a matching model under `pychpp.models.xml`, fetched
through the `xml_*()` methods of the `CHPP` instance:

```python
>>> xml_arena = chpp.xml_arena_details(arena_id=294762)
>>> xml_arena
<ArenaDetails object - Stade Dimitri Liénard (294762)>
```

See the [CHPP client API reference](../api/chpp.md) for the full list of
`xml_*()` methods and their parameters.
