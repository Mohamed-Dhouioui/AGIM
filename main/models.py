from django.db import models

from .constants import COLOR_CHOICES

# add a string method to all models
# merge equal sensor classes - can only the defaults be changed?
# (does not make too much sense because of float and integer fields)
# https://stackoverflow.com/questions/7884757/how-do-you-change-field-arguments-in-django-model-subclasses

class Measurement(models.Model):
    """ Model to store all sensor reads. """

    temperature = models.FloatField(default=None, null=True)
    humidity = models.FloatField(default=None, null=True)
    pressure = models.FloatField(default=None, null=True)
    airflow = models.PositiveSmallIntegerField(default=None, null=True)
    analog = models.PositiveSmallIntegerField(default=None, null=True)
    particles = models.PositiveSmallIntegerField(default=None, null=True)
    room = models.PositiveSmallIntegerField(default=None)  # 1 or 2
    timestamp = models.DateTimeField(auto_now_add= True)


class SensorConfig(models.Model):
    """ Abstract base class for storing sensor configurations. Connected to
    a profile. """

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True, blank=True)
    alarm_active = models.BooleanField(default=False)
    delay = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True


class PartSensorConfig(SensorConfig):
    """ Particle sensor configuration model. Defaults are made up for now. """

    low_alarm = models.PositiveSmallIntegerField(default=100)
    low_warning = models.PositiveSmallIntegerField(default=200)
    high_warning = models.PositiveSmallIntegerField(default=300)
    high_alarm = models.PositiveSmallIntegerField(default=400)


class FlowSensorConfig(SensorConfig):
    """ Airflow sensor configuration model. Stores also the unit type 
    (metric or imperial). """

    low_alarm = models.PositiveSmallIntegerField(default=950)
    low_warning = models.PositiveSmallIntegerField(default=1000)
    high_warning = models.PositiveSmallIntegerField(default=1050)
    high_alarm = models.PositiveSmallIntegerField(default=1100)

    metric = models.BooleanField(default=True)

    volume = models.FloatField(default=28.0)
    square = models.BooleanField(default=False)
    diameter = models.FloatField(default=203.0)
    width = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)

    average = models.FloatField(default=0.0)
    k_factor = models.PositiveSmallIntegerField(default=100)


class PressSensorConfig(SensorConfig):
    """ Pressure sensor configuration model. Stores also values for a 
    negative room and if the current room type is a negative room. """

    negative_room = models.BooleanField(default=False)
    in_h2o = models.BooleanField(default=True)

    low_alarm = models.PositiveSmallIntegerField(default=1)
    low_warning = models.PositiveSmallIntegerField(default=3)
    high_warning = models.PositiveSmallIntegerField(default=22)
    high_alarm = models.PositiveSmallIntegerField(default=25)

    # this sucks a little since i could just use the same fields but
    # specification says we need different defaults
    low_alarm_neg = models.PositiveSmallIntegerField(default=15)
    low_warning_neg = models.PositiveSmallIntegerField(default=12)
    high_warning_neg = models.PositiveSmallIntegerField(default=8)
    high_alarm_neg = models.PositiveSmallIntegerField(default=7)

    average = models.FloatField(default=0.0)


class TempSensorConfig(SensorConfig):
    """ Temperature sensor configuration model. """

    low_alarm = models.FloatField(default=19.0)
    low_warning = models.FloatField(default=22.0)
    high_warning = models.FloatField(default=26.0)
    high_alarm = models.FloatField(default=29.0)

    celsius = models.BooleanField(default=True)


class HumSensorConfig(SensorConfig):
    """ Humidity sensor configuration model. """

    low_alarm = models.FloatField(default=40.0)
    low_warning = models.FloatField(default=45.0)
    high_warning = models.FloatField(default=55.0)
    high_alarm = models.FloatField(default=60.0)

    

class Profile(models.Model):
    room_index = models.PositiveSmallIntegerField(default=None)  # 1 or 2
    profile_index = models.PositiveSmallIntegerField(default=1)  # 1..5
    title = models.CharField(default=None, max_length=30)
    color = models.IntegerField(choices=COLOR_CHOICES, default=4)
    is_active = models.BooleanField(default=False)  # if the profile is active for its room


class Configuration(models.Model):
    """ Main configuration model. Connected to the password model, the active 
    features model, the display settings model, the active profile, sound, and the network 
    configuration. Stores which data should be displayed on data page. Stores
    the log interval index. """

    password = models.ForeignKey('Password', on_delete=models.CASCADE, null=True, blank=True)
    sound = models.ForeignKey('Sound', on_delete=models.CASCADE, null=True, blank=True)
    features = models.ForeignKey('Features', on_delete=models.CASCADE, null=True, blank=True)
    display = models.ForeignKey('Display', on_delete=models.CASCADE, null=True, blank=True)
    active_profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True, blank=True)
    network = models.ForeignKey('Network', on_delete=models.CASCADE, default=None)
    comm = models.ForeignKey('Comm', on_delete=models.CASCADE, null=True, blank=True)
    log_interval = models.PositiveSmallIntegerField(default=1)  # level 1
    display_type = models.PositiveSmallIntegerField(default=0)  # display data for room 1


class Network(models.Model):
    """ Network configuration model with network name and password. """

    name = models.CharField(default=None, max_length=30, null=True, blank=True)
    password = models.CharField(default=None, max_length=30, null=True, blank=True)


class Features(models.Model):
    """ Model containing the activation state of all features. """

    temperature = models.BooleanField(default=True)
    humidity = models.BooleanField(default=True)
    pressure = models.BooleanField(default=True)
    airflow = models.BooleanField(default=True)
    analog = models.BooleanField(default=True)
    particles = models.BooleanField(default=True)


class Sound(models.Model):
    """ Model containing the activation state alarm and touch sound. """

    alarm = models.BooleanField(default=True)
    touch = models.BooleanField(default=False)


class Password(models.Model):
    """ Model with the current password and a flag if screen locking is on. """
    active = models.BooleanField(default=False)
    password = models.CharField(default='master', max_length=30, null=True, blank=True)


class Display(models.Model):
    """ Display configuration mode with screen sleep activation flag and sleep
    timeout and screen lock timeout.  """

    screen_sleep = models.BooleanField(default=False)
    off_time = models.PositiveSmallIntegerField(default=60)  # seconds
    lock_time = models.PositiveSmallIntegerField(default=30)  # seconds
class Comm(models.Model):
    bacnet_status = models.BooleanField(default=False)
    baudrate = models.CharField(default='9600',max_length=30, null=True, blank=True)
    mac_adress = models.CharField(default='11',max_length=30, null=True, blank=True)
    object_instance = models.CharField(default='15',max_length=30, null=True, blank=True)
