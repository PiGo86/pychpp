class HTUser:
    """
    Represent a Hattrick user
    """

    def __init__(self, chpp):

        data = chpp.request(file='managercompendium',
                            version='1.2',
                            ).find('Manager')

        self.ht_id = int(data.find('UserId').text)
        self.username = data.find('Loginname').text
