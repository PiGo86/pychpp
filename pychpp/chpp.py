from rauth import OAuth1Service
from rauth import OAuth1Session
from rauth.oauth import HmacSha1Signature

import xml.etree.ElementTree
import datetime

from pychpp import ht_user, ht_team, ht_player, ht_arena, ht_region, ht_challenge, ht_match, ht_matches_archive
from pychpp import ht_error


class CHPP:
    """
    Manage connection and requests with Hattrick API
    """

    def __init__(self, consumer_key, consumer_secret, access_token_key='', access_token_secret=''):
        """
        Initialization of a CHPP instance

        It needs at least consumer_key and consumer_secret parameters.

        If access_token_key and access_token_secret parameters are not defined,
        the instanciated object can be used to obtain them from Hattrick.

        :param consumer_key: Consumer Key of the application
        :param consumer_secret: Consumer Secret of the application
        :param access_token_key: Access Token Key for the current user
        :param access_token_secret: Access Token Secret for the current user
        :type consumer_key: str
        :type consumer_secret: str
        :type access_token_key: str
        :type access_token_secret: str
        :return: None
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret

        self.request_token_url = "https://chpp.hattrick.org/oauth/request_token.ashx"
        self.access_token_url = "https://chpp.hattrick.org/oauth/access_token.ashx"
        self.authorize_url = "https://chpp.hattrick.org/oauth/authorize.aspx"
        self.base_url = "https://chpp.hattrick.org/chppxml.ashx"

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

        error_code = int(xml_data.find("ErrorCode").text)

        if error_code == 59:
            raise ht_error.HTNotOwnedTeamError("The requested team is not owned by the connected user")

        elif error_code == 70:
            error_text = xml_data.find("Error").text.split("Additional Info:")[-1].strip()

            if "You tried to challenge yourself" in error_text:
                raise ht_error.HTTeamChallengingItself("The team is challenging itself")

            elif error_text == "arena busy":
                raise ht_error.HTArenaNotAvailableError("The arena is not available")

            elif "Your team already has booked" in error_text:
                raise ht_error.HTTeamNotAvailableError("The own team has already booked a friendly match")

            elif error_text[-10:] == "être défié":
                raise ht_error.HTOpponentTeamNotAvailableError("The opponent team is not available")

            elif "Your team is travelling" in error_text:
                raise ht_error.HTTeamIsTravellingError("The own team is travelling"
                                                       "and can't launch a challenge")

            elif "are currently abroad" in error_text:
                raise ht_error.HTOpponentTeamIsTravellingError("The opponent team is travelling"
                                                               "and can't be challenged")

            elif "Challenges have been temporarily disabled" in error_text:
                raise ht_error.HTChallengesNotOpenedError("Challenges can't be launched (to soon)")

            else:
                raise ht_error.HTChallengeError(f"Unknown Hattrick error with challenge : "
                                                f"{xml_data.find('Error').text}")

        else:
            raise ht_error.HTUndefinedError(f"Unknown Hattrick error : "
                                            f"({error_code}) {xml_data.find('Error').text}")

    def get_auth(self, callback_url="oob", scope=""):
        """
        Get url, request_token and request_token_secret to get authentification tokens from Hattrick for this user

        :param callback_url: url that have to be request by Hattrick after the user have fill his credentials
        :param scope: authorization granted by user to the application
                      can be "", "manage_challenges", "set_matchorder", "manage_youthplayers",
                      "set_training", "place_bid"
        :type callback_url: str
        :type scope: str
        :return: {"request_token": ..., "request_token_secret":..., "url": ...}
        :rtype: dict
        """
        auth = dict()

        request_token, request_token_secret = self.service.get_request_token(params={"oauth_callback": callback_url})

        auth["request_token"] = request_token
        auth["request_token_secret"] = request_token_secret
        auth["url"] = self.service.get_authorize_url(request_token, scope=scope)

        return auth

    def get_access_token(self, request_token, request_token_secret, code):
        """
        Query access token from Hattrick once the user granted the application on Hattrick

        Access token have to be stored by the application in order to be used for further use of CHPP class.

        :param request_token: returned by get_auth
        :param request_token_secret: returned by get_auth
        :param code: code returned by Hattrick after the user granted the application
                     send to callback_url by Hattrick or shown direclty on Hattrick if callback_url was ""
        :return: {"key": ..., "secret": ...}
        """
        access_token_query = self.service.get_access_token(request_token,
                                                           request_token_secret,
                                                           params={"oauth_verifier": code},
                                                           )

        access_token = dict()

        access_token["key"] = access_token_query[0]
        access_token["secret"] = access_token_query[1]

        return access_token

    def open_session(self):
        return OAuth1Session(self.consumer_key,
                             self.consumer_secret,
                             access_token=self.access_token_key,
                             access_token_secret=self.access_token_secret,
                             )

    def request(self, **kwargs):
        """
        Send a request via the CHPP API

        :return: xml data fetched on Hattrick
        :rtype: ElementTree
        """
        session = self.open_session()
        query = session.get(self.base_url, params=kwargs)
        query.encoding = "UTF-8"

        data = xml.etree.ElementTree.fromstring(query.text)
        file_name = data.find("FileName").text

        # If Hattrick returns an error, an exception is raised
        if file_name == "chpperror.xml":
            self._analyze_error(data)

        return data

    def user(self, **kwargs):
        """
        Get a user from its Hattrick ID

        If not ht_id is defined, return the connected user.

        :key ht_id: Hattrick ID of the requested user, must be an int
        :rtype: ht_user.HTUser
        """
        return ht_user.HTUser(chpp=self, **kwargs)

    def team(self, **kwargs):
        """
        Get a team from its Hattrick ID

        If not ht_id is defined, return the primary team of connected user.

        :key ht_id: Hattrick ID of the requested team, must be an int
        :rtype: ht_team.HTTeam
        """
        return ht_team.HTTeam(chpp=self, **kwargs)

    def youth_team(self, **kwargs):
        """
        Get a youth team from its Hattrick ID

        If not ht_id is defined, return the youth primary team of connected user.

        :key ht_id: Hattrick ID of the requested youth team, must be an int
        :rtype: ht_team.HTYouthTeam
        """
        return ht_team.HTYouthTeam(chpp=self, **kwargs)

    def player(self, **kwargs):
        """
        Get a player from its Hattrick ID

        :key ht_id: Hattrick ID of the requested player, must be an int
        :rtype: ht_player.HTPlayer
        """
        return ht_player.HTPlayer(chpp=self, **kwargs)

    def youth_player(self, **kwargs):
        """
        Get a youth player from its Hattrick ID

        :key ht_id: Hattrick ID of the requested youth player, must be an int
        :rtype: ht_player.HTYouthPlayer
        """
        return ht_player.HTYouthPlayer(chpp=self, **kwargs)

    def arena(self, **kwargs):
        """
        Get an arena from its Hattrick ID

        If not ht_id is defined, return the primary team arena of connected user.

        :key ht_id: Hattrick ID of the requested arena, must be an int
        :rtype: ht_arena.HTArena
        """
        return ht_arena.HTArena(chpp=self, **kwargs)

    def region(self, **kwargs):
        """
        Get a region from his Hattrick ID

        :key ht_id: Hattrick ID of the requested region, must be an int
        :rtype: ht_region.HTRegion
        """
        return ht_region.HTRegion(chpp=self, **kwargs)

    def challenge_manager(self, **kwargs):
        return ht_challenge.HTChallengeManager(chpp=self, **kwargs)

    def match(self, **kwargs):
        return ht_match.HTMatch(chpp=self, **kwargs)

    def matches_archive(self, **kwargs):
        return ht_matches_archive.HTMatchesArchive(chpp=self, **kwargs)

    def get_matches_archive(self, team_id, start_date=(datetime.datetime.now() - datetime.timedelta(days=30)),
                            end_date=(datetime.datetime.now()), season=None):

        _xml = self.request(
            file="matchesarchive",
            version="1.4",
            teamID=str(team_id),
            isYouth="false",
            FirstMatchDate=start_date.strftime("%Y-%m-%d %H:%M:%S"),
            LastMatchDate=end_date.strftime("%Y-%m-%d %H:%M:%S"),
            season=season,
        )

        file_name = _xml.find("FileName").text

        if file_name == "chpperror.xml":
            result = ("error", int(_xml.find("ErrorCode").text), _xml.find("Error").text, _xml.text)

        else:
            result = list()

            for m in _xml.find("Team").find("MatchList").findall("Match"):
                match = {
                    "MatchID": int(m.find("MatchID").text),
                    "HomeTeamID": int(m.find("HomeTeam").find("HomeTeamID").text),
                    "HomeTeamName": m.find("HomeTeam").find("HomeTeamName").text,
                    "AwayTeamID": int(m.find("AwayTeam").find("AwayTeamID").text),
                    "AwayTeamName": m.find("AwayTeam").find("AwayTeamName").text,
                    "MatchDate": datetime.datetime.strptime(m.find("MatchDate").text, "%Y-%m-%d %H:%M:%S"),
                    "HomeGoals": int(m.find("HomeGoals").text),
                    "AwayGoals": int(m.find("AwayGoals").text),
                }

                result.append(match)

        return result

    def get_matches(self, team_id, end_date):

        _xml = self.request(
            file="matches",
            version="2.8",
            teamID=str(team_id),
            isYouth="false",
            LastMatchDate=end_date.strftime("%Y-%m-%d %H:%M:%S"),
        )

        file_name = _xml.find("FileName").text

        if file_name == "chpperror.xml":
            result = ("error", int(_xml.find("ErrorCode").text), _xml.find("Error").text, _xml.text)

        else:
            result = list()

            for m in _xml.find("Team").find("MatchList").findall("Match"):
                match = {
                    "MatchID": int(m.find("MatchID").text),
                    "HomeTeamID": int(m.find("HomeTeam").find("HomeTeamID").text),
                    "AwayTeamID": int(m.find("AwayTeam").find("AwayTeamID").text),
                    "MatchDate": datetime.datetime.strptime(m.find("MatchDate").text, "%Y-%m-%d %H:%M:%S"),
                }

                result.append(match)

        return result

    def get_match_details(self, match_id):

        _xml = self.request(
            file="matchdetails",
            version="3.0",
            matchEvents="true",
            matchID=str(match_id),
            sourceSystem="hattrick",
        )

        file_name = _xml.find("FileName").text

        if file_name == "chpperror.xml":
            result = ("error", int(_xml.find("ErrorCode").text), _xml.find("Error").text, _xml.text)

        else:

            m = _xml.find("Match")

            result = dict()

            result["MatchID"] = int(m.find("MatchID").text)
            result["MatchDate"] = datetime.datetime.strptime(m.find("MatchDate").text, "%Y-%m-%d %H:%M:%S")

            if m.find("FinishedDate") is not None:
                result["FinishedDate"] = datetime.datetime.strptime(m.find("FinishedDate").text, "%Y-%m-%d %H:%M:%S")
            else:
                result["FinishedDate"] = None

            result["HomeTeamID"] = int(m.find("HomeTeam").find("HomeTeamID").text)

            if m.find("HomeTeam").find("HomeGoals") is not None:
                result["HomeGoals"] = int(m.find("HomeTeam").find("HomeGoals").text)
            else:
                result["HomeGoals"] = None
            result["AwayTeamID"] = int(m.find("AwayTeam").find("AwayTeamID").text)

            if m.find("AwayTeam").find("AwayGoals") is not None:
                result["AwayGoals"] = int(m.find("AwayTeam").find("AwayGoals").text)
            else:
                result["AwayGoals"] = None

            result["ArenaID"] = int(m.find("Arena").find("ArenaID").text)

            # Si le match est terminé
            if result["FinishedDate"] is not None:

                goals = list()

                if m.find("Scorers") is not None:
                    for g in m.find("Scorers").findall("Goal"):
                        goal = {
                            "ScorerTeamID": int(g.find("ScorerTeamID").text),
                            "ScorerHomeGoals": int(g.find("ScorerHomeGoals").text),
                            "ScorerAwayGoals": int(g.find("ScorerAwayGoals").text),
                            "ScorerMinute": int(g.find("ScorerMinute").text),
                            "MatchPart": int(g.find("MatchPart").text),
                        }

                        goals.append(goal)

                result["Goals"] = goals

                extension = False
                penalty = False

                for e in m.find("EventList").findall("Event"):

                    if int(e.find("EventTypeID").text) == 70:
                        extension = True
                    elif int(e.find("EventTypeID").text) == 71:
                        penalty = True

                if penalty:
                    result["End"] = 2
                elif extension:
                    result["End"] = 1
                else:
                    result["End"] = 0

        return result


class HTUndefinedError(Exception):
    """Raise when error occurs with Hattrick request"""
