from rauth import OAuth1Service
from rauth import OAuth1Session
from rauth.oauth import HmacSha1Signature

import xml.etree.ElementTree as ET
import datetime


class CHPP:
    """
    Manage connection and requests with Hattrick API
    """
    def __init__(self, consumer_key, consumer_secret, access_token_key='', access_token_secret=''):

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret

        self.request_token_url = 'https://chpp.hattrick.org/oauth/request_token.ashx'
        self.access_token_url = 'https://chpp.hattrick.org/oauth/access_token.ashx'
        self.authorize_url = 'https://chpp.hattrick.org/oauth/authorize.aspx'
        self.base_url = 'https://chpp.hattrick.org/chppxml.ashx'

        self.service = OAuth1Service(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            request_token_url=self.request_token_url,
            access_token_url=self.access_token_url,
            authorize_url=self.authorize_url,
            base_url=self.base_url,
            signature_obj=HmacSha1Signature,
        )

    def get_auth(self, callback_url='oob', scope=''):
        """
        Get url, request_token and request_token_secret to get auth from Hattrick for this user
        :param callback_url: url that have to be request by Hattrick after the user have fill his credentials
        :param scope: authorization granted by user to the application
                      can be '', 'manage_challenges', 'set_matchorder', 'manage_youthplayers',
                      'set_training', 'place_bid'
        :return: {'request_token': ..., 'request_token_secret':..., 'url': ...}
        """
        auth = dict()

        request_token, request_token_secret = self.service.get_request_token(params={'oauth_callback': callback_url})

        auth['request_token'] = request_token
        auth['request_token_secret'] = request_token_secret
        auth['url'] = self.service.get_authorize_url(request_token, scope=scope)

        return auth

    def get_access_token(self, request_token, request_token_secret, code):
        """
        Query access token from Hattrick once the user granted the application on Hattrick
        Access token have to be stored by the application in order to be used for following use of CHPP class
        :param request_token: returned by get_auth
        :param request_token_secret: returned by get_auth
        :param code: code returned by Hattrick after the user granted the application
                     send to callback_url by Hattrick or shown direclty on Hattrick if callback_url was ''
        :return: {'key': ..., 'secret': ...}
        """
        access_token_query = self.service.get_access_token(request_token,
                                                           request_token_secret,
                                                           params={'oauth_verifier': code},
                                                           )

        access_token = dict()

        access_token['key'] = access_token_query[0]
        access_token['secret'] = access_token_query[1]

        return access_token

    def open_session(self):
        return OAuth1Session(self.consumer_key,
                             self.consumer_secret,
                             access_token=self.access_token_key,
                             access_token_secret=self.access_token_secret,
                             )

    def request(self, **params):

        session = self.open_session()
        query = session.get(self.base_url, params=params)
        query.encoding = 'UTF-8'

        result = ET.fromstring(query.text)
        file_name = result.find('FileName').text

        # Si Hattrick renvoie une erreur, on lance une exception appropriée
        # selon le code d'erreur
        if file_name == 'chpperror.xml':
            raise HTUndefinedError(result.find('Error').text)

        return result

    def get_current_user(self):

        result = self.request(file='managercompendium',
                              version='1.2',
                              )

        infos = result.find('Manager')

        user = dict()

        user['id'] = int(infos.find('UserId').text)
        user['username'] = infos.find('Loginname').text

        return user

    def get_user_teams(self):

        result = self.request(file='managercompendium',
                              version='1.2',
                              )

        infos = result.find('Manager')

        teams = list()

        for t in infos.find('Teams').findall('Team'):
            team = dict()
            team['id'] = int(t.find('TeamId').text)
            team['name'] = t.find('TeamName').text
            team['arena_id'] = int(t.find('Arena').find('ArenaId').text)
            team['country'] = t.find('League').find('LeagueName').text
            team['region'] = t.find('Region').find('RegionName').text
            teams.append(team)

        return teams

    def get_team(self, team_id):

        infos = self.request(file='teamdetails',
                             version='3.4',
                             teamID=f'{team_id}',
                             )

        team = dict()

        team['user_id'] = int(infos.find('User').find('UserID').text)
        team['user_name'] = infos.find('User').find('Loginname').text

        team['id'] = None
        team['name'] = None
        team['short_name'] = None
        team['arena_id'] = None

        for t in infos.find('Teams').findall('Team'):
            if t.find('TeamID').text == str(team_id):
                team['id'] = team_id
                team['name'] = t.find('TeamName').text
                team['short_name'] = t.find('ShortTeamName').text
                team['arena_id'] = int(t.find('Arena').find('ArenaID').text)
                team['country'] = t.find('League').find('LeagueName').text
                team['region'] = t.find('Region').find('RegionName').text

        return team

    def get_arena(self, arena_id):

        result = self.request(file='arenadetails',
                              version='1.5',
                              arenaID=f'{arena_id}',
                              )

        infos = result.find('Arena')

        arena = dict()
        arena['id'] = arena_id
        arena['name'] = infos.find('ArenaName').text
        arena['capacity'] = int(infos.find('CurrentCapacity').find('Total').text)
        arena['country'] = infos.find('League').find('LeagueName').text
        arena['region'] = infos.find('Region').find('RegionName').text

        return arena

    def get_challenges(self, author, weekend):

        xml = self.request(
            file='challenges',
            version='1.6',
            actionType='view',
            isWeekendFriendly=weekend
        )

        if author == 'ByMe':
            xml = xml.find('Team').find('ChallengesByMe')
            child = 'Challenge'
        elif author == 'ByOthers':
            xml = xml.find('Team').find('OffersByOthers')
            child = 'Offer'
        else:
            raise ValueError('author must be "ByMe" or "ByOthers"')

        challenges = list()

        if xml:
            for c in xml.findall(child):
                challenge = dict()
                challenge['TrainingMatchID'] = int(c.find('TrainingMatchID').text)
                challenge['MatchTime'] = datetime.datetime.strptime(c.find('MatchTime').text, '%Y-%m-%d %H:%M:%S')
                challenge['FriendlyType'] = int(c.find('FriendlyType').text)
                challenge['TeamID'] = int(c.find('Opponent').find('TeamID').text)
                challenge['ArenaID'] = int(c.find('Arena').find('ArenaID').text)
                challenge['IsAgreed'] = True if (c.find('IsAgreed').text == 'True') else False

                challenges.append(challenge)

        return challenges

    def is_challengeable(self, team_id):

        session = self.open_session()
        result = session.get(self.base_url, params={'file': 'challenges',
                                                    'version': '1.6',
                                                    'actionType': 'challengeable',
                                                    'suggestedTeamIds': str(team_id),
                                                    })

        infos = ET.fromstring(result.text)
        infos = infos.find('Team').find('ChallengeableResult').find('Opponent').find('IsChallengeable').text

        challengeable = True if infos == 'True' else False

        return challengeable

    def challenge(self, team_id, opponent_team_id, match_type, match_place, neutral_arena_id=0, weekend=0):

        result = self.request(file='challenges',
                              version='1.6',
                              actionType='challenge',
                              teamId=str(team_id),
                              opponentTeamId=str(opponent_team_id),
                              matchType=str(match_type),
                              matchPlace=str(match_place),
                              neutralArenaId=str(neutral_arena_id),
                              isWeekendFriendly=str(weekend),
                              )

        return result

    def accept_challenge(self, team_id, training_match_id):

        session = self.open_session()
        action = session.get(self.base_url, params={'file': 'challenges',
                                                    'version': '1.6',
                                                    'actionType': 'accept',
                                                    'teamId': str(team_id),
                                                    'trainingMatchId': str(training_match_id),
                                                    'isWeekendFriendly': '0',
                                                    })

        action.encoding = 'UTF-8'
        result = ET.fromstring(action.text)
        file_name = result.find('FileName').text

        error = False
        if file_name == "chpperror.xml":
            error = ('error', int(result.find('ErrorCode').text), result.find('Error').text, action.text)

        return error

    def decline_challenge(self, team_id, training_match_id):

        session = self.open_session()
        action = session.get(self.base_url, params={'file': 'challenges',
                                                    'version': '1.6',
                                                    'actionType': 'decline',
                                                    'teamId': str(team_id),
                                                    'trainingMatchId': str(training_match_id),
                                                    'isWeekendFriendly': '0',
                                                    })

        action.encoding = 'UTF-8'
        result = ET.fromstring(action.text)
        file_name = result.find('FileName').text

        error = None
        if file_name == "chpperror.xml":
            error = ('error', int(result.find('ErrorCode').text), result.find('Error').text, action.text)

        return error

    def withdraw_challenge(self, team_id, training_match_id):

        session = self.open_session()
        action = session.get(self.base_url, params={'file': 'challenges',
                                                    'version': '1.6',
                                                    'actionType': 'withdraw',
                                                    'teamId': str(team_id),
                                                    'trainingMatchId': str(training_match_id),
                                                    'isWeekendFriendly': '0',
                                                    })

        action.encoding = 'UTF-8'
        result = ET.fromstring(action.text)
        file_name = result.find('FileName').text

        error = None
        if file_name == "chpperror.xml":
            error = ('error', int(result.find('ErrorCode').text), result.find('Error').text, action.text)

        return error

    def get_matches_archive(self, team_id, start_date=(datetime.datetime.now() - datetime.timedelta(days=30)),
                            end_date=(datetime.datetime.now()), season=None):

        xml = self.request(
            file='matchesarchive',
            version='1.4',
            teamID=str(team_id),
            isYouth='false',
            FirstMatchDate=start_date.strftime('%Y-%m-%d %H:%M:%S'),
            LastMatchDate=end_date.strftime('%Y-%m-%d %H:%M:%S'),
            season=season,
        )

        file_name = xml.find('FileName').text

        if file_name == "chpperror.xml":
            result = ('error', int(xml.find('ErrorCode').text), xml.find('Error').text, xml.text)

        else:
            result = list()

            for m in xml.find('Team').find('MatchList').findall('Match'):
                match = {
                    'MatchID': int(m.find('MatchID').text),
                    'HomeTeamID': int(m.find('HomeTeam').find('HomeTeamID').text),
                    'HomeTeamName': m.find('HomeTeam').find('HomeTeamName').text,
                    'AwayTeamID': int(m.find('AwayTeam').find('AwayTeamID').text),
                    'AwayTeamName': m.find('AwayTeam').find('AwayTeamName').text,
                    'MatchDate': datetime.datetime.strptime(m.find('MatchDate').text, '%Y-%m-%d %H:%M:%S'),
                    'HomeGoals': int(m.find('HomeGoals').text),
                    'AwayGoals': int(m.find('AwayGoals').text),
                }

                result.append(match)

        return result

    def get_matches(self, team_id, end_date):

        xml = self.request(
            file='matches',
            version='2.8',
            teamID=str(team_id),
            isYouth='false',
            LastMatchDate=end_date.strftime('%Y-%m-%d %H:%M:%S'),
        )

        file_name = xml.find('FileName').text

        if file_name == "chpperror.xml":
            result = ('error', int(xml.find('ErrorCode').text), xml.find('Error').text, xml.text)

        else:
            result = list()

            for m in xml.find('Team').find('MatchList').findall('Match'):
                match = {
                    'MatchID': int(m.find('MatchID').text),
                    'HomeTeamID': int(m.find('HomeTeam').find('HomeTeamID').text),
                    'AwayTeamID': int(m.find('AwayTeam').find('AwayTeamID').text),
                    'MatchDate': datetime.datetime.strptime(m.find('MatchDate').text, '%Y-%m-%d %H:%M:%S'),
                }

                result.append(match)

        return result

    def get_match_details(self, match_id):

        xml = self.request(
            file='matchdetails',
            version='3.0',
            matchEvents='true',
            matchID=str(match_id),
            sourceSystem='hattrick',
        )

        file_name = xml.find('FileName').text

        if file_name == "chpperror.xml":
            result = ('error', int(xml.find('ErrorCode').text), xml.find('Error').text, xml.text)

        else:

            m = xml.find('Match')

            result = dict()

            result['MatchID'] = int(m.find('MatchID').text)
            result['MatchDate'] = datetime.datetime.strptime(m.find('MatchDate').text, '%Y-%m-%d %H:%M:%S')

            if m.find('FinishedDate') is not None:
                result['FinishedDate'] = datetime.datetime.strptime(m.find('FinishedDate').text, '%Y-%m-%d %H:%M:%S')
            else:
                result['FinishedDate'] = None

            result['HomeTeamID'] = int(m.find('HomeTeam').find('HomeTeamID').text)

            if m.find('HomeTeam').find('HomeGoals') is not None:
                result['HomeGoals'] = int(m.find('HomeTeam').find('HomeGoals').text)
            else:
                result['HomeGoals'] = None
            result['AwayTeamID'] = int(m.find('AwayTeam').find('AwayTeamID').text)

            if m.find('AwayTeam').find('AwayGoals') is not None:
                result['AwayGoals'] = int(m.find('AwayTeam').find('AwayGoals').text)
            else:
                result['AwayGoals'] = None

            result['ArenaID'] = int(m.find('Arena').find('ArenaID').text)

            # Si le match est terminé
            if result['FinishedDate'] is not None:

                goals = list()

                if m.find('Scorers') is not None:
                    for g in m.find('Scorers').findall('Goal'):
                        goal = {
                            'ScorerTeamID': int(g.find('ScorerTeamID').text),
                            'ScorerHomeGoals': int(g.find('ScorerHomeGoals').text),
                            'ScorerAwayGoals': int(g.find('ScorerAwayGoals').text),
                            'ScorerMinute': int(g.find('ScorerMinute').text),
                            'MatchPart': int(g.find('MatchPart').text),
                        }

                        goals.append(goal)

                result['Goals'] = goals

                extension = False
                penalty = False

                for e in m.find('EventList').findall('Event'):

                    if int(e.find('EventTypeID').text) == 70:
                        extension = True
                    elif int(e.find('EventTypeID').text) == 71:
                        penalty = True

                if penalty:
                    result['End'] = 2
                elif extension:
                    result['End'] = 1
                else:
                    result['End'] = 0

        return result


class HTUndefinedError(Exception):
    """Raise when error occurs with Hattrick request"""
