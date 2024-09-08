from pychpp.models.ht_field import HTAliasField
from pychpp.models.xml import manager_compendium


class HTUser(manager_compendium.ManagerCompendium):
    """
    Hattrick user
    """
    username: str = HTAliasField(target='login_name')