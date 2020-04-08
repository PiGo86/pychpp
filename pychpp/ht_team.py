from pychpp import ht_user


class HTTeam:
    """
    Represents a Hattrick team
    """

    def __init__(self, chpp, ht_id=None):

        self.chpp = chpp

        kwargs = {}

        if ht_id is not None:
            kwargs['teamID'] = ht_id

        data = chpp.request(file='teamdetails',
                            version='3.4',
                            **kwargs,
                            )
        team_data = data.find('Teams').find('Team')
        user_data = data.find('User')

        self.ht_id = int(team_data.find('TeamID').text)
        self.name = team_data.find('TeamName').text
        self.short_name = team_data.find('ShortTeamName').text
        self.is_primary_club = team_data.find('IsPrimaryClub').text
        self.founded_date = team_data.find('FoundedDate').text

        self._user_ht_id = int(user_data.find('UserID').text)

    def __repr__(self):
        return f'<HTTeam object : {self.name} ({self.ht_id})>'

    @property
    def user(self):
        return ht_user.HTUser(self.chpp, ht_id=self._user_ht_id)

