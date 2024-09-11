from pychpp.models.xml.manager_compendium import ManagerCompendium
from .fixtures import chpp


def test_get_current_user(chpp):
    user = chpp.xml_manager_compendium()

    assert isinstance(user, ManagerCompendium)
    assert isinstance(user.id, int)
    assert isinstance(user.login_name, str)

