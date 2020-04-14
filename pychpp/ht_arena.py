class HTArena:
    """
    Hattrick arena
    """

    def __init__(self, chpp, ht_id=None):

        self._chpp = chpp
        kwargs = {}

        if ht_id is not None:
            kwargs['arenaID'] = ht_id

        data = chpp.request(file='arenadetails',
                            version='1.5',
                            **kwargs,
                            ).find('Arena')

        self.ht_id = int(data.find('ArenaID').text)
        self.name = data.find('ArenaName').text

        cap_data = data.find('CurrentCapacity')
        rebuilt_date = (cap_data.find('RebuiltDate').text
                        if cap_data.find('RebuiltDate').attrib['Available'] == 'True'
                        else None
                        )

        self.capacity = {'rebuilt_date': rebuilt_date,
                         'terraces': int(cap_data.find('Terraces').text),
                         'basic': int(cap_data.find('Basic').text),
                         'roof': int(cap_data.find('Roof').text),
                         'vip': int(cap_data.find('VIP').text),
                         'total': int(cap_data.find('Total').text),
                         }

        exp_data = data.find('ExpandedCapacity')

        if exp_data.attrib['Available'] == 'True':
            self.expanded_capacity = {'expansion_date': exp_data.find('ExpansionDate').text,
                                      'terraces': int(exp_data.find('Terraces').text),
                                      'basic': int(exp_data.find('Basic').text),
                                      'roof': int(exp_data.find('Roof').text),
                                      'vip': int(exp_data.find('VIP').text),
                                      'total': int(exp_data.find('Total').text),
                                      }
        else:
            self.expanded_capacity = None

    def __repr__(self):
        return f'<{self.__class__.__name__} object : {self.name} ({self.ht_id})>'
