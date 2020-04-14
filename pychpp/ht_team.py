from pychpp import ht_user, ht_player


class HTCoreTeam:
    """
    Core Hattrick team
    Used to create HTTeam and HTYouthTeam classes
    """

    _SOURCE_FILE = 'teamdetails'
    _SOURCE_FILE_VERSION = '3.4'
    _REQUEST_ARGS = {}

    def __init__(self, chpp, ht_id=None):

        self._chpp = chpp

        # If set, check ht_id integrity and add to request arguments
        # If not set, request will fetch team of current user
        if ht_id is not None:
            if not isinstance(ht_id, int):
                raise ValueError('ht_id must be an integer')
            else:
                if 'youthTeamId' not in self._REQUEST_ARGS:
                    self._REQUEST_ARGS['teamID'] = ht_id
                else:
                    self._REQUEST_ARGS['youthTeamId'] = ht_id

        data = chpp.request(file=self._SOURCE_FILE,
                            version=self._SOURCE_FILE_VERSION,
                            **self._REQUEST_ARGS,
                            )

        # team_data depends on team type (senior or youth)
        if data.find('Teams') is not None:
            team_data = data.find('Teams').find('Team')
        else:
            team_data = data.find('YouthTeam')

        self._data = data
        self._team_data = team_data

        # Assign common attributes
        self.short_name = team_data.find('ShortTeamName').text

    def __repr__(self):
        return f'<{self.__class__.__name__} object : {self.name} ({self.ht_id})>'


class HTTeam(HTCoreTeam):
    """
    Hattrick team
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ht_id = int(self._team_data.find('TeamID').text)

        self._user_data = self._data.find('User')
        self._user_ht_id = int(self._user_data.find('UserID').text)

        self.name = self._team_data.find('TeamName').text
        self.founded_date = self._team_data.find('FoundedDate').text
        self.is_primary_club = True if self._team_data.find('IsPrimaryClub').text == 'True' else False

    @property
    def user(self):
        """Owner of the current team"""
        return ht_user.HTUser(chpp=self._chpp, ht_id=self._user_ht_id)

    @property
    def players(self):
        """Players list of current team"""
        data = self._chpp.request(file='players',
                                  version='2.4',
                                  actionType='view',
                                  teamID=self.ht_id).find('Team').find('PlayerList')

        return [ht_player.HTPlayer(chpp=self._chpp,
                                   data=p_data,
                                   team_ht_id=self.ht_id) for p_data in data.findall('Player')]

    @property
    def youth_team(self):
        yt_id = int(self._team_data.find('YouthTeamID').text)
        return HTYouthTeam(chpp=self._chpp, ht_id=yt_id) if yt_id != 0 else None


class HTYouthTeam(HTCoreTeam):
    """
    Hattrick youth team
    """

    _SOURCE_FILE = 'youthteamdetails'
    _SOURCE_FILE_VERSION = '1.1'
    _REQUEST_ARGS = {'youthTeamId': None}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ht_id = int(self._team_data.find('YouthTeamID').text)
        self.name = self._team_data.find('YouthTeamName').text
        self.created_date = self._team_data.find('CreatedDate').text

    @property
    def players(self):
        """Players list of current team"""
        data = self._chpp.request(file='youthplayerlist',
                                  version='2.4',
                                  actionType='details',
                                  youthTeamID=self.ht_id).find('PlayerList')

        return [ht_player.HTYouthPlayer(chpp=self._chpp,
                                        data=p_data,
                                        team_ht_id=self.ht_id) for p_data in data.findall('YouthPlayer')]
