from rauth import OAuth1Service
from rauth import OAuth1Session
from rauth.oauth import HmacSha1Signature

import xml.etree.ElementTree as ET
import datetime

from pychpp import ht_user, ht_team, ht_player, ht_arena, ht_region
from pychpp import error


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

    # noinspection PyMethodMayBeStatic
    def _analyze_error(self, xml_data):
        """
        Parse xml data returned by Hattrick and raise relevant exception
        """
        error_code = int(xml_data.find('ErrorCode').text)

        if error_code == 59:
            raise error.HTNotOwnedTeamError('The requested team is not owned by the connected user')

        elif error_code == 70:
            error_text = xml_data.find('Error').text.split('Additional Info:')[-1].strip()

            if 'You tried to challenge yourself' in error_text:
                raise error.HTTeamChallengingItself('The team is challenging itself')

            elif error_text == 'arena busy':
                raise error.HTArenaNotAvailableError('The arena is not available')

            elif 'Your team already has booked' in error_text:
                raise error.HTTeamNotAvailableError('The own team has already booked a friendly match')

            elif error_text[-10:] == 'être défié':
                raise error.HTOpponentTeamNotAvailableError('The opponent team is not available')

            elif 'Your team is travelling' in error_text:
                raise error.HTTeamIsTravellingError('The own team is travelling'
                                                    'and can\'t launch a challenge')

            elif 'are currently abroad' in error_text:
                raise error.HTOpponentTeamIsTravellingError('The opponent team is travelling'
                                                            'and can\'t be challenged')

            elif 'Challenges have been temporarily disabled' in error_text:
                raise error.HTChallengesNotOpenedError('Challenges can\'t be launched (to soon)')

            else:
                raise error.HTChallengeError(f"Unknown Hattrick error with challenge : "
                                             f"{xml_data.find('Error').text}")

        else:
            raise error.HTUndefinedError(f"Unknown Hattrick error : "
                                         f"({error_code}) {xml_data.find('Error').text}")

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

        data = ET.fromstring(query.text)
        file_name = data.find('FileName').text

        # If Hattrick returns an error, an exception is raised
        if file_name == 'chpperror.xml':
            self._analyze_error(data)

        return data

    def user(self, **kwargs):
        return ht_user.HTUser(chpp=self, **kwargs)

    def team(self, **kwargs):
        return ht_team.HTTeam(chpp=self, **kwargs)

    def youth_team(self, **kwargs):
        return ht_team.HTYouthTeam(chpp=self, **kwargs)

    def player(self, **kwargs):
        return ht_player.HTPlayer(chpp=self, **kwargs)

    def youth_player(self, **kwargs):
        return ht_player.HTYouthPlayer(chpp=self, **kwargs)

    def arena(self, **kwargs):
        return ht_arena.HTArena(chpp=self, **kwargs)

    def region(self, **kwargs):
        return ht_region.HTRegion(chpp=self, **kwargs)

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
