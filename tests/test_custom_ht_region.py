import re

from pychpp.models.custom.ht_region import HTRegion

from .conftest import REGION_PATTERN


def test_get_current_user_region(chpp):
    region = chpp.region()
    assert isinstance(region, HTRegion)
    assert isinstance(region.id, int)
    assert isinstance(region.name, str)
    assert isinstance(region.number_of_users, int)
    assert isinstance(region.number_of_online, int)
    assert isinstance(region.weather_id, int)
    assert isinstance(region.tomorrow_weather_id, int)
    assert isinstance(region.url, str)

    region_match = re.match(REGION_PATTERN, region.url)
    assert region_match is not None
    assert int(region_match.group(1)) == region.id


def test_get_specific_region(mocked_chpp):
    region = mocked_chpp.region(id_=149)
    assert isinstance(region, HTRegion)
    assert region.id == 149
    assert region.name == "Provence-Alpes-Côte d'Azur"
    assert region.weather_id == 2
    assert region.tomorrow_weather_id == 1
    assert region.number_of_users == 895
    assert region.number_of_online == 34

    region_match = re.match(REGION_PATTERN, region.url)
    assert region_match is not None
    assert int(region_match.group(1)) == 149
