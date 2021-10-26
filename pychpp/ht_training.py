from pychpp import ht_model, ht_xml


class HTTrainingCore(ht_model.HTModel):
    """
    Core Hattrick team training
    Used to create HTTraining and HTTrainingStats classes
    """

    _SOURCE_FILE = "training"
    _SOURCE_FILE_VERSION = "2.2"

    def __init__(self, action_type="view", team_ht_id=None, league_ht_id=None,
                 training_type=None, training_level=None,
                 training_level_stamina=None,
                 **kwargs,
                 ):
        """
        Initialize HTTraining instance

        :param action_type: action to perform
        (can be "view", "stats", "set_training"), defaults to "view"
        :param team_ht_id: team Hattrick ID
        (if none, fetch the primary club of connected user), defaults to None
        :param training_type: selected training type, defaults to None
        :param training_level: selected training level, defaults to None
        :param training_level_stamina: selected training level,
        defaults to None
        :key chpp: CHPP instance of connected user
        :type action_type: str, optional
        :type team_ht_id: int, optional
        :type training_type: int, optional
        :type training_level: int, optional
        :type training_level_stamina: int, optional
        :type chpp: CHPP
        """

        # if set, check parameters integrity and add to request arguments

        # action_type
        if action_type not in ("view", "stats", "set_training"):
            raise ValueError("action_type must be equal to 'view', 'stats' "
                             "or 'set_training'")

        if action_type == "set_training":
            if (not isinstance(training_type, int)
                    or not isinstance(training_level, int)
                    or not isinstance(training_level_stamina, int)):
                raise ValueError("when 'action_type' is equal to "
                                 "'set_training', 'training_type', "
                                 "'training_level' and "
                                 "'training_level_stamina' must be integers")

        # if team_ht_id is not set,
        # request will fetch primary team of current user
        if not isinstance(team_ht_id, int) and team_ht_id is not None:
            raise ValueError("team_ht_id must be an integer")
        elif team_ht_id is None and action_type == "set_training":
            raise ValueError("'team_ht_id' must be explicitly set "
                             "when 'action_type' is equal to 'set_training'")

        # if league_ht_id is set, it must be an integer
        if not isinstance(league_ht_id, int) and league_ht_id is not None:
            raise ValueError("league_ht_id must be an integer")

        # Define request arguments
        self._REQUEST_ARGS = dict()

        self._REQUEST_ARGS["actionType"] = (
            action_type
            if not action_type == "set_training"
            else "setTraining")

        self._REQUEST_ARGS["teamId"] = (str(team_ht_id)
                                        if team_ht_id is not None
                                        else "")

        self._REQUEST_ARGS["leagueID"] = (str(league_ht_id)
                                          if league_ht_id is not None
                                          else "")

        self._REQUEST_ARGS["trainingType"] = (str(training_type)
                                              if training_type is not None
                                              else "")

        self._REQUEST_ARGS["trainingLevel"] = (str(training_level)
                                               if training_level is not None
                                               else "")

        self._REQUEST_ARGS["trainingLevelStamina"] = (
            str(training_level_stamina)
            if training_level_stamina is not None
            else "")

        super().__init__(**kwargs)

    def __repr__(self):
        return f"<{str(self.__class__.__name__)} object : " \
               f"{self.team_name} ({self.team_ht_id}) >"


class HTTraining(HTTrainingCore):

    _ht_attributes = [("user_supporter_tier", "UserSupporterTier",
                       ht_xml.HTXml.ht_str,),
                      # General information
                      ("team_ht_id", "Team/TeamID",
                       ht_xml.HTXml.ht_int,),
                      ("team_name", "Team/TeamName",
                       ht_xml.HTXml.ht_str,),
                      ("training_level", "Team/TrainingLevel",
                       ht_xml.HTXml.ht_int,),
                      ("new_training_level", "Team/NewTrainingLevel",
                       ht_xml.HTXml.ht_int,),
                      ("training_type", "Team/TrainingType",
                       ht_xml.HTXml.ht_int,),
                      ("stamina_training_part", "Team/StaminaTrainingPart",
                       ht_xml.HTXml.ht_int,),
                      ("last_training_training_type",
                       "Team/LastTrainingTrainingType",
                       ht_xml.HTXml.ht_int,),
                      ("last_training_training_level",
                       "Team/LastTrainingTrainingLevel",
                       ht_xml.HTXml.ht_int,),
                      ("last_training_stamina_training_part",
                       "Team/LastTrainingStaminaTrainingPart",
                       ht_xml.HTXml.ht_int,),
                      ("trainer_ht_id",
                       "Team/Trainer/TrainerID",
                       ht_xml.HTXml.ht_int,),
                      ("trainer_name",
                       "Team/Trainer/TrainerName",
                       ht_xml.HTXml.ht_str,),
                      ("trainer_arrival_date",
                       "Team/Trainer/ArrivalDate",
                       ht_xml.HTXml.ht_datetime_from_text,),
                      ("morale",
                       "Team/Morale",
                       ht_xml.HTXml.ht_int,),
                      ("self_confidence",
                       "Team/SelfConfidence",
                       ht_xml.HTXml.ht_int,),
                      ("experience_442",
                       "Team/Experience442",
                       ht_xml.HTXml.ht_int,),
                      ("experience_433",
                       "Team/Experience433",
                       ht_xml.HTXml.ht_int,),
                      ("experience_451",
                       "Team/Experience451",
                       ht_xml.HTXml.ht_int,),
                      ("experience_352",
                       "Team/Experience352",
                       ht_xml.HTXml.ht_int,),
                      ("experience_532",
                       "Team/Experience532",
                       ht_xml.HTXml.ht_int,),
                      ("experience_343",
                       "Team/Experience343",
                       ht_xml.HTXml.ht_int,),
                      ("experience_541",
                       "Team/Experience541",
                       ht_xml.HTXml.ht_int,),
                      ("experience_523",
                       "Team/Experience523",
                       ht_xml.HTXml.ht_int,),
                      ("experience_550",
                       "Team/Experience550",
                       ht_xml.HTXml.ht_int,),
                      ("experience_253",
                       "Team/Experience253",
                       ht_xml.HTXml.ht_int,),
                      ]

    def __init__(self, action_type="view", **kwargs):

        if action_type not in ("view", "set_training"):
            raise ValueError("action_type must be equal to 'view' "
                             "or 'set_training'")

        super().__init__(action_type=action_type, **kwargs)


class HTTrainingStats(HTTrainingCore):
    """
    Hattrick training statistics (for HT supporters only)
    """
    _ht_attributes = [("league_id", "League/LeagueID",
                       ht_xml.HTXml.ht_int,),
                      ("league_name", "League/LeagueName",
                       ht_xml.HTXml.ht_str,),
                      ]

    def __init__(self, **kwargs):
        kwargs.pop("action_type", None)
        super().__init__(action_type="stats", **kwargs)


class HTTrainingStatsItem(ht_model.HTModel):
    """
    Hattrick training statistics item
    """
    _ht_attributes = [("training_stat", "TrainingStat",
                       ht_xml.HTXml.ht_int,),
                      ("number_of_teams", "NumberOfTeams",
                       ht_xml.HTXml.ht_int,),
                      ("fraction_of_teams", "FractionOfTeams",
                       ht_xml.HTXml.ht_int,),
                      ]
