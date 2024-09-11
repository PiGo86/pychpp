from pychpp.models.custom import CustomModel
from pychpp.models.ht_field import HTAliasField
from pychpp.models.xml import manager_compendium


class HTUser(manager_compendium.ManagerCompendium, CustomModel):
    """
    Hattrick user
    """

    URL_PATH = '/Club/Manager/'

    username: str = HTAliasField(target='login_name')