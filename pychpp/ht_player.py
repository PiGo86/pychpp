import xml
from pychpp import ht_team


class HTCorePlayer:
    """
    Default Hattrick player
    Used to create HTPlayer and HTYouthPlayer classes
    """

    _SOURCE_FILE = 'playerdetails'
    _SOURCE_FILE_VERSION = '2.8'
    _REQUEST_ARGS = {'actionType': 'view', 'playerID': None}

    def __init__(self, chpp, ht_id=None, data=None, team_ht_id=None):

        self._chpp = chpp

        # Init depends on given parameters
        # If data is not defined, ht_id has to be defined
        if data is None:

            # Check ht_id integrity as data is not defined
            if ht_id is None:
                raise ValueError('ht_id have to be defined when data is not defined')

            elif not isinstance(ht_id, int):
                raise ValueError('ht_id parameter have to be a integer')

            # If ht_id is well defined, data is fetched and self.team_ht_id defined
            else:

                if self._REQUEST_ARGS.get('playerID', None) is not None:
                    self._REQUEST_ARGS['playerID'] = ht_id
                else:
                    self._REQUEST_ARGS['youthPlayerId'] = ht_id

                data = chpp.request(file=self._SOURCE_FILE,
                                    version=self._SOURCE_FILE_VERSION,
                                    **self._REQUEST_ARGS,
                                    )

                if self._REQUEST_ARGS.get('playerID', None) is not None:
                    data = data.find('Player')
                else:
                    data = data.find('YouthPlayer')

        elif not isinstance(data, xml.etree.ElementTree.Element):
            raise ValueError('data parameter has to be an ElementTree.Element instance')

        elif team_ht_id is None:
            raise ValueError('team_ht_id must be defined as data is defined')

        # if team_ht_id is well defined, it is assigned to self.team_ht_id
        else:
            self.team_ht_id = team_ht_id

        # Skills
        if ht_id is None:
            skill_data = data
        else:
            skill_data = data.find('PlayerSkills')

        # Internal attributes
        self._data = data
        self._skill_data = skill_data

        # Assign attributes
        self.first_name = data.find('FirstName').text
        self.nick_name = data.find('NickName').text
        self.last_name = data.find('LastName').text

        self.age = int(data.find('Age').text)
        self.age_days = int(data.find('AgeDays').text)
        self.arrival_date = data.find('ArrivalDate').text
        # self.owner_notes = data.find('OwnerNotes').text
        self.statement = data.find('Statement').text

        self.league_goals = int(data.find('LeagueGoals').text)
        self.career_goals = int(data.find('CareerGoals').text)
        self.career_hattricks = int(data.find('CareerHattricks').text)
        self.specialty = int(data.find('Specialty').text)

        self.cards = int(data.find('Cards').text)
        self.injury_level = int(data.find('InjuryLevel').text)


class HTPlayer(HTCorePlayer):
    """
    Hattrick player
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        if kwargs.get('data', None) is not None:
            self.team_ht_id = kwargs['ht_id']
        else:
            self.team_ht_id = int(self._data.find('OwningTeam').find('TeamID').text)

        self.ht_id = int(self._data.find('PlayerID').text)
        self.player_number = int(self._data.find('PlayerNumber').text)
        self.tsi = int(self._data.find('TSI').text)
        self.player_form = int(self._data.find('PlayerForm').text)
        self.experience = int(self._data.find('Experience').text)
        self.loyalty = int(self._data.find('Loyalty').text)
        self.mother_club_bonus = True if self._data.find('MotherClubBonus').text == 'True' else False
        self.leadership = int(self._data.find('Leadership').text)
        self.salary = int(self._data.find('Salary').text)
        self.is_abroad = True if self._data.find('IsAbroad').text == 'True' else False
        self.agreeability = int(self._data.find('Agreeability').text)
        self.aggressiveness = int(self._data.find('Aggressiveness').text)
        self.honesty = int(self._data.find('Honesty').text)
        self.friendlies_goals = int(self._data.find('FriendliesGoals').text)
        self.cup_goals = int(self._data.find('CupGoals').text)
        self.goals_current_team = int(self._data.find('GoalsCurrentTeam').text)
        self.matches_current_team = int(self._data.find('MatchesCurrentTeam').text)
        self.transfer_listed = True if self._data.find('TransferListed').text == 'True' else False

        self.caps = int(self._data.find('Caps').text)
        self.caps_u20 = int(self._data.find('CapsU20').text)

        self.stamina_skill = int(self._skill_data.find('StaminaSkill').text)
        self.keeper_skill = int(self._skill_data.find('KeeperSkill').text)
        self.playmaker_skill = int(self._skill_data.find('PlaymakerSkill').text)
        self.scorer_skill = int(self._skill_data.find('ScorerSkill').text)
        self.passing_skill = int(self._skill_data.find('PassingSkill').text)
        self.winger_skill = int(self._skill_data.find('WingerSkill').text)
        self.defender_skill = int(self._skill_data.find('DefenderSkill').text)
        self.set_pieces_skill = int(self._skill_data.find('SetPiecesSkill').text)

    def __repr__(self):
        return f'<HTPlayer object : {self.first_name} {self.last_name} ({self.ht_id})>'

    @property
    def team(self):
        return ht_team.HTTeam(chpp=self._chpp, ht_id=self.team_ht_id)


class HTYouthPlayer(HTCorePlayer):
    """
    Hattrick youth player
    """

    _SOURCE_FILE = 'youthplayerdetails'
    _SOURCE_FILE_VERSION = '1.1'
    _REQUEST_ARGS = {'actionType': 'view', 'youthPlayerId': None}

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        if kwargs.get('data', None) is not None:
            self.team_ht_id = kwargs['ht_id']
        else:
            self.team_ht_id = int(self._data.find('OwningYouthTeam').find('YouthTeamID').text)

        self.ht_id = int(self._data.find('YouthPlayerID').text)
        self.friendlies_goals = int(self._data.find('FriendlyGoals').text)

    def __repr__(self):
        return f'<HTYouthPlayer object : {self.first_name} {self.last_name} ({self.ht_id})>'

