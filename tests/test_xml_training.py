"""Tests for the `training.xml` CHPP file parsing."""

from datetime import datetime

import pytest

from pychpp.models.xml.training import TrainingView
from pychpp.fixtures.ht_datetime import HTDatetime
from pychpp.fixtures.ht_error import HTAccessDeniedError


def test_get_training(mocked_chpp):
    training = mocked_chpp.xml_training(action_type='view', team_id=1165592,
                                        version='2.2')

    assert isinstance(training, TrainingView)

    assert training.team_id == 1165592
    assert training.team_name == "Les Poitevins de La Chapelle"

    assert training.training_level == 98
    assert training.new_training_level is None
    assert training.training_type == 3
    assert training.stamina_training_part == 25
    assert training.last_training.training_type == 5
    assert training.last_training.training_level == 95
    assert training.last_training.stamina_training_part == 16

    assert training.trainer.id == 421746800
    assert training.trainer.name == "Quentin Lavigne"
    assert training.trainer.arrival_date == HTDatetime.from_calendar(
        2018, 3, 23, 19, 44, 0)

    assert training.morale == 4
    assert training.self_confidence == 5

    assert training.experience._442 == 7
    assert training.experience._433 == 4
    assert training.experience._451 == 3
    assert training.experience._352 == 8
    assert training.experience._532 == 4
    assert training.experience._343 == 3
    assert training.experience._541 == 6
    assert training.experience._523 == 9
    assert training.experience._550 == 5
    assert training.experience._253 == 10


def test_training_version_2_3(mocked_chpp):
    training = mocked_chpp.xml_training(action_type='view', team_id=1165592,
                                        version='2.3')

    assert isinstance(training, TrainingView)

    assert training.team_id == 1165592
    assert training.team_name == "Les Poitevins de La Chapelle"
    assert training.training_level == 100
    assert training.training_type == 5
    assert training.stamina_training_part == 22
    assert training.morale == 4
    assert training.self_confidence == 5
    assert training.last_training.training_type == 5
    assert training.last_training.training_level == 100
    assert training.last_training.stamina_training_part == 22
    assert training.trainer.id == 421746800
    assert training.trainer.name == "Quentin Lavigne"
    assert training.trainer.arrival_date == HTDatetime.from_calendar(
        2018, 3, 23, 19, 44, 0)


def test_training_history_access_denied(chpp):
    # actionType=history requires Gold supporter, the connected user has tier 'none'
    with pytest.raises(HTAccessDeniedError, match='Gold supporter is required'):
        chpp.xml_training(action_type='history', team_id=1165592,
                          from_date=datetime(2026, 7, 1), version='2.3')
