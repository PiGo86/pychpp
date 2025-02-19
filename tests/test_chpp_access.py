from pychpp import CHPP


def test_request_token(chpp: CHPP):

    auth = chpp.get_auth(scope='')

    assert isinstance(auth, dict)
    for key in auth.keys():
        assert key in ('oauth_token', 'oauth_token_secret', 'oauth_callback_confirmed', 'url',)

    assert isinstance(auth['oauth_token'], str) and auth['oauth_token']
    assert isinstance(auth['oauth_token_secret'],
                      str) and auth['oauth_token_secret']
    assert (isinstance(auth['url'], str)
            and 'https://chpp.hattrick.org/oauth/authorize.aspx'
                '?scope=&oauth_token=' in auth['url'])
