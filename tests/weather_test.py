import pytest
import json

import sys
sys.path.append('.')

from weather import Weather


@pytest.fixture
def weather_obj():
    weather_instance = Weather(2)
    return weather_instance

# Using Bath Weather Data from Candidate-ID 2 for testing
# I've left out the testing of specific functions, which would
# need a testing endpoint (ones that aggregate data over many cities)
@pytest.fixture
def json_bath():
    with open("tests/test_data/bath_weather.json") as json_file:
        data = json.load(json_file)
        return data


# 3-in-1 test. Tests day, hour and attribute helper function
def test_get_attribute_helper_bath_data(weather_obj, json_bath):
    day_data = weather_obj.get_day(json_bath, "friday")
    hour_data = weather_obj.get_hour(day_data, 4)
    attribute_data = weather_obj.get_attribute(hour_data, "temperature")
    assert attribute_data == 2

def test_get_attribute_hour(weather_obj, json_bath):
    wind_speed = weather_obj.get_attribute_hour(json_bath, "Friday", 7, "wind_speed")
    assert wind_speed == 6

def test_get_median_attribute_city(weather_obj, json_bath):
    assert weather_obj.get_median_attribute_city(json_bath, "wind_speed") == 6
