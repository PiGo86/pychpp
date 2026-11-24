# Authentication

pyCHPP uses the OAuth 1.0a flow of the Hattrick CHPP API.

## First connection: obtain an access token

```python
from pychpp import CHPP

chpp = CHPP(consumer_key, consumer_secret)

# Get the authorization url and the request token
auth = chpp.get_auth(callback_url="www.mycallbackurl.com", scope="")

# Redirect the user to auth["url"] so they can grant your app access.
# Once they have entered their credentials, Hattrick returns a code
# (directly or to the callback url).
code = "..."

# Exchange the request token + code for an access token
access_token = chpp.get_access_token(
    request_token=auth["oauth_token"],
    request_token_secret=auth["oauth_token_secret"],
    code=code,
)

# access_token["key"] and access_token["secret"] must be stored
# to be reused for this user later.
```

### Scopes

`scope` can be a string or a list, among:
`"manage_challenges"`, `"set_matchorder"`, `"manage_youthplayers"`,
`"set_training"`, `"place_bid"`. An empty scope gives read-only access.

## Further connections

Once you have stored the access token of a user:

```python
chpp = CHPP(consumer_key, consumer_secret,
            access_token["key"], access_token["secret"])

# Check that the token is still valid
chpp.check_token()

# Invalidate the token when the user disconnects
chpp.invalidate_token()
```
