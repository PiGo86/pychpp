# Installation

pyCHPP requires **Python >= 3.11**.

With pip:

```bash
pip install pychpp
```

With [uv](https://docs.astral.sh/uv/):

```bash
uv add pychpp
```

## CHPP application credentials

To use the CHPP API, you first need to register an application on Hattrick
(CHPP portal) to obtain a **consumer key** and a **consumer secret**.
These are passed to the `CHPP` constructor together with the user access token
(see [Authentication](authentication.md)).
