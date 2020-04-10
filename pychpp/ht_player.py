import xml
from pychpp import ht_team


class HTPlayer:
    """
    Represents a Hattrick player
    """

    def __init__(self, chpp, ht_id=None, data=None, team_ht_id=None):

        self._chpp = chpp

        # Init depends on given parameters
        # If chpp is given, data variable as to be defined
        if data is None:

            # Check ht_id integrity as data is not defined
            if ht_id is None:
                raise ValueError('ht_id have to be defined when data is not defined')

            elif not isinstance(ht_id, int):
                raise ValueError('ht_id parameter have to be a integer')

            # If ht_id is well defined, data is fetched and self.team_ht_id defined
            else:

                kwargs = {'actionType': 'view', 'playerID': ht_id}
                data = chpp.request(file='playerdetails',
                                    version='2.8',
                                    **kwargs,
                                    ).find('Player')
                self.team_ht_id = int(data.find('OwningTeam').find('TeamID').text)

        elif not isinstance(data, xml.etree.ElementTree.Element):
            raise ValueError('data parameter has to be an ElementTree.Element instance')

        elif team_ht_id is None:
            raise ValueError('team_ht_id must be defined as data is defined')

        # if team_ht_id is well defined, it is assigned to self.team_ht_id
        else:
            self.team_ht_id = team_ht_id

        # Assign attributes
        self.ht_id = int(data.find('PlayerID').text)
        self.first_name = data.find('FirstName').text
        self.nick_name = data.find('NickName').text
        self.last_name = data.find('LastName').text
        self.player_number = int(data.find('PlayerNumber').text)
        self.age = int(data.find('Age').text)
        self.age_days = int(data.find('AgeDays').text)
        self.arrival_date = data.find('ArrivalDate').text
        self.owner_notes = data.find('OwnerNotes').text
        self.tsi = int(data.find('TSI').text)
        self.player_form = int(data.find('PlayerForm').text)
        self.statement = data.find('Statement').text
        self.experience = int(data.find('Experience').text)
        self.loyalty = int(data.find('Loyalty').text)
        self.mother_club_bonus = True if data.find('MotherClubBonus').text == True else False
        self.leadership = int(data.find('Leadership').text)
        self.salary = int(data.find('Salary').text)
        self.is_abroad = True if data.find('IsAbroad').text == 'True' else False
        self.agreeability = int(data.find('Agreeability').text)
        self.aggressiveness = int(data.find('Aggressiveness').text)
        self.honesty = int(data.find('Honesty').text)
        self.league_goals = int(data.find('LeagueGoals').text)
        self.cup_goals = int(data.find('CupGoals').text)
        self.friendlies_goals = int(data.find('FriendliesGoals').text)
        self.career_goals = int(data.find('CareerGoals').text)
        self.career_hattricks = int(data.find('CareerHattricks').text)
        self.matches_current_team = int(data.find('MatchesCurrentTeam').text)
        self.goals_current_team = int(data.find('GoalsCurrentTeam').text)
        self.specialty = int(data.find('Specialty').text)
        self.transfer_listed = True if data.find('TransferListed').text == 'True' else False

        self.caps = int(data.find('Caps').text)
        self.caps_u20 = int(data.find('CapsU20').text)
        self.cards = int(data.find('Cards').text)
        self.injury_level = int(data.find('InjuryLevel').text)

        # Skills
        if ht_id is None:
            skill_data = data
        else:
            skill_data = data.find('PlayerSkills')

        self.stamina_skill = int(skill_data.find('StaminaSkill').text)
        self.keeper_skill = int(skill_data.find('KeeperSkill').text)
        self.playmaker_skill = int(skill_data.find('PlaymakerSkill').text)
        self.scorer_skill = int(skill_data.find('ScorerSkill').text)
        self.passing_skill = int(skill_data.find('PassingSkill').text)
        self.winger_skill = int(skill_data.find('WingerSkill').text)
        self.defender_skill = int(skill_data.find('DefenderSkill').text)
        self.set_pieces_skill = int(skill_data.find('SetPiecesSkill').text)

        # tags name depending on xml source file (players.xml vs playerdetails.xml)
        if ht_id is None:
            self.national_team_id = int(data.find('NationalTeamID').text)
            self.country_id = int(data.find('CountryID').text)
            self.category_id = int(data.find('PlayerCategoryId').text)

        else:
            self.country_id = int(data.find('NativeCountryID').text)
            self.native_league_id = int(data.find('NativeLeagueID').text)
            self.native_league_name = data.find('NativeLeagueName').text
            self.next_birth_day = data.find('NextBirthDay').text
            self.player_language = data.find('PlayerLanguage').text
            self.player_language_id = data.find('PlayerLanguageID').text

    def __repr__(self):
        return f'<HTPlayer object : {self.first_name} {self.last_name} ({self.ht_id})>'

    @property
    def team(self):
        return ht_team.HTTeam(chpp=self._chpp, ht_id=self.team_ht_id)
