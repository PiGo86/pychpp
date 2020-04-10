from pychpp import ht_user, ht_player


class HTTeam:
    """
    Represents a Hattrick team
    """

    def __init__(self, chpp, ht_id=None):

        self._chpp = chpp

        kwargs = {}

        if ht_id is not None:
            kwargs['teamID'] = ht_id

        data = chpp.request(file='teamdetails',
                            version='3.4',
                            **kwargs,
                            )
        team_data = data.find('Teams').find('Team')
        user_data = data.find('User')

        # Assign attributes
        self.ht_id = int(team_data.find('TeamID').text)
        self.name = team_data.find('TeamName').text
        self.short_name = team_data.find('ShortTeamName').text
        self.is_primary_club = True if team_data.find('IsPrimaryClub').text == True else False
        self.founded_date = team_data.find('FoundedDate').text

        self._user_ht_id = int(user_data.find('UserID').text)

    def __repr__(self):
        return f'<HTTeam object : {self.name} ({self.ht_id})>'

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

        return [ht_player.HTPlayer(chpp=self._chpp, data=p_data) for p_data in data.findall('Player')]

