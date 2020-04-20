class HTChallenge:
    """
    Managing challenges on Hattrick
    """

    _SOURCE_FILE = 'challenges'
    _SOURCE_FILE_VERSION = '1.6'
    _ACTION_TYPE = 'view'

    _REQUEST_ARGS = {'file': _SOURCE_FILE,
                     'version': _SOURCE_FILE_VERSION,
                     'action_type': _ACTION_TYPE,
                     }

    def list(self):
        pass

    @classmethod
    def launch(cls, chpp, team_ht_id, opponent_team_ht_id,
               match_type='normal', match_place='home', arena_ht_id=0, match_period='week'):

        # Check parameters integrity
        if not isinstance(team_ht_id, int):
            raise ValueError('team_ht_id must be an integer')
        elif not isinstance(opponent_team_ht_id, int):
            raise ValueError('opponent_team_ht_id must be an integer')
        elif match_type not in ('normal', 'cup_rules'):
            raise ValueError("match_type must be equal to 'normal' or 'cup_rules'")
        elif match_place not in ('home', 'away', 'neutral'):
            raise ValueError("match_type must be equal to 'home', 'away' or 'neutral'")
        elif not isinstance(arena_ht_id, int):
            raise ValueError('arena_ht_id must be an integer')
        elif match_period not in ('week', 'weekend'):
            raise ValueError("match_period must be equal to 'week' or 'weekend'")

        # Defined request arguments according to method parameters
        cls._REQUEST_ARGS['actionType'] = 'challenge'
        cls._REQUEST_ARGS['teamId'] = str(team_ht_id)
        cls._REQUEST_ARGS['opponentTeamId'] = str(opponent_team_ht_id)
        cls._REQUEST_ARGS['matchType'] = {'normal': '0', 'cup_rules': '1'}[match_type]
        cls._REQUEST_ARGS['matchPlace'] = {'home': '0', 'away': '1', 'neutral': '2'}[match_place]
        cls._REQUEST_ARGS['neutralArenaId'] = str(arena_ht_id)
        cls._REQUEST_ARGS['isWeekendFriendly'] = {'week': '0', 'weekend': '1'}[match_period]

        # Send Hattrick request
        data = chpp.request(**cls._REQUEST_ARGS)
        return data

    def accept(self, team_ht_id, training_match_ht_id):
        pass

    def decline(self, team_ht_id, training_match_ht_id):
        pass

    def withdraw(self, team_id, training_match_id):
        pass
