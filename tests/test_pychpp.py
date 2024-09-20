import os
import datetime as dt
import pytz
import pytest
import re
import pathlib
import xml.etree.ElementTree

from pychpp import CHPP

from .fixtures import chpp, mocked_chpp


def test_request_token(chpp: CHPP):

    auth = chpp.get_auth(scope='')

    assert isinstance(auth, dict)
    for key in auth.keys():
        assert key in ('request_token', 'request_token_secret', 'url',)

    assert isinstance(auth['request_token'], str) and auth['request_token']
    assert isinstance(auth['request_token_secret'],
                      str) and auth['request_token_secret']
    assert (isinstance(auth['url'], str)
            and 'https://chpp.hattrick.org/oauth/authorize.aspx'
                '?scope=&oauth_token=' in auth['url'])

