class HTUser:
    """
    Represent a Hattrick user
    """

    def __init__(self, chpp, ht_id=None):

        kwargs = {}

        if ht_id is not None:
            kwargs['userid'] = ht_id

        data = chpp.request(file='managercompendium',
                            version='1.2',
                            **kwargs,
                            ).find('Manager')

        self.ht_id = int(data.find('UserId').text)
        self.username = data.find('Loginname').text
        self.supporter_tier = data.find('SupporterTier').text
        self.last_logins = [login.text for login in data.find('LastLogins').findall('LoginTime')]

    def __repr__(self):
        return f'<HTUser object : {self.username} ({self.ht_id})>'




