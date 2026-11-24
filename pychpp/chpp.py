"""Client for the Hattrick CHPP API."""

from datetime import datetime
from http.client import RemoteDisconnected
from typing import Literal, Optional, overload

import xml.etree.ElementTree

from requests.adapters import HTTPAdapter
from requests_oauthlib import OAuth1Session
from urllib3 import Retry

from pychpp.models.xml import (manager_compendium, team_details, team_history, achievements,
                               arena_details,
                               challenges, region_details, league_details, league_fixtures,
                               match_lineup, national_teams, national_team_details, player_details,
                               training, transfers_team, world_details, world_cup, players,
                               youth_player_details, youth_team_details, youth_player_list,
                               matches_archive, match_details, cup_matches, alliances,
                               alliance_details, avatars, bookmarks, club, current_bids, economy,
                               fans, hof_players, ladder_details, ladder_list, league_levels, live,
                               matches, match_orders, national_team_matches, national_players,
                               national_prospect_players, player_events, player_stats, search,
                               staff_avatars, staff_list, supporters,
                               tournament_details, tournament_fixtures, tournament_league_tables,
                               tournament_list, training_events, transfer_search, transfers_player,
                               world_languages, youth_avatars, youth_league_details,
                               youth_league_fixtures, translations)
from pychpp.models.custom import (ht_team, ht_arena, ht_user, ht_region, ht_youth_team, ht_player,
                                  ht_league_unit, ht_youth_player, ht_league, ht_matches_archive,
                                  ht_match, ht_challenge, ht_match_lineup, ht_transfer_history)
from pychpp.fixtures import ht_error
from pychpp.models.ht_xml import HTXml


class CHPPBase:
    """Manage the connection and the requests with the Hattrick CHPP API.

    Args:
        consumer_key: Consumer key of the application.
        consumer_secret: Consumer secret of the application.
        access_token_key: Access token key for the current user. If not defined,
            the instance can be used to obtain tokens from Hattrick.
        access_token_secret: Access token secret for the current user.

    """

    def __init__(self,
                 consumer_key: str,
                 consumer_secret: str,
                 access_token_key: Optional[str] = None,
                 access_token_secret: Optional[str] = None,
                 ):
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
        self.check_token_url = (
            "https://chpp.hattrick.org/oauth/check_token.ashx")
        self.invalidate_token_url = (
            "https://chpp.hattrick.org/oauth/invalidate_token.ashx")

        self.session = None

    @staticmethod
    def _analyze_error(xml_data):
        """Parse XML data returned by Hattrick and raise the relevant exception.

        Args:
            xml_data: Xml data to analyze.

        Raises:
            ht_error.HTError: The relevant CHPP error exception, depending on the
                error code returned by Hattrick.

        """
        error_code = int(xml_data.findtext("ErrorCode", "0"))
        error_text = xml_data.findtext("Error", "")

        if error_code == 1:
            raise ht_error.HTAccessDeniedError(
                "Access to specified parameters or file was denied : "
                + error_text)

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
            error_info = error_text.split("Additional Info:")[-1].strip()

            if "You tried to challenge yourself" in error_info:
                raise ht_error.HTTeamChallengingItself(
                    "The team is challenging itself")

            elif error_info == "arena busy":
                raise ht_error.HTArenaNotAvailableError(
                    "The arena is not available")

            elif "Your team already has booked" in error_info:
                raise ht_error.HTTeamNotAvailableError(
                    "The own team has already booked a friendly match")

            elif "Your team is still in the cup" in error_info:
                raise ht_error.HTTeamNotAvailableError(
                    "The own team is still in cup")

            elif error_info[-10:] == "être défié":
                raise ht_error.HTOpponentTeamNotAvailableError(
                    "The opponent team is not available")

            elif "Your team is travelling" in error_info:
                raise ht_error.HTTeamIsTravellingError(
                    "The own team is travelling and can't launch a challenge")

            elif "are currently abroad" in error_info:
                raise ht_error.HTOpponentTeamIsTravellingError(
                    "The opponent team is travelling and can't be challenged")

            elif "Challenges have been temporarily disabled" in error_info:
                raise ht_error.HTChallengesNotOpenedError(
                    "Challenges can't be launched (to soon)")

            else:
                raise ht_error.HTChallengeError(
                    f"Unknown Hattrick error with challenge : "
                    f"{error_text}")

        else:
            raise ht_error.HTUndefinedError(
                f"Unknown Hattrick error : "
                f"({error_code}) {error_text}")

    def get_auth(self, callback_url="oob", scope: str | list = ""):
        """Get the url, request_token and request_token_secret to authenticate a user.

        Args:
            callback_url: Url that has to be requested by Hattrick after the user
                has entered their credentials.
            scope: Authorization granted by the user to the application. Can be one
                or more of "", "manage_challenges", "set_matchorder",
                "manage_youthplayers", "set_training", "place_bid".

        Returns:
            A dict with "request_token", "request_token_secret" and "url" keys.

        Raises:
            ValueError: If callback_url or scope is invalid.

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

        oauth = OAuth1Session(client_key=self.consumer_key,
                              client_secret=self.consumer_secret,
                              callback_uri=callback_url,
                              )
        auth = oauth.fetch_request_token(self.request_token_url)
        auth["url"] = oauth.authorization_url(self.authorize_url, scope=scope)

        return auth

    def get_access_token(self, request_token, request_token_secret, code):
        """Query the access token from Hattrick once the user granted the application.

        The access token has to be stored by the application
        in order to be used for further use of the CHPP class.

        Args:
            request_token: Request token returned by `get_auth()`.
            request_token_secret: Request token secret returned by `get_auth()`.
            code: Code returned by Hattrick after the user granted the application,
                sent to callback_url by Hattrick or shown directly on Hattrick
                if callback_url was "oob".

        Returns:
            A dict with "key" and "secret" keys.

        Raises:
            ValueError: If request_token, request_token_secret or code is not a string.

        """
        if not isinstance(request_token, str):
            raise ValueError("request_token must be a string")
        elif not isinstance(request_token_secret, str):
            raise ValueError("request_token_secret must be a string")
        elif not isinstance(code, str):
            raise ValueError("code must be a string")

        oauth = OAuth1Session(client_key=self.consumer_key,
                              client_secret=self.consumer_secret,
                              resource_owner_key=request_token,
                              resource_owner_secret=request_token_secret,
                              verifier=code,
                              )

        tokens = oauth.fetch_access_token(self.access_token_url)

        return dict(key=tokens['oauth_token'], secret=tokens['oauth_token_secret'])

    def open_session(self):
        """Open the OAuth session."""
        self.session = OAuth1Session(client_key=self.consumer_key,
                                     client_secret=self.consumer_secret,
                                     resource_owner_key=self.access_token_key,
                                     resource_owner_secret=self.access_token_secret,
                                     )

        # retry strategy
        retry_strategy = Retry(
            total=5,
            redirect=5,
            backoff_factor=0.5,
        )

        self.session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    @overload
    def _base_request(
            self, url, parse_data: Literal[True] = ..., method: str = ...,
            **kwargs,
    ) -> xml.etree.ElementTree.Element: ...

    @overload
    def _base_request(
            self, url, parse_data: Literal[False], method: str = ...,
            **kwargs,
    ) -> str: ...

    def _base_request(
            self, url, parse_data=True, method='GET', **kwargs,
    ) -> xml.etree.ElementTree.Element | str:
        """Send a request via the CHPP API.

        Args:
            url: Url to fetch.
            parse_data: Whether to parse the returned data as XML.
            method: HTTP method to use ('GET' or 'POST').
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The XML data fetched on Hattrick.

        """

        def proceed_request():
            if method == 'GET':
                return self.session.get(url, params=kwargs)
            elif method == 'POST':
                return self.session.post(url, data=kwargs)
            else:
                raise ValueError(f"Unknown method '{method}'")

        if self.session is None:
            self.open_session()

        try:
            query = proceed_request()

        except RemoteDisconnected:
            self.open_session()
            query = proceed_request()

        query.encoding = "UTF-8"
        self.last_url = query.url

        if query.status_code == 401:
            raise ht_error.HTUnauthorizedAction(
                "The requested action seems to be unauthorized "
                "(401 error code). Please check your credentials scope.")

        if not parse_data:
            return query.text

        else:
            data = xml.etree.ElementTree.fromstring(query.text)
            file_name = data.findtext("FileName")

            # If Hattrick returns an error, an exception is raised
            if file_name == "chpperror.xml":
                self._analyze_error(data)

            return data

    def check_token(self):
        """Check the token key and secret validity.

        Returns:
            Validity and other information about the current token.

        """
        data = None
        token_is_valid = None

        try:
            data = self._base_request(url=self.check_token_url,
                                      parse_data=True)

        except ht_error.HTUnauthorizedAction:
            token_is_valid = False

        else:
            token_is_valid = True

        finally:
            token_data = {
                "is_valid": token_is_valid,
                "user_id": None,
                "fetched_date": None,
                "key": None,
                "created_date": None,
            }

            if data is not None:
                token_data["user_id"] = HTXml.ht_int(data.find("UserID"))
                token_data["fetched_date"] = HTXml.ht_datetime_from_text(
                    data.find("FetchedDate"))
                token_data["key"] = HTXml.ht_str(data.find("Token"))
                token_data["created_date"] = HTXml.ht_datetime_from_text(
                    data.find("Created"))

            return token_data

    def invalidate_token(self):
        """Invalidate the current token.

        Returns:
            Information about the invalidated token.

        """
        try:
            return self._base_request(url=self.invalidate_token_url,
                                      parse_data=False)
        except ht_error.HTUnauthorizedAction:
            return "token is already invalid"

    def request(self, **kwargs) -> xml.etree.ElementTree.Element:
        """Send a request to the CHPP API endpoint.

        Args:
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed XML data fetched on Hattrick.

        Raises:
            ht_error.HTError: If the CHPP API returns an error.

        """
        return self._base_request(url=self.base_url, parse_data=True, **kwargs)


class CHPPXml(CHPPBase):
    """Wrapper exposing one method per CHPP XML file.

    Each `xml_<file>()` method fetches and parses the corresponding
    `<file>.xml` file from the Hattrick CHPP API. If Hattrick returns an
    error, a `ht_error.HTError` subclass is raised.

    """

    def xml_achievements(
        self, user_id: Optional[int] = None, **kwargs,
    ) -> achievements.Achievements:
        """Request the `achievements.xml` file from the CHPP API.

        Args:
            user_id: Which user to show achievements for. If `None` (the default), Hattrick uses
                the authenticated user's ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `achievements.xml` file.

        """
        return achievements.Achievements(chpp=self, user_id=user_id, **kwargs)

    def xml_alliances(
            self,
            search_for: str,
            search_type: Optional[int] = None,
            search_language_id: Optional[int] = None,
            page_index: Optional[int] = None,
            user_id: Optional[int] = None,
            **kwargs,
    ) -> alliances.Alliances:
        """Request the `alliances.xml` file from the CHPP API.

        Args:
            search_for: What to search for (length ≥ 3 characters).
            search_type: Which field to search in. Allowed values: '1' (Let the list include only
                         federations with names beginning with search string), '2' (Let the list
                         include only federations with abbreviation including search string), '3'
                         (Let the list include only federations with description including search
                         string), '4' (Search for a specific AllianceID), '5' (Get the federations
                         of the currently authenticated manager, or of another user).
            search_language_id: Specifies a language to restrict the federations on the list to.
                If `None` (the default), Hattrick uses 0 (all languages).
            page_index: Zero based pageindex to retrieve. If the search result spans more than one
                page, the total number of pages is returned. Each result may not return more than
                25 rows. If `None` (the default), Hattrick uses 0.
            user_id: The user to show the federations for. Gives AccessDenied if the user does not
                exist or has no team. If `None` (the default), Hattrick uses the authenticated
                    user's ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `alliances.xml` file.

        """
        return alliances.Alliances(
            chpp=self,
            search_type=search_type,
            search_for=search_for,
            search_language_id=search_language_id,
            page_index=page_index,
            user_id=user_id,
            **kwargs,
        )

    def xml_alliance_details(
            self,
            action_type: str = 'view',
            subset: Optional[int] = None,
            alliance_id: Optional[int] = None,
            **kwargs,
    ) -> (alliance_details.AllianceDetailsView
          | alliance_details.AllianceDetailsRoles
          | alliance_details.AllianceDetailsMembers
          | alliance_details.AllianceDetailsMembersSubset):
        """Request the `alliance_details.xml` file from the CHPP API.

        Args:
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'view' (Federation info), 'roles' (View the roles of a federation),
                         'members' (List the members of a federation), 'membersSubset' (List a
                         subset of the members of a federation).
            subset: Starting character names to show A = 65.... Z = 90. Use 0 for other than
                    english starting characters. Only relevant for actionType membersSubset.
            alliance_id: ID of the federation to search information for.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `alliance_details.xml` file.

        """
        if action_type == 'view':
            return alliance_details.AllianceDetailsView(
                chpp=self,
                action_type=action_type,
                alliance_id=alliance_id,
                **kwargs,
            )

        elif action_type == 'roles':
            return alliance_details.AllianceDetailsRoles(
                chpp=self,
                action_type=action_type,
                alliance_id=alliance_id,
                **kwargs,
            )

        elif action_type == 'members':
            return alliance_details.AllianceDetailsMembers(
                chpp=self,
                action_type=action_type,
                alliance_id=alliance_id,
                **kwargs,
            )

        elif action_type == 'membersSubset':
            return alliance_details.AllianceDetailsMembersSubset(
                chpp=self,
                action_type=action_type,
                subset=subset,
                alliance_id=alliance_id,
                **kwargs,
            )

        else:
            raise ValueError("'action_type' argument must be "
                       "equal to 'view', 'roles', "
                       "'members' or 'membersSubset'")

    def xml_arena_details(
            self,
            stats_type: Optional[str] = None,
            arena_id: Optional[int] = None,
            team_id: Optional[int] = None,
            match_type: Optional[str] = None, first_date: Optional[datetime] = None,
            last_date: Optional[datetime] = None, stats_league_id: Optional[int] = None,
    ) -> (arena_details.ArenaDetailsDefault
          | arena_details.ArenaDetailsMyArena
          | arena_details.ArenaDetailsLeagueArenaStats):
        """Request the `arena_details.xml` file from the CHPP API.

        Args:
            stats_type: Statistics type to show. Allowed values: '(empty)' (Default view),
                        'MyArena' (Show supporter statistics for the users own arena),
                        'OtherArenas' (Shows supporter statistics over biggest arenas).
            arena_id: Which arena to show details for. If `None` (the default), Hattrick uses the
                authenticated user's arena ID, if no team ID is supplied.
            team_id: Which of the authenticated user's teams' arenas to show details for, only
                used when no arena ID is supplied. If `None` (the default), Hattrick uses the
                authenticated user's primary team's ID.
            match_type: Which type of matches that will be included in the statistics. If `None`
                (the default), Hattrick uses All.
            first_date: The first date the statistics should cover. If `None` (the default),
                Hattrick uses Date of first match in arena.
            last_date: The last date the statistics should cover. If `None` (the default),
                Hattrick uses DateTime.Now.
            stats_league_id: Which league to show statistics for. 0 = global statistic. Defaults
                to 0.

        Returns:
            The parsed data from the `arena_details.xml` file.

        """
        if stats_type is None:
            return arena_details.ArenaDetailsDefault(
                chpp=self, stats_type=stats_type, arena_id=arena_id, team_id=team_id,
            )

        elif stats_type == 'MyArena':
            return arena_details.ArenaDetailsMyArena(
                chpp=self, stats_type=stats_type, arena_id=arena_id, team_id=team_id,
                match_type=match_type, first_date=first_date, last_date=last_date,
            )

        elif stats_type == 'OtherArenas':
            return arena_details.ArenaDetailsLeagueArenaStats(
                chpp=self, stats_league_id=stats_league_id,
            )

        else:
            raise ValueError("'stats_type' argument must be None, "
                             "or equal to 'MyArena' or 'OtherArenas'")

    def xml_avatars(
            self,
            action_type: Optional[str] = None,
            team_id: Optional[int] = None,
            **kwargs,
    ) -> avatars.Avatars:
        """Request the `avatars.xml` file from the CHPP API.

        Args:
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'players' (View the avatars of players for the team of the
                         currently authenticated user), 'hof' (View the avatars of Hall of
                         Fame players for the team of the currently authenticated user).
            team_id: What team/user to show the avatars for. If `None` (the default), Hattrick
                uses the authenticated user's senior team ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `avatars.xml` file.

        """
        return avatars.Avatars(
            chpp=self,
            action_type=action_type,
            team_id=team_id,
            **kwargs,
        )

    def xml_bookmarks(
            self, bookmark_type_id: Optional[int] = None,
            **kwargs,
    ) -> bookmarks.Bookmarks:
        """Request the `bookmarks.xml` file from the CHPP API.

        Args:
            bookmark_type_id: Bookmark Type.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `bookmarks.xml` file.

        """
        return bookmarks.Bookmarks(
            chpp=self,
            bookmark_type_id=bookmark_type_id,
            **kwargs,
        )

    def xml_challenges(
            self, action_type: str = 'view', team_id: Optional[int] = None,
            is_weekend_friendly: int = 0, suggested_team_ids: Optional[str] = None,
            opponent_team_id: Optional[int] = None, match_type: Optional[int] = None,
            match_place: Optional[int] = None, neutral_arena_id: Optional[int] = None,
            training_match_id: Optional[int] = None, **kwargs,
    ) -> (challenges.ChallengesView
          | challenges.ChallengesChallengeable
          | challenges.ChallengesChallenge
          | challenges.ChallengesAccept
          | challenges.ChallengesDecline
          | challenges.ChallengesWithdraw):
        """Request the `challenges.xml` file from the CHPP API.

        Args:
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'view' (Returns data on the challenges made by the authenticated
                         user and the offers received), 'challengeable' (Check if it is
                         possible to challenge the teams specified in parameter
                         suggestedTeamIDs), 'challenge'
                         (Challenge an opponent to a friendly match. (Requires
                         "manage_challenges" scope.)), 'accept' (Accept a challenge from an
                         opponent. (Requires "manage_challenges" scope.)), 'decline' (Decline
                         a challenge from an opponent. (Requires "manage_challenges" scope.)),
                         'withdraw' (Withdraw a not yet accepted challenge. (Requires
                         "manage_challenges" scope.)).
            team_id: Team ID to manage challenges for. Must refer to a senior team managed by
                requesting user. If `None` (the default), Hattrick uses the authenticated user's
                primary team ID.
            is_weekend_friendly: Show weekend Friendly match and use it to set data for weekend
                                 friendly. Defaults to 0.
            suggested_team_ids: A comma-separated list of teamID numbers for the teams to check the
                                challengeable status for.
            opponent_team_id: The ID of the team to challenge.
            match_type: Specifies whether to challenge for a normal friendly (0) or a friendly
                with cup rules (1). If `None` (the default), Hattrick uses 0.
            match_place: Defines if challenger wants to play home (0), away (1) or on a neutral
                arena (2). If `None` (the default), Hattrick uses 0.
            neutral_arena_id: ArenaID for arena where friendly on neutral ground should be played.
                If `None` (the default), Hattrick uses 0.
            training_match_id: Specifies the training match ID for the friendly offer to accept.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `challenges.xml` file.

        """
        if action_type == 'view':
            return challenges.ChallengesView(
                chpp=self, action_type=action_type, team_id=team_id,
                is_weekend_friendly=is_weekend_friendly, **kwargs,
            )

        elif action_type == 'challengeable':
            return challenges.ChallengesChallengeable(
                chpp=self, action_type=action_type, team_id=team_id,
                is_weekend_friendly=is_weekend_friendly,
                suggested_team_ids=suggested_team_ids, **kwargs,
            )

        elif action_type == 'challenge':
            return challenges.ChallengesChallenge(
                chpp=self, action_type=action_type, team_id=team_id,
                is_weekend_friendly=is_weekend_friendly, opponent_team_id=opponent_team_id,
                match_type=match_type, match_place=match_place, neutral_arena_id=neutral_arena_id,
                **kwargs,
            )

        elif action_type == 'accept':
            return challenges.ChallengesAccept(
                chpp=self, action_type=action_type, team_id=team_id,
                is_weekend_friendly=is_weekend_friendly, training_match_id=training_match_id,
                **kwargs,
            )

        elif action_type == 'decline':
            return challenges.ChallengesDecline(
                chpp=self, action_type=action_type, team_id=team_id,
                is_weekend_friendly=is_weekend_friendly,
                training_match_id=training_match_id,
                **kwargs,
            )

        elif action_type == 'withdraw':
            return challenges.ChallengesWithdraw(
                chpp=self, action_type=action_type, training_match_id=training_match_id,
                **kwargs,
            )

        else:
            raise ValueError("if set, 'action_type' must be equal to"
                             "'view', 'challengeable', 'challenge', "
                             "'accept', 'decline' or 'withdraw'")

    def xml_club(self, team_id: Optional[int] = None, **kwargs,
                 ) -> club.Club:
        """Request the `club.xml` file from the CHPP API.

        Args:
            team_id: Team ID to get data for. Must refer to a senior team managed by requesting
                user. If `None` (the default), Hattrick uses the authenticated user's primary
                team ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `club.xml` file.

        """
        return club.Club(chpp=self, team_id=team_id, **kwargs)

    def xml_cup_matches(
            self, cup_id: int, season: Optional[int] = None, cup_round: Optional[int] = None,
            start_after_match_id: Optional[int] = None, **kwargs,
    ) -> cup_matches.CupMatches:
        """Request the `cup_matches.xml` file from the CHPP API.

        Args:
            cup_id: What cup to show the matches for.
            season: What season to show the matches for. If `None` (the default), Hattrick uses
                Latest Season.
            cup_round: What cupround to show the matches for. If `None` (the default), Hattrick
                uses Latest CupRound.
            start_after_match_id: For large cups in the first round, there will be more than 256
                matches to display. To be able to fetch the next 256 matches, take the last
                MatchID received from the XML output. Send it as StartAfterMatchID=matchID. This
                will return the next 256 matches with MatchID > StartAfterMatchID. Matches are
                sorted by MatchID ascending. If `None` (the default), Hattrick uses 0.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `cup_matches.xml` file.

        """
        return cup_matches.CupMatches(
            chpp=self, cup_id=cup_id, season=season, cup_round=cup_round,
            start_after_match_id=start_after_match_id, **kwargs,
        )

    def xml_current_bids(
            self,
            action_type: str = 'view',
            team_id: Optional[int] = None,
            transfer_id: Optional[int] = None,
            tracking_type_id: Optional[int] = None,
            **kwargs,
    ) -> current_bids.CurrentBids:
        """Request the `current_bids.xml` file from the CHPP API.

        Args:
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'view' (Shows all active, recently finished or hotlisted transfers for the
                         specified team), 'ignoreTransfer' (Removes the tracking of a specific
                         transfer, for Supporters only), 'deleteAllFinished' (Removes
                         the tracking of all finished transfers in one go, for Supporters only).
            team_id: Team ID to show the transfers for. Must refer to a senior team managed by
                requesting user. If `None` (the default), Hattrick uses the authenticated user's
                primary team ID.
            transfer_id: ID of the transfer to be ignored.
            tracking_type_id: Tracking type (category) of the transfer to be ignored. Only values
                              5, 8 and 9 are allowed.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `current_bids.xml` file.

        """
        return current_bids.CurrentBids(
            chpp=self,
            action_type=action_type,
            team_id=team_id,
            transfer_id=transfer_id,
            tracking_type_id=tracking_type_id,
            **kwargs,
        )

    def xml_economy(self, team_id: Optional[int] = None, **kwargs,
                    ) -> economy.Economy:
        """Request the `economy.xml` file from the CHPP API.

        Args:
            team_id: Team ID to get data for. Must refer to a senior team managed by requesting
                user. If `None` (the default), Hattrick uses the authenticated user's primary
                team ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `economy.xml` file.

        """
        return economy.Economy(chpp=self, team_id=team_id, **kwargs)

    def xml_fans(self, team_id: Optional[int] = None, **kwargs,
                 ) -> fans.Fans:
        """Request the `fans.xml` file from the CHPP API.

        Args:
            team_id: Team ID to get data for. Must refer to a senior team managed by requesting
                user. If `None` (the default), Hattrick uses the authenticated user's primary
                team ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `fans.xml` file.

        """
        return fans.Fans(chpp=self, team_id=team_id, **kwargs)

    def xml_hof_players(self, team_id: Optional[int] = None, **kwargs,
                        ) -> hof_players.HallOfFamePlayers:
        """Request the `hof_players.xml` file from the CHPP API.

        Args:
            team_id: Team ID for HoF. If `None` (the default), Hattrick uses the
                authenticated user's ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `hof_players.xml` file.

        """
        return hof_players.HallOfFamePlayers(chpp=self, team_id=team_id, **kwargs)

    def xml_ladder_details(
            self, team_id: Optional[int] = None, page_size: Optional[int] = None,
            page_index: Optional[int] = None, **kwargs,
    ) -> ladder_details.LadderDetails:
        """Request the `ladder_details.xml` file from the CHPP API.

        Args:
            team_id: If pageindex is -1, the page where this team is positioned will be shown. If
                `None` (the default), Hattrick uses the authenticated user's primary team ID.
            page_size: How many results to be shown in each page, the maximum value is 100. If
                `None` (the default), Hattrick uses 25.
            page_index: What page to be shown, starts from 0. If `None` (the default), Hattrick
                uses -1.
            ladder_id: Ladder ID to get data for.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `ladder_details.xml` file.

        """
        return ladder_details.LadderDetails(
            chpp=self, team_id=team_id, page_size=page_size,
            page_index=page_index, **kwargs,
        )

    def xml_ladder_list(self, team_id: Optional[int] = None, **kwargs,
                        ) -> ladder_list.LadderList:
        """Request the `ladder_list.xml` file from the CHPP API.

        Args:
            team_id: Team ID to get data for. If `None` (the default), Hattrick uses the
                authenticated user's primary team ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `ladder_list.xml` file.

        """
        return ladder_list.LadderList(chpp=self, team_id=team_id, **kwargs)

    def xml_league_details(
            self, league_level_unit_id: Optional[int] = None, **kwargs,
    ) -> league_details.LeagueDetails:
        """Request the `league_details.xml` file from the CHPP API.

        Args:
            league_level_unit_id: Specifies the 'series' (leagueLevelUnit) to look for data on.
                If `None` (the default), Hattrick uses LeaguelevelUnitID of the team of the
                currently authenticated user's primary club.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `league_details.xml` file.

        """
        return league_details.LeagueDetails(
            chpp=self, league_level_unit_id=league_level_unit_id, **kwargs,
        )

    def xml_league_fixtures(
            self,
            league_level_unit_id: Optional[int] = None,
            season: Optional[int] = None,
            **kwargs,
    ) -> league_fixtures.LeagueFixtures:
        """Request the `league_fixtures.xml` file from the CHPP API.

        Args:
            league_level_unit_id: Specifies the 'series' (leagueLevelUnit) to look for data on. If
                `None` (the default), Hattrick uses LeaguelevelUnitID of the team of the currently
                authenticated user's primary club.
            season: Specifies the season to look for data on. If `None` (the default), Hattrick
                uses the current season.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `league_fixtures.xml` file.

        """
        return league_fixtures.LeagueFixtures(
            chpp=self, league_level_unit_id=league_level_unit_id, season=season, **kwargs,
        )

    def xml_league_levels(self, league_id: Optional[int] = None, **kwargs,
                          ) -> league_levels.LeagueLevels:
        """Request the `league_levels.xml` file from the CHPP API.

        Args:
            league_id: The ID number of the League (for instance Sverige, USA, England...).
                If `None` (the default), Hattrick uses league ID of the team of the authenticated
                    user's primary club.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `league_levels.xml` file.

        """
        return league_levels.LeagueLevels(
            chpp=self, league_id=league_id, **kwargs,
        )

    def xml_live(
            self, action_type: str = 'view', match_id: Optional[int] = None,
            source_system: str = 'hattrick', include_starting_lineup: bool = False,
            use_live_events_and_texts: bool = False, last_shown_indexes: Optional[str] = None,
            **kwargs,
    ) -> live.Live:
        """Request the `live.xml` file from the CHPP API.

        Args:
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'view' (Show the latest event(s) for all tracked matches. If matchID is
                         supplied), 'viewNew' (Show those matches where new events have
                         occured since last request of the page), 'viewAll' (Show all the events
                         for all matches), 'clearAll' (Remove all tracked matches from the tracking
                         session), 'addMatch' (Add a new match to be tracked), 'deleteMatch'
                         (Remove a particular match from the session).
            match_id: The globally unique matchID.
            source_system: Specifies which source system the match belongs to.
                           Defaults to hattrick.
            include_starting_lineup: Should StartingLineup and Substitutions be included in the
                                     response? Defaults to false.
            use_live_events_and_texts: Should the events and texts be as on the live page on the
                                       site? Defaults to false.
            last_shown_indexes: JSON formatted array of last shown indexes for each match.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `live.xml` file.

        """
        return live.Live(
            chpp=self, action_type=action_type, match_id=match_id,
            source_system=source_system, include_starting_lineup=include_starting_lineup,
            use_live_events_and_texts=use_live_events_and_texts,
            last_shown_indexes=last_shown_indexes, **kwargs,
        )

    def xml_manager_compendium(
            self, user_id: Optional[int] = None, **kwargs,
    ) -> manager_compendium.ManagerCompendium:
        """Request the `manager_compendium.xml` file from the CHPP API.

        Args:
            user_id: What user to show the data for. If `None` (the default), Hattrick uses the
                authenticated user's ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `manager_compendium.xml` file.

        """
        return manager_compendium.ManagerCompendium(
            chpp=self, user_id=user_id, **kwargs,
        )

    def xml_match_details(
            self, match_id: int, source_system: Optional[str] = None,
            match_events: Optional[bool] = None, **kwargs,
    ) -> match_details.MatchDetails:
        """Request the `match_details.xml` file from the CHPP API.

        Args:
            match_id: Which match to show details for.
            source_system: Specifies which source system the match belongs to.
            match_events: Whether match events shall be shown or not. Allowed values: 'false' (Show
                          no match events), 'true' (Show match events).
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `match_details.xml` file.

        """
        return match_details.MatchDetails(
            chpp=self, match_id=match_id, source_system=source_system,
            match_events=match_events, **kwargs,
        )

    def xml_match_lineup(
            self, match_id: Optional[int] = None, team_id: Optional[int] = None,
            source_system: Optional[str] = None, **kwargs,
    ) -> match_lineup.MatchLineup:
        """Request the `match_lineup.xml` file from the CHPP API.

        Args:
            match_id: Specifies which particular match data is requested for. If `None` (the
                default), Hattrick uses the last match.
            team_id: Specifies which of the two participating teams data should be shown for. If
                `None` (the default), Hattrick uses the authenticated user's team.
            source_system: Specifies which source system the match belongs to.
                           If `None` (the default), Hattrick uses Hattrick.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `match_lineup.xml` file.

        """
        return match_lineup.MatchLineup(
            chpp=self, match_id=match_id, team_id=team_id,
            source_system=source_system, **kwargs,
        )

    def xml_match_orders(
            self, match_id: int, action_type: str = 'view', team_id: Optional[int] = None,
            source_system: str = 'Hattrick', lineup: Optional[str] = None, **kwargs,
    ) -> (match_orders.MatchOrdersView
          | match_orders.MatchOrdersSetMatchOrder
          | match_orders.MatchOrdersPredictRatings):
        """Request the `match_orders.xml` file from the CHPP API.

        Args:
            match_id: Specifies which particular match data is requested for.
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'view' (Returns data on the matchorder for the match requested),
                         'setmatchorder' (Sets a matchorder for the match specified. Requests to
                         set matchorder), 'predictratings' (Predicts the sector and tactic
                         ratings for the match specified).
            team_id: Team ID to get/set orders for. Must refer to a senior or youth team managed
                by requesting user. If `None` (the default), Hattrick uses the authenticated
                user's primary team ID.
            source_system: Specifies which source system the match belongs to.
                           Defaults to Hattrick.
            lineup: JSON formatted match orders to set for the match specified or to predict
                    ratings. Must be specified as request body for POST. Required for
                    actionType=setmatchorder and optional for actionType=predictratings, otherwise
                    not used.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `match_orders.xml` file.

        """
        if action_type == 'view':
            return match_orders.MatchOrdersView(
                chpp=self, action_type=action_type, match_id=match_id,
                team_id=team_id, source_system=source_system, lineup=lineup,
                **kwargs,
            )

        elif action_type == 'setmatchorder':
            return match_orders.MatchOrdersSetMatchOrder(
                chpp=self, action_type=action_type, match_id=match_id,
                team_id=team_id, source_system=source_system, lineup=lineup,
                **kwargs,
            )

        elif action_type == 'predictratings':
            return match_orders.MatchOrdersPredictRatings(
                chpp=self, action_type=action_type, match_id=match_id,
                team_id=team_id, source_system=source_system, lineup=lineup,
                **kwargs,
            )

        else:
            raise ValueError("if set, 'action_type' must be equal to"
                             "'view', 'setmatchorder' or 'predictratings'")

    def xml_matches(
            self, team_id: Optional[int] = None, is_youth: Optional[bool] = None, **kwargs,
    ) -> matches.Matches:
        """Request the `matches.xml` file from the CHPP API.

        Args:
            team_id: What team to show the matches for: Either teamID or youthTeamID depending on
                isYouth. If `None` (the default), Hattrick uses the authenticated user's senior or
                youth team ID.
            is_youth: Is request for youth or not. If `None` (the default), Hattrick uses false.
            last_match_date: Last date to show matches to. If more than 50 matches are affected,
                             only the 50 first will be returned. If `None` (the default), Hattrick
                             uses Datetime.Now + 28 days.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `matches.xml` file.

        """
        return matches.Matches(
            chpp=self, team_id=team_id, is_youth=is_youth, **kwargs,
        )

    def xml_matches_archive(
            self, team_id: Optional[int] = None, is_youth: Optional[bool] = None,
            first_match_date: Optional[datetime] = None,
            last_match_date: Optional[datetime] = None,
            season: Optional[int] = None, include_hto: Optional[bool] = None, **kwargs,
    ) -> matches_archive.MatchesArchive:
        """Request the `matches_archive.xml` file from the CHPP API.

        Args:
            team_id: What team to show the matches for: Either teamID or youthTeamID depending on
                isYouth. If `None` (the default), Hattrick uses the authenticated user's senior or
                youth team ID.
            is_youth: Is request for youth or not. If `None` (the default), Hattrick uses false.
            first_match_date: First date to show matches in archive from. If `None` (the default),
                Hattrick uses Datetime.Now - 3 months.
            last_match_date: Last date to show matches to. For performance reasons, only an
                interval of 2 seasons back in time can be specified. If `None` (the default),
                Hattrick uses Datetime.Now - 1 day.
            season: Season to show matches for. (Only valid for senior teams, not for youth!).
            include_hto: If HTO matches (tournaments, ladders, preparation, and single matches)
                should be included. If `None` (the default), Hattrick uses false.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `matches_archive.xml` file.

        """
        return matches_archive.MatchesArchive(
            chpp=self, team_id=team_id, is_youth=is_youth,
            first_match_date=first_match_date, last_match_date=last_match_date,
            season=season, include_hto=include_hto, **kwargs,
        )

    def xml_national_teams(
            self, league_office_type_id: Optional[int] = None, **kwargs,
    ) -> national_teams.NationalTeams:
        """Request the `national_teams.xml` file from the CHPP API.

        Args:
            league_office_type_id: What national team type to list (2 = National teams, 4 = U-20
                Teams). If `None` (the default), Hattrick uses 2.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `national_teams.xml` file.

        """
        return national_teams.NationalTeams(
            chpp=self, league_office_type_id=league_office_type_id, **kwargs,
        )

    def xml_national_team_details(
            self, team_id: int, **kwargs,
    ) -> national_team_details.NationalTeamDetails:
        """Request the `national_team_details.xml` file from the CHPP API.

        Args:
            team_id: What national team type to list.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `national_team_details.xml` file.

        """
        return national_team_details.NationalTeamDetails(
            chpp=self, team_id=team_id, **kwargs,
        )

    def xml_national_team_matches(
            self, league_office_type_id: Optional[int] = None, **kwargs,
    ) -> national_team_matches.NationalTeamMatches:
        """Request the `national_team_matches.xml` file from the CHPP API.

        Args:
            league_office_type_id: What national team type to list (2 = National teams, 4 = U-20
                Teams). If `None` (the default), Hattrick uses 2.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `national_team_matches.xml` file.

        """
        return national_team_matches.NationalTeamMatches(
            chpp=self, league_office_type_id=league_office_type_id, **kwargs,
        )

    def xml_national_players(
            self,
            team_id: int,
            action_type: str = 'view',
            match_type_category: Optional[int] = None,
            show_all: Optional[bool] = None, **kwargs,
    ) -> (national_players.NationalPlayersView
          | national_players.NationalPlayersStats):
        """Request the `national_players.xml` file from the CHPP API.

        Args:
            team_id: What national team type to list.
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'view' (View the national team players of a specific type ('regular' or
                         'U-20')), 'SupporterStats' (View the number of matches that players have
                         played in the national team).
            match_type_category: What national team type to list ('NT' = all matches played in
                this National Team, 'WC' = World Cup matches played in this National Team). If
                `None` (the default), Hattrick uses NT.
            show_all: Whether to show all players (true) or a maximum of 20 players ordered by
                number of matches played (false). If `None` (the default), Hattrick uses false.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `national_players.xml` file.

        """
        if action_type == 'view':
            return national_players.NationalPlayersView(
                chpp=self, action_type=action_type, team_id=team_id, **kwargs,
            )

        elif action_type == 'SupporterStats':
            return national_players.NationalPlayersStats(
                chpp=self, action_type=action_type, team_id=team_id,
                match_type_category=match_type_category, show_all=show_all, **kwargs,
            )

        else:
            raise ValueError("if set, 'action_type' must be equal to"
                             "'view', 'setmatchorder' or 'SupporterStats'")

    def xml_national_prospect_players(
            self, team_id: int, player_category_id: Optional[int] = None, **kwargs,
    ) -> national_prospect_players.NationalProspectPlayers:
        """Request the `national_prospect_players.xml` file from the CHPP API.

        Args:
            team_id: The nationalTeamID to list prospect players for.
            player_category_id: Only list the prospect players in this category. Use 0 for players
                with no category set. If `None` (the default), Hattrick uses All categories.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `national_prospect_players.xml` file.

        """
        return national_prospect_players.NationalProspectPlayers(
            chpp=self, team_id=team_id, player_category_id=player_category_id, **kwargs,
        )

    def xml_player_events(
            self, player_id: Optional[int] = None, **kwargs,
    ) -> player_events.PlayerEvents:
        """Request the `player_events.xml` file from the CHPP API.

        Args:
            player_id: The player to get information for.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `player_events.xml` file.

        """
        return player_events.PlayerEvents(
            chpp=self, player_id=player_id, **kwargs,
        )

    def xml_player_stats(
            self, player_id: Optional[int] = None, **kwargs,
    ) -> player_stats.PlayerStats:
        """Request the `player_stats.xml` file from the CHPP API.

        Args:
            player_id: The player to get statistics for.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `player_stats.xml` file.

        """
        return player_stats.PlayerStats(
            chpp=self, player_id=player_id, **kwargs,
        )

    def xml_players(self, action_type: str = 'view', order_by: Optional[str] = None,
                    team_id: Optional[int] = None,
                    include_match_info: Optional[bool] = None,
                    **kwargs,
                    ) -> (players.PlayersView
                          | players.PlayersViewOldies
                          | players.PlayersViewOldCoaches):
        """Request the `players.xml` file from the CHPP API.

        Args:
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'view' (View the list of players belonging to a team), 'viewOldies' (View
                         the list of players who no longer belong to the club but were promoted
                         from the youth team), 'viewOldCoaches' (View list of former players that
                         now are coaches).
            order_by: The field that the outdata PlayerList should be sorted by. If `None` (the
                default), Hattrick uses PlayerNumber.
            team_id: The team for which the data should apply to. If `None` (the default),
                Hattrick uses the authenticated user's team ID.
            include_match_info: Include LastMatch container for all players. If `None` (the
                default), Hattrick uses false.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `players.xml` file.

        """
        if action_type == 'view':
            return players.PlayersView(
                chpp=self, action_type=action_type, order_by=order_by,
                team_id=team_id, include_match_info=include_match_info, **kwargs,
            )

        elif action_type == 'viewOldies':
            return players.PlayersViewOldies(
                chpp=self, action_type=action_type, order_by=order_by,
                team_id=team_id, include_match_info=include_match_info, **kwargs,
            )

        elif action_type == 'viewOldCoaches':
            return players.PlayersViewOldCoaches(
                chpp=self, action_type=action_type, order_by=order_by,
                team_id=team_id, include_match_info=include_match_info, **kwargs,
            )

        else:
            raise ValueError("if set, 'action_type' must be equal to"
                             "'view', 'viewOldies' or 'viewOldCoaches'")

    def xml_player_details(
            self, action_type: Optional[str] = None, player_id: Optional[int] = None,
            include_match_info: Optional[bool] = None, team_id: Optional[int] = None,
            bid_amount: Optional[int] = None, max_bid_amount: Optional[int] = None, **kwargs,
    ) -> player_details.PlayerDetails:
        """Request the `player_details.xml` file from the CHPP API.

        Args:
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'view' (Shows information for the player with the corresponding playerID),
                         'placeBid' (Places a bid on the player and then shows all the information,
                         for Supporters).
            player_id: The player to get information for.
            include_match_info: Set it to 'true' to get LastMatch Container. If `None` (the
                default), Hattrick uses false.
            team_id: Team ID of the team placing the bid. Must refer to a senior team managed by
                     requesting user.
            bid_amount: Bid amount in SEK.
            max_bid_amount: Maximum bid amount in SEK (autobid).
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `player_details.xml` file.

        """
        return player_details.PlayerDetails(
            chpp=self, action_type=action_type, player_id=player_id,
            include_match_info=include_match_info, team_id=team_id,
            bid_amount=bid_amount, max_bid_amount=max_bid_amount, **kwargs,
        )

    def xml_region_details(
            self, region_id: Optional[int] = None, **kwargs,
    ) -> region_details.RegionDetails:
        """Request the `region_details.xml` file from the CHPP API.

        Args:
            region_id: The region to get information for.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `region_details.xml` file.

        """
        return region_details.RegionDetails(
            chpp=self, region_id=region_id, **kwargs,
        )

    def xml_search(
            self, search_type: Optional[int] = None, search_string: Optional[str] = None,
            search_string_2: Optional[str] = None,
            search_id: Optional[int] = None,
            search_league_id: Optional[int] = None,
            page_index: Optional[int] = None, **kwargs,
    ) -> search.Search:
        """Request the `search.xml` file from the CHPP API.

        Args:
            search_type: Which type of search to perform. Allowed values: '0' (Search for players),
                         '1' (Search for arenas), '2' (Search for managers), '3' (Search for
                         series), '4' (Search for teams), '5' (Search for regions), '6' (Search for
                         match).
            search_string: The string to search for. Must be >= 3 characters long.
            search_string_2: The second string to search for. Must be >= 3 characters long.
            search_id: The specific ID to search for.
            search_league_id: The specific LeagueID to search in. -1 searches in ALL leagues. If
                `None` (the default), Hattrick uses the authenticated user's league ID.
            page_index: The zerobased PageIndex to retrieve. Will only have effect when resultset
                        has more than 25 rows.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `search.xml` file.

        """
        return search.Search(
            chpp=self, search_type=search_type, search_string=search_string,
            search_string_2=search_string_2, search_id=search_id,
            search_league_id=search_league_id, page_index=page_index, **kwargs,
        )

    def xml_staff_avatars(
            self, team_id: Optional[int] = None, **kwargs,
    ) -> staff_avatars.StaffAvatars:
        """Request the `staff_avatars.xml` file from the CHPP API.

        Args:
            team_id: Team ID to get data for. If `None` (the default), Hattrick uses the
                authenticated user's primary team ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `staff_avatars.xml` file.

        """
        return staff_avatars.StaffAvatars(
            chpp=self, team_id=team_id, **kwargs,
        )

    def xml_staff_list(
            self, team_id: Optional[int] = None, **kwargs,
    ) -> staff_list.StaffList:
        """Request the `staff_list.xml` file from the CHPP API.

        Args:
            team_id: Team ID to get data for. If `None` (the default), Hattrick uses the
                authenticated user's primary team ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `staff_list.xml` file.

        """
        return staff_list.StaffList(
            chpp=self, team_id=team_id, **kwargs,
        )

    def xml_supporters(
            self, action_type: str = 'supportedteams',
            user_id: Optional[int] = None, team_id: Optional[int] = None,
            page_index: Optional[int] = None, page_size: Optional[int] = None, **kwargs,
    ) -> (supporters.SupportersSupportedTeams
          | supporters.SupportersMySupporters):
        """Request the `supporters.xml` file from the CHPP API.

        Args:
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'supportedteams' (See the teams the user support), 'mysupporters' (See the
                         teams supporting the team).
            user_id: User ID to get data for. If `None` (the default), Hattrick uses the
                authenticated user's ID.
            team_id: Team ID to get data for. If `None` (the default), Hattrick uses the
                authenticated user's primary team ID.
            page_index: Zero based pageindex to retrieve. If `None` (the default), Hattrick uses 0.
            page_size: How many results to be shown in each page, the maximum value is 500.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `supporters.xml` file.

        """
        if action_type == 'supportedteams':
            return supporters.SupportersSupportedTeams(
                chpp=self, action_type=action_type, user_id=user_id,
                page_index=page_index, page_size=page_size, **kwargs,
            )

        elif action_type == 'mysupporters':
            return supporters.SupportersMySupporters(
                chpp=self, action_type=action_type, team_id=team_id,
                page_index=page_index, page_size=page_size, **kwargs,
            )

        else:
            raise ValueError("if set, 'action_type' must be equal to"
                             "'view', 'supportedteams' or 'mysupporters'")

    def xml_team_details(
            self, team_id: Optional[int] = None, user_id: Optional[int] = None,
            include_domestics_flags: Optional[bool] = None, include_flags: Optional[bool] = None,
            include_supporters: Optional[bool] = None, **kwargs,
    ) -> team_details.TeamDetails:
        """Request the `team_details.xml` file from the CHPP API.

        Args:
            team_id: Which team/user to show data for. teamID and userID give the same result,
                except that ownerless teams can only be accessed if submitting a teamID and that
                users without a team can only be accessed if userID is submitted. If `None` (the
                default), Hattrick uses the authenticated user's senior team ID.
            user_id: Which team/user to show data for. If neither user_id nor team_id is supplied,
                     user_id defaults to the authenticated user's ID.
            include_domestics_flags: Whether or not the teams own country should be included in
                the flag collections (provided games against domestic opponents have been played).
                If `None` (the default), Hattrick uses false.
            include_flags: Whether or not the flag collection should be provided. If `None` (the
                default), Hattrick uses false.
            include_supporters: Whether or not the supported teams and the teams supporters should
                be included. If `None` (the default), Hattrick uses false.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `team_details.xml` file.

        """
        return team_details.TeamDetails(
            chpp=self, team_id=team_id, user_id=user_id,
            include_domestics_flags=include_domestics_flags,
            include_flags=include_flags, include_supporters=include_supporters,
            ** kwargs,
        )

    def xml_team_history(
            self, team_id: Optional[int] = None, **kwargs,
    ) -> team_history.TeamHistory:
        """Request the `team_history.xml` file from the CHPP API.

        Args:
            team_id: The ID of the team to fetch the history for. If `None` (the default),
                Hattrick uses the authenticated user's primary team ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `team_history.xml` file.

        """
        return team_history.TeamHistory(
            chpp=self, team_id=team_id, **kwargs,
        )

    def xml_tournament_details(
            self, tournament_id: int, season: Optional[int] = None, **kwargs,
    ) -> tournament_details.TournamentDetails:
        """Request the `tournament_details.xml` file from the CHPP API.

        Args:
            tournament_id: The ID for the tournament to get data for.
            season: The season of the tournament.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `tournament_details.xml` file.

        """
        return tournament_details.TournamentDetails(
            chpp=self, tournament_id=tournament_id, season=season, **kwargs,
        )

    def xml_tournament_fixtures(
            self,
            tournament_id: int,
            season: Optional[int] = None,
            match_round: Optional[int] = None,
            **kwargs,
    ) -> tournament_fixtures.TournamentFixtures:
        """Request the `tournament_fixtures.xml` file from the CHPP API.

        Args:
            tournament_id: The ID for the tournament to get data for.
            season: The starting season of the tournament. This is available only for National
                    Teams cups.
            match_round: Specific match round for this tournament. It will pick the last match
                         round if the selected round is greater than the tournament's last round.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `tournament_fixtures.xml` file.

        """
        return tournament_fixtures.TournamentFixtures(
            chpp=self, tournament_id=tournament_id, season=season,
            match_round=match_round, **kwargs,
        )

    def xml_tournament_league_tables(
            self,
            tournament_id: int,
            season: Optional[int] = None,
            world_cup_round: Optional[int] = None,
            **kwargs,
    ) -> tournament_league_tables.TournamentLeagueTables:
        """Request the `tournament_league_tables.xml` file from the CHPP API.

        Args:
            tournament_id: The ID for the tournament to get data for.
            season: The season of the tournament.
            world_cup_round: Specifies which particular world cup stage data is requested for. Used
                             only for World Cup tournaments. Otherwise, not used.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `tournament_league_tables.xml` file.

        """
        return tournament_league_tables.TournamentLeagueTables(
            chpp=self, tournament_id=tournament_id, season=season,
            world_cup_round=world_cup_round, **kwargs,
        )

    def xml_tournament_list(
            self, team_id: Optional[int] = None, **kwargs,
    ) -> tournament_list.TournamentList:
        """Request the `tournament_list.xml` file from the CHPP API.

        Args:
            team_id: Team ID to get data for. If `None` (the default), Hattrick uses the
                authenticated user's primary team ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `tournament_list.xml` file.

        """
        return tournament_list.TournamentList(
            chpp=self, team_id=team_id, **kwargs,
        )

    def xml_training(
            self, action_type: str = 'view', team_id: Optional[int] = None,
            training_type: Optional[int] = None, training_level: Optional[int] = None,
            training_level_stamina: Optional[int] = None, league_id: Optional[int] = None,
            from_date: Optional[datetime] = None, **kwargs,
    ) -> (training.TrainingView
          | training.TrainingSetTraining
          | training.TrainingStats
          | training.TrainingHistoryView):
        """Request the `training.xml` file from the CHPP API.

        Args:
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'view' (Training information for the authenticated user's team), 'stats'
                         (Shows the distribution among training types for all leagues or for a
                         specific league), 'setTraining' (Set the training settings for the
                         authenticated user's team. (Requires "set_training" scope)), 'history'
                         (The training changes of a senior team since a given date. Requires
                         Gold supporter).
            team_id: Team ID to view training information for. Must refer to a senior team managed
                by requesting user. For actionType=history, it can also be a team the user
                mentors. If `None` (the default), Hattrick uses the authenticated user's primary
                team ID, except in action setTraining.
            training_type: Type of training to be set for the specified team if action is
                           setTraining.
            training_level: Training level to be set for the specified team (0-100) if action is
                            setTraining.
            training_level_stamina: Stamina level to be set for the specified team (5-100) if
                                    action is setTraining.
            league_id: What LeagueID to retrieve statistics for (empty for global stats in version
                1.7 or above). If `None` (the default), Hattrick uses the authenticated user's
                league ID.
            from_date: The date to start the training history from. A date before the first
                Hattrick season or in the future is moved to the nearest valid date. If `None`
                (the default), Hattrick uses 16 weeks before today.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `training.xml` file.

        """
        if action_type == 'view':
            return training.TrainingView(
                chpp=self, action_type=action_type,
                team_id=team_id, **kwargs,
            )

        elif action_type == 'stats':
            return training.TrainingStats(
                chpp=self, action_type=action_type,
                league_id=league_id, **kwargs,
            )

        elif action_type == 'setTraining':
            return training.TrainingSetTraining(
                chpp=self, action_type=action_type, team_id=team_id,
                training_type=training_type, training_level=training_level,
                training_level_stamina=training_level_stamina, **kwargs,
            )

        elif action_type == 'history':
            return training.TrainingHistoryView(
                chpp=self, action_type=action_type, team_id=team_id,
                from_date=from_date, **kwargs,
            )

        else:
            raise ValueError("if set, 'action_type' must be equal to"
                             "'view', 'setTraining', 'stats' or 'history'")

    def xml_training_events(
            self, player_id: int, **kwargs,
    ) -> training_events.TrainingEvents:
        """Request the `training_events.xml` file from the CHPP API.

        Args:
            player_id: What player to show training events for.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `training_events.xml` file.

        """
        return training_events.TrainingEvents(
            chpp=self, player_id=player_id, **kwargs,
        )

    def xml_transfer_search(
            self, age_min: int, age_max: int, skill_type_1: int, min_skill_value_1: int,
            max_skill_value_1: int,
            age_days_min: Optional[int] = None,
            age_days_max: Optional[int] = None,
            skill_type_2: Optional[int] = None,
            min_skill_value_2: Optional[int] = None,
            max_skill_value_2: Optional[int] = None,
            skill_type_3: Optional[int] = None,
            min_skill_value_3: Optional[int] = None,
            max_skill_value_3: Optional[int] = None,
            skill_type_4: Optional[int] = None,
            min_skill_value_4: Optional[int] = None,
            max_skill_value_4: Optional[int] = None,
            specialty: Optional[int] = None, native_country_id: Optional[int] = None,
            tsi_min: Optional[int] = None,
            tsi_max: Optional[int] = None,
            price_min: Optional[int] = None,
            price_max: Optional[int] = None,
            salary_min: Optional[int] = None, salary_max: Optional[int] = None,
            transfer_compare_avg_min: Optional[int] = None,
            transfer_compare_avg_max: Optional[int] = None,
            page_size: Optional[int] = None, page_index: Optional[int] = None, **kwargs,
    ) -> transfer_search.TransferSearch:
        """Request the `transfer_search.xml` file from the CHPP API.

        Args:
            age_min: Minimum age value (years) to search for.
            age_max: Maximum age value (years) to search for.
            skill_type_1: Main skill to search for.
            min_skill_value_1: Minimum value for the main skill (skillType1) to search for. The
                               difference between min and max can be up to 4 levels. Set pieces,
                               leadership and experience need a minimum level of 5 and keeper of 3.
            max_skill_value_1: Maximum value for the main skill (skillType1) to search for. The
                               difference between min and max can be up to 4 levels.
            age_days_min: Minimum age value (days) to search for. If `None` (the default),
                Hattrick uses 0.
            age_days_max: Maximum age value (days) to search for. If `None` (the default),
                Hattrick uses 111.
            skill_type_2: Secondary skill to search for. If `None` (the default), Hattrick uses
                'Not specified'.
            min_skill_value_2: Minimum value for the secondary skill (skillType2) to search for.
                If `None` (the default), Hattrick uses 'Not specified'.
            max_skill_value_2: Maximum value for the secondary skill (skillType2) to search for.
                If `None` (the default), Hattrick uses 'Not specified'.
            skill_type_3: Secondary skill to search for. If `None` (the default), Hattrick uses
                'Not specified'.
            min_skill_value_3: Minimum value for the secondary skill (skillType3) to search for.
                If `None` (the default), Hattrick uses 'Not specified'.
            max_skill_value_3: Maximum value for the secondary skill (skillType3) to search for.
                If `None` (the default), Hattrick uses 'Not specified'.
            skill_type_4: Secondary skill to search for. If `None` (the default), Hattrick uses
                'Not specified'.
            min_skill_value_4: Minimum value for the secondary skill (skillType4) to search for.
                If `None` (the default), Hattrick uses 'Not specified'.
            max_skill_value_4: Maximum value for the secondary skill (skillType4) to search for.
                If `None` (the default), Hattrick uses 'Not specified'.
            specialty: The specialty of the players to search for. If `None` (the default),
                Hattrick uses 'Not specified'.
            native_country_id: CountryID where the players to search for where born. If `None`
                (the default), Hattrick uses Not specified.
            tsi_min: Minimum TSI value to search for. If `None` (the default), Hattrick uses 'Not
                specified'.
            tsi_max: Maximum TSI value to search for. If `None` (the default), Hattrick uses 'Not
                specified'.
            price_min: Minimum price to search for. If `None` (the default), Hattrick uses 'Not
                specified'.
            price_max: Maximum price to search for. If `None` (the default), Hattrick uses 'Not
                specified'.
            salary_min: Minimum weekly salary to search for. It is the player's base salary,
                without the extra 20% for foreign players, the same value as Salary in the
                results. If `None` (the default), Hattrick uses 'Not specified'.
            salary_max: Maximum weekly salary to search for. It is the player's base salary,
                without the extra 20% for foreign players, the same value as Salary in the
                results. If `None` (the default), Hattrick uses 'Not specified'.
            transfer_compare_avg_min: Minimum transfer estimate to search for. It is the estimate
                saved when the player was put on the market. Players without an estimate are left
                out when this is set. If `None` (the default), Hattrick uses 'Not specified'.
            transfer_compare_avg_max: Maximum transfer estimate to search for. It is the estimate
                saved when the player was put on the market. Players without an estimate are
                included. If `None` (the default), Hattrick uses 'Not specified'.
            page_size: How many results to be shown in each page, the maximum value is 100. If
                `None` (the default), Hattrick uses 25.
            page_index: What page to be shown, starts from 0. If `None` (the default), Hattrick
                uses 0.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `transfer_search.xml` file.

        """
        return transfer_search.TransferSearch(
            chpp=self,
            age_min=age_min, age_days_min=age_days_min,
            age_max=age_max, age_days_max=age_days_max,
            skill_type_1=skill_type_1,
            min_skill_value_1=min_skill_value_1, max_skill_value_1=max_skill_value_1,
            skill_type_2=skill_type_2,
            min_skill_value_2=min_skill_value_2, max_skill_value_2=max_skill_value_2,
            skill_type_3=skill_type_3,
            min_skill_value_3=min_skill_value_3, max_skill_value_3=max_skill_value_3,
            skill_type_4=skill_type_4,
            min_skill_value_4=min_skill_value_4, max_skill_value_4=max_skill_value_4,
            specialty=specialty, native_country_id=native_country_id,
            tsi_min=tsi_min, tsi_max=tsi_max, price_min=price_min, price_max=price_max,
            salary_min=salary_min, salary_max=salary_max,
            transfer_compare_avg_min=transfer_compare_avg_min,
            transfer_compare_avg_max=transfer_compare_avg_max,
            page_size=page_size, page_index=page_index, **kwargs,
        )

    def xml_transfers_player(
            self, player_id: int, **kwargs,
    ) -> transfers_player.TransfersPlayer:
        """Request the `transfers_player.xml` file from the CHPP API.

        Args:
            player_id: The player to get the transfers for.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `transfers_player.xml` file.

        """
        return transfers_player.TransfersPlayer(
            chpp=self, player_id=player_id, **kwargs,
        )

    def xml_transfers_team(
            self, team_id: Optional[int] = None, page_index: Optional[int] = None, **kwargs,
    ) -> transfers_team.TransfersTeam:
        """Request the `transfers_team.xml` file from the CHPP API.

        Args:
            team_id: What team to show the transfers for. If `None` (the default), Hattrick uses
                the authenticated user's team ID.
            page_index: What page in the list to retrieve. Each page consists of 25 records unless
                last page which may contain 25 or less. To get the last page, specify 0. Defaults
                to 1.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `transfers_team.xml` file.

        """
        return transfers_team.TransfersTeam(
            chpp=self, team_id=team_id, page_index=page_index, **kwargs,
        )

    def xml_translations(
            self, language_id: Optional[int] = None, **kwargs,
    ) -> translations.Translations:
        """Request the `translations.xml` file from the CHPP API.

        Args:
            language_id: The ID of the language to get the translations for.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `translations.xml` file.

        """
        return translations.Translations(
            chpp=self, language_id=language_id, **kwargs,
        )

    def xml_world_cup(
            self, action_type: str = 'viewMatches', cup_id: Optional[int] = None,
            season: Optional[int] = None, match_round: Optional[int] = None,
            cup_series_unit_id: Optional[int] = None, **kwargs,
    ) -> world_cup.WorldCupViewMatches | world_cup.WorldCupViewGroups:
        """Request the `world_cup.xml` file from the CHPP API.

        Args:
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'viewMatches' (View a list of the matches of a particular group),
                         'viewGroups' (View a list of the groups (with points, place, etc.) of a
                         particular round, season).
            cup_id: The globally unique cupID. If `None` (the default), Hattrick uses 137 (the
                World Cup).
            season: The starting season of the cup.
            match_round: A key that indicates a certain round (typically 10 weeks or 9 days).
                Qualifications are always matchRound 1. If `None` (the default), Hattrick uses the
                last initialized round of the chosen cup.
            cup_series_unit_id: The globally unique identifier of the CupSeriesUnit (a 'group' of
                                4-6 teams).
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `world_cup.xml` file.

        """
        if action_type == 'viewMatches':
            return world_cup.WorldCupViewMatches(
                chpp=self, action_type=action_type, cup_id=cup_id,
                season=season, match_round=match_round,
                cup_series_unit_id=cup_series_unit_id, **kwargs,
            )

        elif action_type == 'viewGroups':
            return world_cup.WorldCupViewGroups(
                chpp=self, action_type=action_type, cup_id=cup_id,
                season=season, **kwargs,
            )

        else:
            raise ValueError("if set, 'action_type' must be equal to "
                             "'viewMatches' or 'viewGroups'")

    def xml_world_details(
            self, league_id: Optional[int] = None, country_id: Optional[int] = None,
            include_regions: Optional[bool] = None, **kwargs,
    ) -> world_details.WorldDetails:
        """Request the `world_details.xml` file from the CHPP API.

        Args:
            league_id: The leagueID to get information for.
            country_id: The countryID to get information for.
            include_regions: Indicates if regions should be shown or not.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `world_details.xml` file.

        """
        return world_details.WorldDetails(
            chpp=self, include_regions=include_regions, country_id=country_id,
            league_id=league_id, **kwargs,
        )

    def xml_world_languages(self, **kwargs) -> world_languages.WorldLanguages:
        """Request the `world_languages.xml` file from the CHPP API.

        Args:
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `world_languages.xml` file.

        """
        return world_languages.WorldLanguages(chpp=self, **kwargs)

    def xml_youth_avatars(
            self, youth_team_id: Optional[int] = None, **kwargs,
    ) -> youth_avatars.YouthAvatars:
        """Request the `youth_avatars.xml` file from the CHPP API.

        Args:
            youth_team_id: Youth team ID to get data for. Must refer to a youth team managed by
                requesting user. If `None` (the default), Hattrick uses the authenticated user's
                    primary youth team ID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `youth_avatars.xml` file.

        """
        return youth_avatars.YouthAvatars(
            chpp=self, youth_team_id=youth_team_id, **kwargs,
        )

    def xml_youth_league_details(
            self, youth_league_id: Optional[int] = None, **kwargs,
    ) -> youth_league_details.YouthLeagueDetails:
        """Request the `youth_league_details.xml` file from the CHPP API.

        Args:
            youth_league_id: Specifies the 'series' (league) to look for data on. If `None`
                (the default), Hattrick uses LeagueID of the youth team of the authenticated
                user's primary club.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `youth_league_details.xml` file.

        """
        return youth_league_details.YouthLeagueDetails(
            chpp=self, youth_league_id=youth_league_id, **kwargs,
        )

    def xml_youth_league_fixtures(
            self, youth_league_id: Optional[int] = None, season: Optional[int] = None, **kwargs,
    ) -> youth_league_fixtures.YouthLeagueFixtures:
        """Request the `youth_league_fixtures.xml` file from the CHPP API.

        Args:
            youth_league_id: Specifies the 'series' (league) to look for data on. If `None` (the
                default), Hattrick uses LeagueID of the youth team of the authenticated user's
                primary club.
            season: The season number for the league. If `None` (the default), Hattrick uses the
                current season for the YouthLeagueID.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `youth_league_fixtures.xml` file.

        """
        return youth_league_fixtures.YouthLeagueFixtures(
            chpp=self, youth_league_id=youth_league_id, season=season, **kwargs,
        )

    def xml_youth_player_details(
            self, action_type: Optional[str] = None, youth_player_id: Optional[int] = None,
            show_scout_call: Optional[bool] = None, show_last_match: Optional[bool] = None,
            **kwargs,
    ) -> youth_player_details.YouthPlayerDetails:
        """Request the `youth_player_details.xml` file from the CHPP API.

        Args:
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'details' (Show the player information), 'unlockskills' (Unlock the skills
                         of the player before showing the player information).
            youth_player_id: The player to get information for.
            show_scout_call: Set it to 'true' to get the information the scout provided when the
                player was scouted. If `None` (the default), Hattrick uses false.
            show_last_match: Set it to 'true' to get LastMatch container. If `None` (the default),
                Hattrick uses false.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `youth_player_details.xml` file.

        """
        return youth_player_details.YouthPlayerDetails(
            chpp=self, action_type=action_type, youth_player_id=youth_player_id,
            show_scout_call=show_scout_call, show_last_match=show_last_match,
            **kwargs,
        )

    def xml_youth_player_list(
            self, action_type: str = 'list', order_by: Optional[str] = None,
            youth_team_id: Optional[int] = None, show_scout_call: Optional[bool] = None,
            show_last_match: Optional[bool] = None, **kwargs,
    ) -> (youth_player_list.YouthPlayerListList
          | youth_player_list.YouthPlayerListDetails):
        """Request the `youth_player_list.xml` file from the CHPP API.

        Args:
            action_type: Indicates what type of action the page should perform. Allowed values:
                         'list' (List the players, containing only PlayerID and Name-containers),
                         'details' (Show detailed players information), 'unlockskills' (Unlock the
                         skills of the entire team before showing the players information).
            order_by: The field that the outdata PlayerList should be sorted by. If `None` (the
                default), Hattrick uses PlayerNumber.
            youth_team_id: The youth team for which the data should apply to. If `None` (the
                default), Hattrick uses the authenticated user's youth team ID.
            show_scout_call: Set it to 'true' to get the information the scout provided when the
                player was scouted. Only available if actionType=details or
                actionType=unlockskills. If `None` (the default), Hattrick uses false.
            show_last_match: Set it to 'true' to get LastMatch container. Only available if
                actionType=details or actionType=unlockskills. If `None` (the default), Hattrick
                    uses false.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `youth_player_list.xml` file.

        """
        if action_type == 'list':
            return youth_player_list.YouthPlayerListList(
                chpp=self, action_type=action_type, order_by=order_by, youth_team_id=youth_team_id,
                show_scout_call=show_scout_call, show_last_match=show_last_match, **kwargs,
            )

        elif action_type in ('details', 'unlockskills'):
            return youth_player_list.YouthPlayerListDetails(
                chpp=self, action_type=action_type, order_by=order_by,
                youth_team_id=youth_team_id, show_scout_call=show_scout_call,
                show_last_match=show_last_match, **kwargs,
            )

        else:
            raise ValueError("if set, 'action_type' must be equal to "
                             "'list', 'details' or 'unlockskills'")

    def xml_youth_team_details(
            self,
            youth_team_id: Optional[int] = None,
            show_scouts: Optional[bool] = None,
            **kwargs,
    ) -> youth_team_details.YouthTeamDetails:
        """Request the `youth_team_details.xml` file from the CHPP API.

        Args:
            youth_team_id: Which team/user to show data for. If `None` (the default), Hattrick
                uses the authenticated user's youth team ID.
            show_scouts: Set it to 'true' to get ScoutList container. If `None` (the default),
                Hattrick uses false.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The parsed data from the `youth_team_details.xml` file.

        """
        return youth_team_details.YouthTeamDetails(
            chpp=self, youth_team_id=youth_team_id, show_scouts=show_scouts, **kwargs,
        )


class CHPP(CHPPXml):
    """High-level object-oriented interface on top of the CHPP XML files.

    Custom methods (`team()`, `player()`, `match()`, ...) return
    navigable objects from `pychpp.models.custom`.

    """

    def arena(self, id_: Optional[int]=None, **kwargs) -> ht_arena.HTArena:
        """Get an arena by its Hattrick ID.

        If no ID is defined, the arena of the connected user's primary team is returned.

        Args:
            id_: Hattrick ID of the requested arena.
            **kwargs: Additional keyword arguments forwarded to the model class.

        """
        return ht_arena.HTArena(chpp=self, arena_id=id_, **kwargs)

    def league_unit(self, id_: Optional[int]=None, **kwargs) -> ht_league_unit.HTLeagueUnit:
        """Get a league unit by its Hattrick ID.

        If no ID is defined, the league unit of the connected user's primary team
        is returned.

        Args:
            id_: Hattrick ID of the requested league unit.
            **kwargs: Additional keyword arguments forwarded to the model class.

        """
        return ht_league_unit.HTLeagueUnit(chpp=self, league_level_unit_id=id_, **kwargs)

    def user(self, id_: Optional[int] = None, **kwargs) -> ht_user.HTUser:
        """Get a user by their Hattrick ID.

        If no ID is defined, the connected user is returned.

        Args:
            id_: Hattrick ID of the requested user.
            **kwargs: Additional keyword arguments forwarded to the model class.

        """
        return ht_user.HTUser(chpp=self, user_id=id_, **kwargs)

    def team(
        self, id_: Optional[int] = None, user_id: Optional[int] = None, **kwargs,
    ) -> ht_team.HTTeam:
        """Get a team by its Hattrick ID.

        If no ID is given:
        - if 'user_id' is defined, the primary team of the corresponding user is returned;
        - else the primary team of the connected user is returned.

        Args:
            id_: Hattrick ID of the requested team.
            user_id: Hattrick ID of the user whose primary team is requested.
            **kwargs: Additional keyword arguments forwarded to the model class.

        """
        return ht_team.HTTeam(chpp=self, team_id=id_, user_id=user_id, **kwargs)

    def youth_team(self, id_: Optional[int]=None, **kwargs) -> ht_youth_team.HTYouthTeam:
        """Get a youth team by its Hattrick ID.

        If no id_ is provided, the youth primary team of the connected user is returned.

        Args:
            id_: Hattrick ID of the requested youth team.
            **kwargs: Additional keyword arguments forwarded to the model class.

        """
        return ht_youth_team.HTYouthTeam(chpp=self, youth_team_id=id_, **kwargs)

    def player(self, id_: int, **kwargs) -> ht_player.HTPlayer:
        """Get a player by their Hattrick ID.

        Args:
            id_: Hattrick ID of the requested player.
            **kwargs: Additional keyword arguments forwarded to the model class.

        """
        return ht_player.HTPlayer(chpp=self, player_id=id_, **kwargs)

    def youth_player(self, id_: int, **kwargs) -> ht_youth_player.HTYouthPlayer:
        """Get a youth player by their Hattrick ID.

        Args:
            id_: Hattrick ID of the requested youth player.
            **kwargs: Additional keyword arguments forwarded to the model class.

        """
        return ht_youth_player.HTYouthPlayer(chpp=self, youth_player_id=id_, **kwargs)

    def region(self, id_: Optional[int] = None, **kwargs) -> ht_region.HTRegion:
        """Get a region by its Hattrick ID.

        Args:
            id_: Hattrick ID of the requested region.
            **kwargs: Additional keyword arguments forwarded to the model class.

        """
        return ht_region.HTRegion(chpp=self, region_id=id_, **kwargs)

    def challenge_manager(
            self,
            team_id: Optional[int] = None,
            is_weekend_friendly: Optional[bool] = None,
            **kwargs,
    ) -> ht_challenge.HTChallengeManager:
        """Get a challenge manager object.

        Args:
            team_id: Hattrick ID of the concerned team.
            is_weekend_friendly: Whether the request concerns a weekend friendly.
            **kwargs: Additional keyword arguments forwarded to the model class.

        """
        return ht_challenge.HTChallengeManager(
            chpp=self, team_id=team_id, is_weekend_friendly=is_weekend_friendly, **kwargs,
        )

    def league(
            self, id_: Optional[int] = None, country_id: Optional[int] = None,
            include_regions: Optional[bool] = None, **kwargs,
    ) -> ht_league.HTLeague:
        """Get a league by its Hattrick ID or from a country ID.

        Args:
            id_: Hattrick ID of the requested league.
            country_id: Hattrick ID of the country whose league is requested.
            include_regions: Whether to include the regions in the response.
            **kwargs: Additional keyword arguments forwarded to the model class.

        """
        return ht_league.HTLeague(chpp=self, league_id=id_, country_id=country_id,
                                  include_regions=include_regions, **kwargs)

    def match(
        self,
        id_: int,
        source_system: Optional[str] = None,
        events: Optional[bool] = None,
        **kwargs,
    ):
        """Get a match by its Hattrick ID.

        Args:
            id_: Hattrick ID of the requested match.
            source_system: Source system of the requested match.
            events: Whether to include the match events.
            **kwargs: Additional keyword arguments forwarded to the model class.

        """
        return ht_match.HTMatch(
            chpp=self, match_id=id_, source_system=source_system, match_events=events, **kwargs,
        )

    def matches_archive(self, id_: Optional[int] = None, is_youth: Optional[bool] = None,
                        first_match_date: Optional[datetime] = None,
                        last_match_date: Optional[datetime] = None,
                        season: Optional[int] = None, include_hto: Optional[bool] = None, **kwargs,
                        ) -> ht_matches_archive.HTMatchesArchive:
        """Get a matches archive.

        Args:
            id_: Hattrick ID of the team to search matches for.
            is_youth: Whether the archive concerns a youth team.
            first_match_date: Begin date to search matches.
            last_match_date: End date to search matches.
            season: Season to search matches for.
            include_hto: Whether to include tournament matches.
            **kwargs: Additional keyword arguments forwarded to the model class.

        """
        return ht_matches_archive.HTMatchesArchive(
            chpp=self, team_id=id_, is_youth=is_youth, first_match_date=first_match_date,
            last_match_date=last_match_date, season=season, include_hto=include_hto, **kwargs)

    def match_lineup(
            self,
            match_id: Optional[int] = None,
            team_id: Optional[int] = None,
            source_system: Optional[str] = None,
            **kwargs,
    ) -> ht_match_lineup.HTMatchLineup:
        """Get a match lineup.

        Args:
            match_id: Hattrick ID of the requested match.
            team_id: Hattrick ID of the team for which the lineup is requested.
            source_system: Source system of the requested match.
            **kwargs: Additional keyword arguments forwarded to the model class.

        """
        return ht_match_lineup.HTMatchLineup(
            chpp=self, match_id=match_id, team_id=team_id,
            source_system=source_system, **kwargs,
        )

    def transfer_history(
            self, team_id: Optional[int] = None, page: Optional[int] = None,
            all_transfers: Optional[bool] = None, **kwargs,
    ) -> ht_transfer_history.HTTransferHistory:
        """Get the transfer history of a team.

        Args:
            team_id: Hattrick ID of the team to get the transfer history for.
            page: Page of the transfer history to fetch.
            all_transfers: Whether to fetch all the pages of the transfer history.
            **kwargs: Additional keyword arguments forwarded to the model class.

        Returns:
            The transfer history of the team.

        """
        return ht_transfer_history.HTTransferHistory(
            chpp=self, team_id=team_id, page=page,
            all_transfers=all_transfers, **kwargs,
        )
