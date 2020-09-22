from rauth import OAuth1Service
from rauth import OAuth1Session
from rauth.oauth import HmacSha1Signature

import xml.etree.ElementTree

from pychpp import (ht_user, ht_team, ht_player, ht_arena, ht_region,
                    ht_challenge, ht_match, ht_matches_archive,
                    ht_match_lineup, ht_league, ht_world)
from pychpp import ht_error


class CHPP:
    """
    Manage connection and requests with Hattrick API
    """

    def __init__(self, consumer_key, consumer_secret,
                 access_token_key='', access_token_secret=''):
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

        self.request_token_url = (
            "https://chpp.hattrick.org/oauth/request_token.ashx")
        self.access_token_url = (
            "https://chpp.hattrick.org/oauth/access_token.ashx")
        self.authorize_url = (
            "https://chpp.hattrick.org/oauth/authorize.aspx")
        self.base_url = (
            "https://chpp.hattrick.org/chppxml.ashx")

        self.service = OAuth1Service(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            request_token_url=self.request_token_url,
            access_token_url=self.access_token_url,
            authorize_url=self.authorize_url,
            base_url=self.base_url,
            signature_obj=HmacSha1Signature,
        )

    @staticmethod
    def _analyze_error(xml_data):
        """
        Parse xml data returned by Hattrick and raise relevant exception

        :param xml_data: xml data to analyze
        :type xml_data: xml.etree.ElementTree.Element
        """

        error_code = int(xml_data.find("ErrorCode").text)

        if error_code == 50:
            raise ht_error.HTUnknownTeamIdError(
                "The requested team id is unknown")

        elif error_code == 51:
            raise ht_error.HTUnknownMatchIdError(
                "The requested match id is unknown")

        elif error_code == 52:
            raise ht_error.HTUnknownActionTypeError(
                "The requested action is unknown")

        elif error_code == 54:
            raise ht_error.HTUnknownYouthTeamIdError(
                "The requested youth team id is unknown")

        elif error_code == 55:
            raise ht_error.HTUnknownYouthPlayerIdError(
                "The requested youth player id is unknown")

        if error_code == 56:
            raise ht_error.HTUnknownPlayerIdError(
                "The requested player id is unknown")

        elif error_code == 59:
            raise ht_error.HTNotOwnedTeamError(
                "The requested team is not owned by the connected user")

        elif error_code == 70:
            error_text = xml_data.find("Error").text.split(
                "Additional Info:")[-1].strip()

            if "You tried to challenge yourself" in error_text:
                raise ht_error.HTTeamChallengingItself(
                    "The team is challenging itself")

            elif error_text == "arena busy":
                raise ht_error.HTArenaNotAvailableError(
                    "The arena is not available")

            elif "Your team already has booked" in error_text:
                raise ht_error.HTTeamNotAvailableError(
                    "The own team has already booked a friendly match")

            elif error_text[-10:] == "être défié":
                raise ht_error.HTOpponentTeamNotAvailableError(
                    "The opponent team is not available")

            elif "Your team is travelling" in error_text:
                raise ht_error.HTTeamIsTravellingError(
                    "The own team is travelling and can't launch a challenge")

            elif "are currently abroad" in error_text:
                raise ht_error.HTOpponentTeamIsTravellingError(
                    "The opponent team is travelling and can't be challenged")

            elif "Challenges have been temporarily disabled" in error_text:
                raise ht_error.HTChallengesNotOpenedError(
                    "Challenges can't be launched (to soon)")

            else:
                raise ht_error.HTChallengeError(
                    f"Unknown Hattrick error with challenge : "
                    f"{xml_data.find('Error').text}")

        else:
            raise ht_error.HTUndefinedError(
                f"Unknown Hattrick error : "
                f"({error_code}) {xml_data.find('Error').text}")

    def get_auth(self, callback_url="oob", scope=""):
        """
        Get url, request_token and request_token_secret
        to get authentification tokens from Hattrick for this user

        :param callback_url: url that have to be request by Hattrick
                             after the user have fill his credentials
        :param scope: authorization granted by user to the application
                      can be one or more from "", "manage_challenges",
                      "set_matchorder", "manage_youthplayers",
                      "set_training", "place_bid"
        :type callback_url: str
        :type scope: str, list
        :return: {"request_token": ..., "request_token_secret":..., "url": ...}
        :rtype: dict
        """

        # Check callback_url and scope parameters integrity
        if not isinstance(callback_url, str):
            raise ValueError("callback_url must be an url or equal to 'oob'")

        # Scope can be a string (no or one scope)
        # or a list (one or more scopes)
        if isinstance(scope, str):
            if scope not in ("", "manage_challenges", "set_matchorder",
                             "manage_youthplayers",
                             "set_training", "place_bid"):
                raise ValueError(
                    "As scope is a string, it must be empty "
                    "or equal to 'manage_challenges', 'set_matchorder', "
                    "'manage_youthplayers','set_training' or 'place_bid'")

        elif isinstance(scope, list):
            if not set(scope) <= {"manage_challenges", "set_matchorder",
                                  "manage_youthplayers",
                                  "set_training", "place_bid"}:
                raise ValueError(
                    "As scope is a list, its items must be equal to "
                    "'manage_challenges', 'set_matchorder', "
                    "'manage_youthplayers','set_training' or 'place_bid'")

            # If scope is a list and its items are correct,
            # it is converted into a string
            else:
                scope = ",".join(scope)

        else:
            raise ValueError("Scope parameter must be a string a or list")

        auth = dict()

        request_token, request_token_secret = (
            self.service.get_request_token(
                params={"oauth_callback": callback_url}))

        auth["request_token"] = request_token
        auth["request_token_secret"] = request_token_secret
        auth["url"] = (
            self.service.get_authorize_url(request_token, scope=scope))

        return auth

    def get_access_token(self, request_token, request_token_secret, code):
        """
        Query access token from Hattrick
        once the user granted the application on Hattrick

        Access token have to be stored by the application
        in order to be used for further use of CHPP class.

        :param request_token: returned by get_auth
        :param request_token_secret: returned by get_auth
        :param code: code returned by Hattrick
                     after the user granted the application
                     send to callback_url by Hattrick
                     or shown direclty on Hattrick if callback_url was ""
        :return: {"key": ..., "secret": ...}
        """
        if not isinstance(request_token, str):
            raise ValueError("request_token must be a string")
        elif not isinstance(request_token_secret, str):
            raise ValueError("request_token_secret must be a string")
        elif not isinstance(code, str):
            raise ValueError("code must be a string")

        access_token_query = (
            self.service.get_access_token(request_token,
                                          request_token_secret,
                                          params={"oauth_verifier": code},
                                          ))

        access_token = dict()

        access_token["key"] = access_token_query[0]
        access_token["secret"] = access_token_query[1]

        return access_token

    def open_session(self):
        """
        Open OAuth session
        """
        return OAuth1Session(self.consumer_key,
                             self.consumer_secret,
                             access_token=self.access_token_key,
                             access_token_secret=self.access_token_secret,
                             )

    def request(self, **kwargs):
        """
        Send a request via the CHPP API

        :return: xml data fetched on Hattrick
        :rtype: xml.etree.ElementTree
        """
        session = self.open_session()
        query = session.get(self.base_url, params=kwargs)
        query.encoding = "UTF-8"

        if query.status_code == 401:
            raise ht_error.HTUnauthorizedAction(
                "The requested action seems to be unauthorized "
                "(401 error code). Please heck your credentials scope.")

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

        If not ht_id is defined,
        return the youth primary team of connected user.

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

        If not ht_id is defined,
        return the primary team arena of connected user.

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
        """
                Get a challenge manager object

                :key team_ht_id: Hattrick ID of the concerned team,
                                 must be an int
                :key period: concerned period,
                             must be equal to 'week' or 'weekend'
                :rtype: ht_challenge.HTChallengeManager
                """
        return ht_challenge.HTChallengeManager(chpp=self, **kwargs)

    def match(self, **kwargs):
        """
        Get a match from his Hattrick ID

        :key ht_id: Hattrick ID of the requested match, must be an int
        :rtype: ht_match.HTMatch
        """
        return ht_match.HTMatch(chpp=self, **kwargs)

    def matches_archive(self, **kwargs):
        """
        Get a matches archive

        :key ht_id: Hattrick ID of team to search matches
        :key youth: is requested mathes archive concerns a youth team,
                    must be a boolean
        :key first_match_date: begin date to search matches,
                               must be a datetime.datetime object
        :key last_match_date: end date to search matches,
                              must be a datetime.datetime object
        :key season: season to search matches, must be an integer
        :key hto: including or not tounaments matches, must be a boolean
        :return: a ht_matches_archive.HTMatchesArchive object
        :rtype: ht_matches_archive.HTMatchesArchive
        """
        return ht_matches_archive.HTMatchesArchive(chpp=self, **kwargs)

    def league(self, **kwargs):
        """
        Get a league from his Hattrick ID

        :key ht_id: Hattrick ID of the requested league, must be an int
        :rtype: ht_league.HTLeague
        """
        return ht_league.HTLeague(chpp=self, **kwargs)

    def match_lineup(self, **kwargs):
        """
        Get a match lineup from its Hattrick ID

        :key ht_id: Hattrick ID of the requested match, must be an int
        :key team_id: Hattrick ID of the team for each the lineup is requested,
        must be an int
        :rtype: ht_match_lineup.HTMatchLineup
        """
        return ht_match_lineup.HTMatchLineup(chpp=self, **kwargs)

    def world(self, **kwargs):
        """
        Get a world details

        :key ht_id: Hattrick ID of the requested country league,
        must be an int (optional)
        :key include_regions: Whether or not to include regions
        for the countries, must be an bool (optional, default=False)
        :rtype: ht_world.HTWorld
        """
        return ht_world.HTWorld(chpp=self, **kwargs)
