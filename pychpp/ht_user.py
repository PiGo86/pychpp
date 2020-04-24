from pychpp import ht_team


class HTUser:
    """
    Hattrick user
    """

    def __init__(self, chpp, ht_id=None):
        """
        Initialize HTUser instance

        :param chpp: CHPP instance of connected user
        :param ht_id: user Hattrick ID (if none, fetch the connected user), defaults to None
        :type chpp: CHPP
        :type ht_id: int, optional
        """
        self._chpp = chpp
        kwargs = {}

        if ht_id is not None:
            kwargs["userid"] = ht_id

        data = chpp.request(file="managercompendium",
                            version="1.2",
                            **kwargs,
                            ).find("Manager")

        teams_data = data.find("Teams")

        self.teams_data = teams_data

        # Assign attributes
        self.ht_id = int(data.find("UserId").text)
        self.username = data.find("Loginname").text
        self.supporter_tier = data.find("SupporterTier").text
        self.last_logins = [login.text for login in data.find("LastLogins").findall("LoginTime")]

        self._teams_ht_id = [int(team.find("TeamId").text) for team in teams_data.findall("Team")]

    def __repr__(self):
        return f"<HTUser object : {self.username} ({self.ht_id})>"

    @property
    def teams(self):
        """Teams list of current user"""
        return [ht_team.HTTeam(chpp=self._chpp, ht_id=team_ht_id) for team_ht_id in self._teams_ht_id]
