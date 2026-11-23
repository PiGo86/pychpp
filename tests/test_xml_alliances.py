"""Tests for the `alliances.xml` CHPP file parsing."""

from pychpp import CHPP
from pychpp.models.xml.alliances import Alliances


def test_alliances_version_1_4(mocked_chpp: 'CHPP'):
    a = mocked_chpp.xml_alliances(search_for='flag', search_type=1, version='1.4')

    assert isinstance(a, Alliances)
    assert a.pages == 3
    assert a.page_index == 0
    assert a.user_supporter_tier == 'none'
    assert len(a.alliances) == 25

    first = a.alliances[0]
    assert first.id == 120897
    assert first.name == 'Capture The Flag'
    assert first.description == 'Team Rot gegen Team Blau, ein ewig w&#228;hrender Kampf. '
    assert a.alliances[1].id == 119259
    assert a.alliances[1].name == 'Flags'


def test_alliances_version_1_5(mocked_chpp: 'CHPP'):
    a = mocked_chpp.xml_alliances(search_for='flag', search_type=1, version='1.5')

    # 1.5 adds no output compared to 1.4 (only the userId input for SearchType 5)
    assert a.pages == 3
    assert a.page_index == 0
    assert a.user_supporter_tier == 'none'
    assert len(a.alliances) == 25
    assert a.alliances[0].id == 120897
    assert a.alliances[0].name == 'Capture The Flag'


def test_alliances_search_type_5_with_user_id(mocked_chpp: 'CHPP'):
    # SearchType=5 with userId only exists from version 1.5 ; the mock only finds
    # the fixture if userId is correctly sent as 'userId' in the request
    a = mocked_chpp.xml_alliances(search_for='', search_type=5, user_id=1728698,
                                  version='1.5')

    assert a.pages == 1
    assert a.page_index == 0
    assert a.user_supporter_tier == 'none'
    assert a.alliances == []


def test_alliances_search_type_5_current_user(mocked_chpp: 'CHPP'):
    a = mocked_chpp.xml_alliances(search_for='', search_type=5, version='1.5')

    assert a.pages == 1
    assert a.alliances == []
