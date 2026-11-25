# Error handling

When the CHPP API returns an error (`chpperror.xml`), pyCHPP raises a dedicated
exception from `pychpp.fixtures.ht_error`, subclass of `HTError`:

```python
from pychpp import CHPP
from pychpp.fixtures import ht_error

chpp = CHPP(consumer_key, consumer_secret, token_key, token_secret)

try:
    team = chpp.team(1165592)
except ht_error.HTUnauthorizedAction:
    # 401: missing/invalid scope or credentials
    ...
except ht_error.HTUnknownTeamIdError:
    # error code 50: unknown team id
    ...
except ht_error.HTError as e:
    # any other CHPP error (HTAccessDeniedError, HTChallengeError, ...)
    ...
```

Invalid arguments (wrong types, unknown `action_type`, ...) raise a plain
`ValueError`.
