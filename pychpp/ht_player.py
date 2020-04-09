class HTPlayer:
    """
    Represents a Hattrick player
    """

    def __init__(self, chpp, ht_id=None):

        self.chpp = chpp

        kwargs = {'actionType': 'view'}

        if ht_id is not None:
            kwargs['playerID'] = ht_id

        data = chpp.request(file='playerdetails',
                            version='2.8',
                            **kwargs,
                            ).find('Player')

        self.ht_id = int(data.find('PlayerID').text)
        self.first_name = data.find('FirstName').text
        self.nick_name = data.find('NickName').text
        self.last_name = data.find('LastName').text
        self.player_number = int(data.find('PlayerNumber').text)
        self.category_id = int(data.find('PlayerCategoryID').text)
        self.owner_notes = data.find('OwnerNotes').text
        self.age = int(data.find('Age').text)
        self.age_days = int(data.find('AgeDays').text)
        self.next_birth_day = data.find('NextBirthDay').text
        self.arrival_date = data.find('ArrivalDate').text
        self.player_form = int(data.find('PlayerForm').text)
        self.cards = int(data.find('Cards').text)
        self.injury_level = int(data.find('InjuryLevel').text)
        self.statement = data.find('Statement').text
        self.player_language = data.find('PlayerLanguage').text
        self.player_language_id = data.find('PlayerLanguageID').text
        self.agreeability = int(data.find('Agreeability').text)
        self.aggressiveness = int(data.find('Aggressiveness').text)
        self.honesty = int(data.find('Honesty').text)
        self.experience = int(data.find('Experience').text)
        self.loyalty = int(data.find('Loyalty').text)
        self.mother_club_bonus = True if data.find('MotherClubBonus').text == True else False
        self.leadership = int(data.find('Leadership').text)
        self.specialty = int(data.find('Specialty').text)
        self.native_country_id = int(data.find('NativeCountryID').text)
        self.native_league_id = int(data.find('NativeLeagueID').text)
        self.native_league_name = data.find('NativeLeagueName').text
        self.tsi = int(data.find('TSI').text)
        self.salary = int(data.find('Salary').text)
        self.is_abroad = True if data.find('IsAbroad').text == 'True' else False
        self.caps = int(data.find('Caps').text)
        self.caps_u20 = int(data.find('CapsU20').text)
        self.career_goals = int(data.find('CareerGoals').text)
        self.career_hattricks = int(data.find('CareerHattricks').text)
        self.league_goals = int(data.find('LeagueGoals').text)
        self.cup_goals = int(data.find('CupGoals').text)
        self.friendlies_goals = int(data.find('FriendliesGoals').text)
        self.matches_current_team = int(data.find('MatchesCurrentTeam').text)
        self.goals_current_team = int(data.find('GoalsCurrentTeam').text)
        # self.national_team_id = int(data.find('NationalTeamID').text)
        # self.national_team_name = data.find('NationalTeamName').text
        self.transfer_listed = True if data.find('TransferListed').text == 'True' else False

    def __repr__(self):
        return f'<HTPlayer object : {self.first_name} {self.last_name} ({self.ht_id})>'
