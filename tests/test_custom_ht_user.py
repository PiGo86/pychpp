import re

from pychpp.models.custom.ht_user import HTUser
from .fixtures import chpp, USER_PATTERN


def test_get_current_user(chpp):
    user = chpp.user()

    assert isinstance(user, HTUser)
    assert isinstance(user.id, int)
    assert isinstance(user.login_name, str)
    assert user.username == user.login_name

    user_match = re.match(USER_PATTERN, user.url)
    assert user_match is not None
    assert int(user_match.group(1)) == user.id
