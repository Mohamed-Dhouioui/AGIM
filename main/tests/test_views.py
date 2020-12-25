#encoding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'agim.settings'

import json

import django
django.setup()

from unittest import TestCase, mock

from ..views import toggle_room, toggle_profile, get_sensors, update_sensor, sanitize
from ..models import Configuration, Profile, TempSensorConfig, PressSensorConfig 
from ..constants import SENSOR_TYPES

from .helpers import set_field, get_field, restore_defaults, activate_profile


class ViewTestCase(TestCase):
    def setUp(self):
        """ Set the profile 1 of room 1 to be the active one. """

        self.config = Configuration.objects.get()
        activate_profile(self.config, 1, 1)

    def tearDown(self):
        activate_profile(self.config, 1, 1)


class ToggleRoomTestCase(ViewTestCase):
    def test_toggle_room(self):
        result = json.loads(toggle_room(None, 2).content)
        assert result['room_index'] == 2

        config = Configuration.objects.get()
        assert config.active_profile.room_index == 2


class ToggleProfileTestCase(ViewTestCase):
    def test_toggle_profile(self):
        old_profile = Profile.objects.get(room_index=1, profile_index=1)
        assert old_profile.is_active == True
        new_profile = Profile.objects.get(room_index=1, profile_index=2)
        assert new_profile.is_active == False
        del old_profile, new_profile

        result = json.loads(toggle_profile(None, 2).content)
        assert result['profile_index'] == 2

        config = Configuration.objects.get()
        assert config.active_profile.profile_index == 2

        old_profile = Profile.objects.get(room_index=1, profile_index=1)
        assert old_profile.is_active == False
        new_profile = Profile.objects.get(room_index=1, profile_index=2)
        assert new_profile.is_active == True

BASIC_FIELDS = ['low_alarm', 'low_warning', 'high_warning', 'high_alarm', 
    'value', 'active', 'delay']

class GetSensorsTestCase(TestCase):
    def setUp(self):
        profile = Profile.objects.get(room_index=1, profile_index=1)
        self.sensor = TempSensorConfig.objects.get(profile=profile)
        set_field(self.sensor, 'low_alarm', 15.0)

    def tearDown(self):
        restore_defaults(self.sensor)
    
    def test_get_sensors_uses_correct_sensor_config(self):
        result = json.loads(get_sensors(None).content)
        assert result['temp']['low_alarm'] == 15.0

        # data of the correct room and profile were retrieved
        config = Configuration.objects.get()
        assert config.active_profile.room_index == 1
        assert config.active_profile.profile_index == 1

    def test_get_sensors_other_profiles_remain_unchanged(self):
        profile = Profile.objects.get(room_index=2, profile_index=2)
        sensor = TempSensorConfig.objects.get(profile=profile)
        assert sensor.low_alarm == 19.0

    def test_get_sensors_retrieves_all_required_fields(self):
        result = json.loads(get_sensors(None).content)

        assert 'analog' in result
        assert 'value' in result['analog']

        for sensor_type in SENSOR_TYPES:
            assert sensor_type in result
            for field in BASIC_FIELDS:
                assert field in result[sensor_type]

        assert 'celsius' in result['temp']              
        assert 'metric' in result['flow']
        assert 'in_h2o' in result['press']
        assert 'negative' in result['press']
        assert 'low_alarm_neg' in result['press']
        assert 'low_warning_neg' in result['press']
        assert 'high_warning_neg' in result['press']
        assert 'high_alarm_neg' in result['press']

 
class UpdateSensorTestCase(ViewTestCase):
    def test_update_sensor_for_press_sensor_all_fields(self):
        request = mock.Mock
        request.POST = {'low_alarm': '1', 'low_warning': '2', 
            'high_warning': '3', 'high_alarm': '4', 'alarm_active': 'true', 
            'delay': '5', 'low_alarm_neg': '5', 'low_warning_neg': '6', 
            'high_warning_neg': '7', 'high_alarm_neg': '8', 
            'negative_room': 'true', 'in_h2o': 'false', 'sensor_type': 'press'}

        update_sensor(request)

        profile = Configuration.objects.get().active_profile
        sensor =  PressSensorConfig.objects.get(profile=profile) 

        for key in ['alarm_active', 'in_h2o', 'negative_room', 'sensor_type']:
            request.POST.pop(key)

        for field, value in request.POST.items():
            assert get_field(sensor, field) == int(value)  

        assert sensor.alarm_active == True 
        assert sensor.in_h2o == False 
        assert sensor.negative_room == True 

        restore_defaults(sensor)

    def test_sanitize(self):
        assert sanitize("3 °C") == '3'
        assert sanitize("3 Pa") == '3'
        assert sanitize("-3 Pa") == '3'
        assert sanitize("-3 in H2O") == '3'
        assert sanitize("3") == '3'
        assert sanitize("3 F") == '3'
