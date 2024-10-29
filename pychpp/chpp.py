from datetime import datetime
from typing import Union, Optional

from rauth import OAuth1Service
from rauth import OAuth1Session
from rauth.oauth import HmacSha1Signature
import xml.etree.ElementTree

from pychpp.models.xml import (manager_compendium, team_details, achievements, arena_details,
                               challenges, region_details, league_details, league_fixtures,
                               match_lineup, national_teams, national_team_details, player_details,
                               training, transfers_team, world_details, world_cup, players,
                               youth_player_details, youth_team_details, youth_player_list,
                               matches_archive, match_details, cup_matches, alliances,
                               alliance_details, avatars, bookmarks, club, current_bids, economy,
                               fans, hof_players, ladder_details, ladder_list, league_levels, live,
                               matches, match_orders, national_team_matches, national_players,
                               player_events, search, staff_avatars, staff_list, supporters,
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
    """
    Manage connection and requests with Hattrick API
    """

    def __init__(self,
                 consumer_key: str,
                 consumer_secret: str,
                 access_token_key: str = None,
                 access_token_secret: str = None,
                 ):
        """
        Initialization of a CHPP instance

        It needs at least consumer_key and consumer_secret parameters.

        If access_token_key and access_token_secret parameters are not defined,
        the instantiated object can be used to obtain them from Hattrick.

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
        self.check_token_url = (
            "https://chpp.hattrick.org/oauth/check_token.ashx")
        self.invalidate_token_url = (
            "https://chpp.hattrick.org/oauth/invalidate_token.ashx")

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

            elif "Your team is still in the cup" in error_text:
                raise ht_error.HTTeamNotAvailableError(
                    "The own team is still in cup")

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

    def _base_request(
            self, url, parse_data=True, method='GET', **kwargs,
    ) -> xml.etree.ElementTree:
        """
        Base method for sending a request via the CHPP API

        :param url: url to fetch
        :param parse_data: parse or not returned data as xml
        :return: xml data fetched on Hattrick
        """
        session = self.open_session()

        if method == 'GET':
            query = session.get(url, params=kwargs)
        elif method == 'POST':
            query = session.post(url, data=kwargs)
        else:
            raise ValueError(f"Unknown method '{method}'")

        query.encoding = "UTF-8"
        self.last_url = query.url

        if query.status_code == 401:
            raise ht_error.HTUnauthorizedAction(
                "The requested action seems to be unauthorized "
                "(401 error code). Please heck your credentials scope.")

        if not parse_data:
            return query.text

        else:
            data = xml.etree.ElementTree.fromstring(query.text)
            file_name = data.find("FileName").text

            # If Hattrick returns an error, an exception is raised
            if file_name == "chpperror.xml":
                self._analyze_error(data)

            return data

    def check_token(self):
        """
        Check token key and secret validity

        :return: validity and other information about current token
        :rtype: dict
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
        """
        Invalidate current token

        :return: information about invalidated token
        :rtype: str
        """
        try:
            return self._base_request(url=self.invalidate_token_url,
                                      parse_data=False)
        except ht_error.HTUnauthorizedAction:
            return "token is already invalid"

    def request(self, **kwargs):
        """
        Send a request via the CHPP API

        :return: xml data fetched on Hattrick
        :rtype: xml.etree.ElementTree
        """
        return self._base_request(url=self.base_url, parse_data=True, **kwargs)


class CHPPXml(CHPPBase):

    def xml_achievements(self, user_id: int = None) -> achievements.Achievements:

        return achievements.Achievements(chpp=self, user_id=user_id)

    def xml_alliances(
            self,
            search_for: str,
            search_type: int = None,
            search_language_id: int = None,
            page_index: int = None,
            **kwargs,
    ) -> alliances.Alliances:

        return alliances.Alliances(
            chpp=self,
            search_type=search_type,
            search_for=search_for,
            search_language_id=search_language_id,
            page_index=page_index,
            **kwargs,
        )

    def xml_alliance_details(
            self,
            action_type: str = 'view',
            subset: int = None,
            alliance_id: int = None,
            **kwargs,
    ) -> Union[alliance_details.AllianceDetailsView,
               alliance_details.AllianceDetailsRoles,
               alliance_details.AllianceDetailsMembers,
               alliance_details.AllianceDetailsMembersSubset,
               ]:

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
            ValueError("'action_type' argument must be "
                       "equal to 'view', 'roles', "
                       "'members' or 'membersSubset'")

    def xml_arena_details(
            self, stats_type: str = None, arena_id: int = None, team_id: int = None,
            match_type: str = None, first_date: datetime = None,
            last_date: datetime = None, stats_league_id: int = None,
    ) -> Union[arena_details.ArenaDetailsDefault,
               arena_details.ArenaDetailsMyArena,
               arena_details.ArenaDetailsLeagueArenaStats]:

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
            action_type: str = None,
            team_id: int = None,
            **kwargs,
    ) -> avatars.Avatars:

        return avatars.Avatars(
            chpp=self,
            action_type=action_type,
            team_id=team_id,
            **kwargs,
        )

    def xml_bookmarks(
            self, bookmark_type_id: int = None,
            **kwargs,
    ) -> bookmarks.Bookmarks:

        return bookmarks.Bookmarks(
            chpp=self,
            bookmark_type_id=bookmark_type_id,
            **kwargs,
        )

    def xml_challenges(
            self, action_type: str = 'view', team_id: Optional[int] = None,
            is_weekend_friendly: int = 0, suggested_team_ids: str = None,
            opponent_team_id: int = None, match_type: int = None,
            match_place: int = None, neutral_arena_id: int = None,
            training_match_id: int = None, **kwargs,
    ) -> Union[challenges.ChallengesView,
               challenges.ChallengesChallengeable,
               challenges.ChallengesChallenge,
               challenges.ChallengesAccept,
               challenges.ChallengesDecline,
               challenges.ChallengesWithdraw]:

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

    def xml_club(self, team_id: int = None, **kwargs,
                 ) -> club.Club:

        return club.Club(chpp=self, team_id=team_id, **kwargs)

    def xml_cup_matches(
            self, cup_id: int, season: int = None, cup_round: int = None,
            start_after_match_id: int = None, **kwargs,
    ) -> cup_matches.CupMatches:

        return cup_matches.CupMatches(
            chpp=self, cup_id=cup_id, season=season, cup_round=cup_round,
            start_after_match_id=start_after_match_id, **kwargs,
        )

    def xml_current_bids(
            self,
            action_type: str = 'view',
            team_id: int = None,
            transfer_id: int = None,
            tracking_type_id: int = None,
            **kwargs,
    ) -> current_bids.CurrentBids:

        return current_bids.CurrentBids(
            chpp=self,
            action_type=action_type,
            team_id=team_id,
            transfer_id=transfer_id,
            tracking_type_id=tracking_type_id,
            **kwargs,
        )

    def xml_economy(self, team_id: int = None, **kwargs,
                    ) -> economy.Economy:

        return economy.Economy(chpp=self, team_id=team_id, **kwargs)

    def xml_fans(self, team_id: int = None, **kwargs,
                 ) -> fans.Fans:

        return fans.Fans(chpp=self, team_id=team_id, **kwargs)

    def xml_hof_players(self, team_id: int = None, **kwargs,
                        ) -> hof_players.HallOfFamePlayers:

        return hof_players.HallOfFamePlayers(chpp=self, team_id=team_id, **kwargs)

    def xml_ladder_details(
            self, team_id: int = None, page_size: int = None,
            page_index: int = None, **kwargs,
    ) -> ladder_details.LadderDetails:

        return ladder_details.LadderDetails(
            chpp=self, team_id=team_id, page_size=page_size,
            page_index=page_index, **kwargs,
        )

    def xml_ladder_list(self, team_id: int = None, **kwargs,
                        ) -> ladder_list.LadderList:

        return ladder_list.LadderList(chpp=self, team_id=team_id, **kwargs)

    def xml_league_details(
            self, league_level_unit_id: int = None, **kwargs,
    ) -> league_details.LeagueDetails:

        return league_details.LeagueDetails(
            chpp=self, league_level_unit_id=league_level_unit_id, **kwargs,
        )

    def xml_league_fixtures(
            self, league_level_unit_id: int = None, season: int = None, **kwargs,
    ) -> league_fixtures.LeagueFixtures:

        return league_fixtures.LeagueFixtures(
            chpp=self, league_level_unit_id=league_level_unit_id, season=season, **kwargs,
        )

    def xml_league_levels(self, league_id: int = None, **kwargs,
                          ) -> league_levels.LeagueLevels:

        return league_levels.LeagueLevels(
            chpp=self, league_id=league_id, **kwargs,
        )

    def xml_live(
            self, action_type: str = 'view', match_id: int = None,
            source_system: str = 'hattrick', include_starting_lineup: bool = False,
            use_live_events_and_texts: bool = False, last_shown_indexes: str = None,
            **kwargs,
    ) -> live.Live:

        return live.Live(
            chpp=self, action_type=action_type, match_id=match_id,
            source_system=source_system, include_starting_lineup=include_starting_lineup,
            use_live_events_and_texts=use_live_events_and_texts,
            last_shown_indexes=last_shown_indexes, **kwargs,
        )

    def xml_manager_compendium(
            self, user_id: int = None, **kwargs,
    ) -> manager_compendium.ManagerCompendium:

        return manager_compendium.ManagerCompendium(
            chpp=self, user_id=user_id, **kwargs,
        )

    def xml_match_details(
            self, match_id: int, source_system: str = None,
            match_events: bool = None, **kwargs,
    ) -> match_details.MatchDetails:

        return match_details.MatchDetails(
            chpp=self, match_id=match_id, source_system=source_system,
            match_events=match_events, **kwargs,
        )

    def xml_match_lineup(
            self, match_id: int = None, team_id: int = None,
            source_system: str = None, **kwargs,
    ) -> match_lineup.MatchLineup:

        return match_lineup.MatchLineup(
            chpp=self, match_id=match_id, team_id=team_id,
            source_system=source_system, **kwargs,
        )

    def xml_match_orders(
            self, match_id: int, action_type: str = 'view', team_id: int = None,
            source_system: str = 'Hattrick', lineup: str = None, **kwargs,
    ) -> Union[match_orders.MatchOrdersView,
               match_orders.MatchOrdersSetMatchOrder,
               match_orders.MatchOrdersPredictRatings,
               ]:

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
            self, team_id: int = None, is_youth: bool = None, **kwargs,
    ) -> matches.Matches:

        return matches.Matches(
            chpp=self, team_id=team_id, is_youth=is_youth, **kwargs,
        )

    def xml_matches_archive(
            self, team_id: int = None, is_youth: bool = None,
            first_match_date: datetime = None, last_match_date: datetime = None,
            season: int = None, include_hto: bool = None, **kwargs,
    ) -> matches_archive.MatchesArchive:

        return matches_archive.MatchesArchive(
            chpp=self, team_id=team_id, is_youth=is_youth,
            first_match_date=first_match_date, last_match_date=last_match_date,
            season=season, include_hto=include_hto, **kwargs,
        )

    def xml_national_teams(
            self, league_office_type_id: int = None, **kwargs,
    ) -> national_teams.NationalTeams:

        return national_teams.NationalTeams(
            chpp=self, league_office_type_id=league_office_type_id, **kwargs,
        )

    def xml_national_team_details(
            self, team_id: int, **kwargs,
    ) -> national_team_details.NationalTeamDetails:

        return national_team_details.NationalTeamDetails(
            chpp=self, team_id=team_id, **kwargs,
        )

    def xml_national_team_matches(
            self, league_office_type_id: int = None, **kwargs,
    ) -> national_team_matches.NationalTeamMatches:

        return national_team_matches.NationalTeamMatches(
            chpp=self, league_office_type_id=league_office_type_id, **kwargs,
        )

    def xml_national_players(
            self, team_id: int, action_type: str = 'view', match_type_category: int = None,
            show_all: bool = None, **kwargs,
    ) -> Union[national_players.NationalPlayersView,
               national_players.NationalPlayersStats,
               ]:

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

    def xml_player_events(
            self, player_id: int = None, **kwargs,
    ) -> player_events.PlayerEvents:

        return player_events.PlayerEvents(
            chpp=self, player_id=player_id, **kwargs,
        )

    def xml_players(self, action_type: str = 'view', order_by: str = None,
                    team_id: int = None, include_match_info: bool = None, **kwargs,
                    ) -> Union[players.PlayersView,
                               players.PlayersViewOldies,
                               players.PlayersViewOldCoaches]:

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
            self, action_type: str = None, player_id: int = None,
            include_match_info: bool = None, team_id: int = None,
            bid_amount: int = None, max_bid_amount: int = None, **kwargs,
    ) -> player_details.PlayerDetails:

        return player_details.PlayerDetails(
            chpp=self, action_type=action_type, player_id=player_id,
            include_match_info=include_match_info, team_id=team_id,
            bid_amount=bid_amount, max_bid_amount=max_bid_amount, **kwargs,
        )

    def xml_region_details(
            self, region_id: int = None, **kwargs,
    ) -> region_details.RegionDetails:
        return region_details.RegionDetails(
            chpp=self, region_id=region_id, **kwargs,
        )

    def xml_search(
            self, search_type: int = None, search_string: str = None,
            search_string_2: str = None, search_id: int = None, search_league_id: int = None,
            page_index: int = None, **kwargs,
    ) -> search.Search:

        return search.Search(
            chpp=self, search_type=search_type, search_string=search_string,
            search_string_2=search_string_2, search_id=search_id,
            search_league_id=search_league_id, page_index=page_index, **kwargs,
        )

    def xml_staff_avatars(
            self, team_id: int = None, **kwargs,
    ) -> staff_avatars.StaffAvatars:

        return staff_avatars.StaffAvatars(
            chpp=self, team_id=team_id, **kwargs,
        )

    def xml_staff_list(
            self, team_id: int = None, **kwargs,
    ) -> staff_list.StaffList:

        return staff_list.StaffList(
            chpp=self, team_id=team_id, **kwargs,
        )

    def xml_supporters(
            self, action_type: str = 'supportedteams',
            user_id: int = None, team_id: int = None, **kwargs,
    ) -> Union[supporters.SupportersSupportedTeams,
               supporters.SupportersMySupporters,
               ]:

        if action_type == 'supportedteams':
            return supporters.SupportersSupportedTeams(
                chpp=self, action_type=action_type, user_id=user_id, **kwargs,
            )

        elif action_type == 'mysupporters':
            return supporters.SupportersMySupporters(
                chpp=self, action_type=action_type, team_id=team_id, **kwargs,
            )

        else:
            raise ValueError("if set, 'action_type' must be equal to"
                             "'view', 'supportedteams' or 'mysupporters'")

    def xml_team_details(
            self, team_id: int = None, user_id: int = None,
            include_domestics_flags: bool = None, include_flags: bool = None,
            include_supporters: bool = None, **kwargs,
    ) -> team_details.TeamDetails:

        return team_details.TeamDetails(
            chpp=self, team_id=team_id, user_id=user_id,
            include_domestics_flags=include_domestics_flags,
            include_flags=include_flags, include_supporters=include_supporters,
            ** kwargs,
        )

    def xml_tournament_details(
            self, tournament_id: int, season: int = None, **kwargs,
    ) -> tournament_details.TournamentDetails:

        return tournament_details.TournamentDetails(
            chpp=self, tournament_id=tournament_id, season=season, **kwargs,
        )

    def xml_tournament_fixtures(
            self, tournament_id: int, season: int = None, **kwargs,
    ) -> tournament_fixtures.TournamentFixtures:

        return tournament_fixtures.TournamentFixtures(
            chpp=self, tournament_id=tournament_id, season=season, **kwargs,
        )

    def xml_tournament_league_tables(
            self, tournament_id: int, season: int = None, world_cup_round: int = None, **kwargs,
    ) -> tournament_league_tables.TournamentLeagueTables:

        return tournament_league_tables.TournamentLeagueTables(
            chpp=self, tournament_id=tournament_id, season=season,
            world_cup_round=world_cup_round, **kwargs,
        )

    def xml_tournament_list(
            self, team_id: int = None, **kwargs,
    ) -> tournament_list.TournamentList:

        return tournament_list.TournamentList(
            chpp=self, team_id=team_id, **kwargs,
        )

    def xml_training(
            self, action_type: str = 'view', team_id: int = None,
            training_type: int = None, training_level: int = None,
            training_level_stamina: int = None, league_id: int = None,
            **kwargs,
    ) -> Union[training.TrainingView,
               training.TrainingSetTraining,
               training.TrainingStats]:

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

        else:
            raise ValueError("if set, 'action_type' must be equal to"
                             "'view', 'setTraining' or 'stats'")

    def xml_training_events(
            self, player_id: int, **kwargs,
    ) -> training_events.TrainingEvents:

        return training_events.TrainingEvents(
            chpp=self, player_id=player_id, **kwargs,
        )

    def xml_transfer_search(
            self, age_min: int, age_max: int, skill_type_1: int, min_skill_value_1: int,
            max_skill_value_1: int, age_days_min: int = None, age_days_max: int = None,
            skill_type_2: int = None, min_skill_value_2: int = None, max_skill_value_2: int = None,
            skill_type_3: int = None, min_skill_value_3: int = None, max_skill_value_3: int = None,
            skill_type_4: int = None, min_skill_value_4: int = None, max_skill_value_4: int = None,
            specialty: int = None, native_country_id: int = None,
            tsi_min: int = None, tsi_max: int = None, price_min: int = None, price_max: int = None,
            page_size: int = None, page_index: int = None, **kwargs,
    ) -> transfer_search.TransferSearch:

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
            page_size=page_size, page_index=page_index, **kwargs,
        )

    def xml_transfers_player(
            self, player_id: int, **kwargs,
    ) -> transfers_player.TransfersPlayer:

        return transfers_player.TransfersPlayer(
            chpp=self, player_id=player_id, **kwargs,
        )

    def xml_transfers_team(
            self, team_id: int = None, page_index: int = None, **kwargs,
    ) -> transfers_team.TransfersTeam:

        return transfers_team.TransfersTeam(
            chpp=self, team_id=team_id, page_index=page_index, **kwargs,
        )

    def xml_translations(
            self, language_id: int = None, **kwargs,
    ) -> translations.Translations:

        return translations.Translations(
            chpp=self, language_id=language_id, **kwargs,
        )

    def xml_world_cup(
            self, action_type: str = 'viewMatches', cup_id: int = None,
            season: int = None, match_round: int = None,
            cup_series_unit_id: int = None, **kwargs,
    ) -> Union[world_cup.WorldCupViewMatches, world_cup.WorldCupViewGroups]:

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
            self, league_id: int = None, country_id: int = None,
            include_regions: bool = None, **kwargs,
    ) -> world_details.WorldDetails:

        return world_details.WorldDetails(
            chpp=self, include_regions=include_regions, country_id=country_id,
            league_id=league_id, **kwargs,
        )

    def xml_world_languages(self, **kwargs) -> world_languages.WorldLanguages:

        return world_languages.WorldLanguages(chpp=self, **kwargs)

    def xml_youth_avatars(
            self, youth_team_id: int = None, **kwargs,
    ) -> youth_avatars.YouthAvatars:

        return youth_avatars.YouthAvatars(
            chpp=self, youth_team_id=youth_team_id, **kwargs,
        )

    def xml_youth_league_details(
            self, youth_league_id: int = None, **kwargs,
    ) -> youth_league_details.YouthLeagueDetails:

        return youth_league_details.YouthLeagueDetails(
            chpp=self, youth_league_id=youth_league_id, **kwargs,
        )

    def xml_youth_league_fixtures(
            self, youth_league_id: int = None, season: int = None, **kwargs,
    ) -> youth_league_fixtures.YouthLeagueFixtures:

        return youth_league_fixtures.YouthLeagueFixtures(
            chpp=self, youth_league_id=youth_league_id, season=season, **kwargs,
        )

    def xml_youth_player_details(
            self, action_type: str = None, youth_player_id: int = None,
            show_scout_call: bool = None, show_last_match: bool = None,
            **kwargs,
    ) -> youth_player_details.YouthPlayerDetails:

        return youth_player_details.YouthPlayerDetails(
            chpp=self, action_type=action_type, youth_player_id=youth_player_id,
            show_scout_call=show_scout_call, show_last_match=show_last_match,
            **kwargs,
        )

    def xml_youth_player_list(
            self, action_type: str = 'list', order_by: str = None,
            youth_team_id: int = None, show_scout_call: bool = None,
            show_last_match: bool = None, **kwargs,
    ) -> Union[youth_player_list.YouthPlayerListList,
               youth_player_list.YouthPlayerListDetails]:

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
            self, youth_team_id: int = None, show_scouts: bool = None, **kwargs,
    ) -> youth_team_details.YouthTeamDetails:

        return youth_team_details.YouthTeamDetails(
            chpp=self, youth_team_id=youth_team_id, show_scouts=show_scouts, **kwargs,
        )


class CHPP(CHPPXml):

    def arena(self, id_=None, **kwargs) -> ht_arena.HTArena:
        """
        Get an arena from its Hattrick ID

        If no id is defined,
        return the primary team arena of connected user.

        :param id_: Hattrick ID of the requested arena
        """
        return ht_arena.HTArena(chpp=self, arena_id=id_, **kwargs)

    def league_unit(self, id_=None, **kwargs) -> ht_league_unit.HTLeagueUnit:
        """
        Get a league unit from its Hattrick ID

        If no id is defined,
        return the primary team league unit of connected user.

        :param id_: Hattrick ID of the requested league unit
        """
        return ht_league_unit.HTLeagueUnit(chpp=self, league_level_unit_id=id_, **kwargs)

    def user(self, id_: int = None, **kwargs) -> ht_user.HTUser:
        """
        Get a user from its Hattrick ID

        If no id is defined, return the connected user.

        :param id_: Hattrick ID of the requested user
        """
        return ht_user.HTUser(chpp=self, user_id=id_, **kwargs)

    def team(self, id_: int = None, user_id: int = None, **kwargs) -> ht_team.HTTeam:
        """
        Get a team from its Hattrick ID

        If ID is not given :
        - if 'user_id' is defined, returns the primary team of the corresponding user ;
        - else returns the primary team of the connected user.

        :param id_: Hattrick ID of the requested team
        :param user_id: Hattrick ID of the requested user
        """
        return ht_team.HTTeam(chpp=self, team_id=id_, user_id=user_id, **kwargs)

    def youth_team(self, id_=None, **kwargs) -> ht_youth_team.HTYouthTeam:
        """
        Get a youth team from its Hattrick ID

        If no id_ is provided,
        returns the youth primary team of connected user.

        :param id_: Hattrick ID of the requested youth team
        """
        return ht_youth_team.HTYouthTeam(chpp=self, youth_team_id=id_, **kwargs)

    def player(self, id_: int, **kwargs) -> ht_player.HTPlayer:
        """
        Get a player from its Hattrick ID

        :param id_: Hattrick ID of the requested player
        """
        return ht_player.HTPlayer(chpp=self, player_id=id_, **kwargs)

    def youth_player(self, id_: int, **kwargs) -> ht_youth_player.HTYouthPlayer:
        """
        Get a youth player from its Hattrick ID

        :param id_: Hattrick ID of the requested youth player
        """
        return ht_youth_player.HTYouthPlayer(chpp=self, youth_player_id=id_, **kwargs)

    def region(self, id_: int = None, **kwargs) -> ht_region.HTRegion:
        """
        Get a region from his Hattrick ID

        :param id_: Hattrick ID of the requested region
        """
        return ht_region.HTRegion(chpp=self, region_id=id_, **kwargs)

    def challenge_manager(
            self, team_id: int = None, is_weekend_friendly: bool = None, **kwargs,
    ) -> ht_challenge.HTChallengeManager:
        """
        Get a challenge manager object

        :param team_id: Hattrick ID of the concerned team, must be an int
        :param is_weekend_friendly: does the request concerns weekend or not
        """
        return ht_challenge.HTChallengeManager(
            chpp=self, team_id=team_id, is_weekend_friendly=is_weekend_friendly, **kwargs,
        )

    def league(
            self, id_: int = None, country_id: int = None,
            include_regions: bool = None, **kwargs,
    ) -> ht_league.HTLeague:
        """
        Get a league from its Hattrick ID or from its country ID

        :param id_: Hattrick ID of the requested league
        :param country_id: Hattrick ID of the requested country
        :param include_regions: include or no regions
        """
        return ht_league.HTLeague(chpp=self, league_id=id_, country_id=country_id,
                                  include_regions=include_regions, **kwargs)

    def match(self, id_: int, source_system: str = None, events: bool = None, **kwargs):
        """
        Get a match from its Hattrick ID

        :param id_: Hattrick ID of the requested match
        :param source_system: source system of the requested match
        :param events: include or no match events
        """
        return ht_match.HTMatch(
            chpp=self, match_id=id_, source_system=source_system, match_events=events, **kwargs,
        )

    def matches_archive(self, id_: int = None, is_youth: bool = None,
                        first_match_date: datetime = None, last_match_date: datetime = None,
                        season: int = None, include_hto: bool = None, **kwargs,
                        ) -> ht_matches_archive.HTMatchesArchive:
        """
        Get a matches archive

        :param id_: Hattrick ID of team to search matches
        :param is_youth: is requested matches archive concerns a youth team
        :param first_match_date: begin date to search matches
        :param last_match_date: end date to search matches
        :param season: season to search matches
        :param include_hto: including or not tournaments matches
        """
        return ht_matches_archive.HTMatchesArchive(
            chpp=self, team_id=id_, is_youth=is_youth, first_match_date=first_match_date,
            last_match_date=last_match_date, season=season, include_hto=include_hto, **kwargs)

    def match_lineup(
            self, match_id: int = None, team_id: int = None, source_system: str = None, **kwargs
    ) -> ht_match_lineup.HTMatchLineup:
        """
        Get a match lineup from its Hattrick ID

        :param match_id: Hattrick ID of the requested match
        :param team_id: Hattrick ID of the team for which the lineup is requested
        :param source_system: source system of the requested match
        """
        return ht_match_lineup.HTMatchLineup(
            chpp=self, match_id=match_id, team_id=team_id,
            source_system=source_system, **kwargs,
        )

    def transfer_history(
            self, team_id: int = None, page: int = None,
            all_transfers: bool = None, **kwargs,
    ) -> ht_transfer_history.HTTransferHistory:
        """
        Get transfer history for a team
        """
        return ht_transfer_history.HTTransferHistory(
            chpp=self, team_id=team_id, page=page,
            all_transfers=all_transfers, **kwargs,
        )
