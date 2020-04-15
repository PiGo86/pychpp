import xml
from pychpp import ht_team
from pychpp.ht_date import HTDate


class HTCorePlayer:
    """
    Core Hattrick player
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

                # Request arguments depends on player type (senior or youth)
                if 'playerID' in self._REQUEST_ARGS:
                    self._REQUEST_ARGS['playerID'] = ht_id
                else:
                    self._REQUEST_ARGS['youthPlayerId'] = ht_id

                data = chpp.request(file=self._SOURCE_FILE,
                                    version=self._SOURCE_FILE_VERSION,
                                    **self._REQUEST_ARGS,
                                    )

                # Xml main tag depends on player type (senior or youth)
                if 'playerID' in self._REQUEST_ARGS:
                    data = data.find('Player')
                else:
                    data = data.find('YouthPlayer')

        elif not isinstance(data, xml.etree.ElementTree.Element):
            raise ValueError('data parameter has to be an ElementTree.Element instance')

        elif team_ht_id is None:
            raise ValueError('team_ht_id must be defined as data is defined')

        # Skills
        if ht_id is None:
            skill_data = data
        else:
            skill_data = data.find('PlayerSkills')

        # Internal attributes
        self._data = data
        self._skill_data = skill_data
        self.ht_id = ht_id

        # Assign attributes
        self.first_name = data.find('FirstName').text
        self.nick_name = data.find('NickName').text
        self.last_name = data.find('LastName').text

        self.age = int(data.find('Age').text)
        self.age_days = int(data.find('AgeDays').text)
        self.arrival_date = HTDate.from_ht(data.find('ArrivalDate').text)
        self.statement = data.find('Statement').text

        self.league_goals = int(data.find('LeagueGoals').text)
        self.career_goals = int(data.find('CareerGoals').text)
        self.career_hattricks = int(data.find('CareerHattricks').text)
        self.specialty = int(data.find('Specialty').text)

        self.cards = int(data.find('Cards').text)
        self.injury_level = int(data.find('InjuryLevel').text)

    def __repr__(self):
        return f'<{self.__class__.__name__} object : {self.first_name} {self.last_name} ({self.ht_id})>'


class HTPlayer(HTCorePlayer):
    """
    Hattrick player
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # team_ht_id is defined by arguments or inside xml data
        if kwargs.get('data', None) is not None:
            self.team_ht_id = kwargs['ht_id']
        else:
            self.team_ht_id = int(self._data.find('OwningTeam').find('TeamID').text)

        # Assign specific senior player attributes
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

        # attributes only visible for team of current user
        self.owner_notes = (self._data.find('OwnerNotes').text
                            if self._data.find('OwnerNotes') is not None else None)

        # TODO: connect to HTSkill class
        # stamina is always available
        self.stamina_skill = int(self._skill_data.find('StaminaSkill').text)

        # other skills are only available if this current user team
        # if skills are not available, set to None
        self.keeper_skill = (int(self._skill_data.find('KeeperSkill').text)
                             if self._skill_data.find('KeeperSkill') is not None else None)

        self.playmaker_skill = (int(self._skill_data.find('PlaymakerSkill').text)
                                if self._skill_data.find('PlaymakerSkill') is not None else None)

        self.scorer_skill = (int(self._skill_data.find('ScorerSkill').text)
                             if self._skill_data.find('ScorerSkill') is not None else None)

        self.passing_skill = (int(self._skill_data.find('PassingSkill').text)
                              if self._skill_data.find('PassingSkill') is not None else None)

        self.winger_skill = (int(self._skill_data.find('WingerSkill').text)
                             if self._skill_data.find('WingerSkill') is not None else None)

        self.defender_skill = (int(self._skill_data.find('DefenderSkill').text)
                               if self._skill_data.find('DefenderSkill') is not None else None)

        self.set_pieces_skill = (int(self._skill_data.find('SetPiecesSkill').text)
                                 if self._skill_data.find('SetPiecesSkill') is not None else None)

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

        # team_ht_id is defined by arguments or inside xml data
        if kwargs.get('data', None) is not None:
            self.team_ht_id = kwargs['ht_id']
        else:
            self.team_ht_id = int(self._data.find('OwningYouthTeam').find('YouthTeamID').text)

        # Assign specific youth player attributes
        self.ht_id = int(self._data.find('YouthPlayerID').text)
        self.can_be_promoted_in = int(self._data.find('CanBePromotedIn').text)
        self.player_number = (int(self._data.find('PlayerNumber').text)
                              if self._data.find('PlayerNumber') is not None
                              else None)
        self.player_category_id = (int(self._data.find('PlayerCategoryID').text)
                                   if self._data.find('PlayerNumber') is not None
                                   else None)
        self.friendlies_goals = int(self._data.find('FriendlyGoals').text)

        # Skills attributes
        # TODO: connect to HTYouthSkill class
        self.keeper_skill = int(self._skill_data.find('KeeperSkill').text)
        self.playmaker_skill = int(self._skill_data.find('PlaymakerSkill').text)
        self.scorer_skill = int(self._skill_data.find('ScorerSkill').text)
        self.passing_skill = int(self._skill_data.find('PassingSkill').text)
        self.winger_skill = int(self._skill_data.find('WingerSkill').text)
        self.defender_skill = int(self._skill_data.find('DefenderSkill').text)
        self.set_pieces_skill = int(self._skill_data.find('SetPiecesSkill').text)
