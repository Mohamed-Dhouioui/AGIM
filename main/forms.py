from django import forms

from main.models import Network, Comm, Sound, TempSensorConfig, \
    HumSensorConfig, FlowSensorConfig, PressSensorConfig, PartSensorConfig, \
    Features, Display, Profile

# CHANGE ALL FORMS BY USING add_class template tag instead of setting attrs here!
# {% load widget_tweaks %} {{ field|add_class:"form-control"}} 
# https://pypi.org/project/django-widget-tweaks/


class AchCalibrationForm(forms.Form): 
    reading = forms.CharField(widget=forms.TextInput())
    cfm = forms.CharField(widget=forms.TextInput())
    k_factor = forms.CharField(widget=forms.TextInput())
    height = forms.CharField(widget=forms.TextInput())


class AchSetupForm(forms.Form): 
    volume = forms.CharField(widget=forms.TextInput())
    diameter = forms.CharField(widget=forms.TextInput())
    width = forms.CharField(widget=forms.TextInput())
    height = forms.CharField(widget=forms.TextInput())


class ResetPasswordForm(forms.Form):
    """ Form for the password reset modal. """

    old_password = forms.CharField(widget=forms.TextInput())
    new_password = forms.CharField(widget=forms.TextInput())
    confirm_password = forms.CharField(widget=forms.TextInput())


class DisplayForm(forms.ModelForm):
    """ Form for the display settings modal. """

    class Meta:
        model = Display
        fields = (
            'screen_sleep', 'off_time', 'lock_time',
        )


class ClockForm(forms.Form):
    """ Form for the clock modal. """

    now = forms.CharField(widget=forms.TextInput(attrs={'size':'70'}))


class ProfileForm(forms.ModelForm):
    """ Form for room configuration modal. """

    class Meta:
        model = Profile
        fields = ('title', 'profile_index', 'color', )


class TempSensorForm(forms.Form):
    """ Basic sensor configuration form. Only used for the Temperature sensor. """

    low_alarm = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control bg-danger btn-sm text-white genSensor wrap',}))
    low_warning = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control bg-warning btn-sm text-white genSensor wrap',}))
    high_warning = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control bg-warning btn-sm text-white genSensor wrap',}))
    high_alarm = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control bg-danger btn-sm text-white genSensor wrap',}))

    delay = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}))

    # THIS IS BAD, make a common base class and only add alarm_active_x for all
    # sensors or try to alter it for alarm_active without _x
    alarm_active_temp = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class':'custom-control-input alarm_active',}))


class HumSensorForm(TempSensorForm):
    """ Form for the humidity sensor. """

    alarm_active_hum = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class':'custom-control-input alarm_active',}))
    


class PartSensorForm(TempSensorForm):
    """ Form for the particles sensor. """

    alarm_active_part = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class':'custom-control-input alarm_active',}))
    # delay = forms.CharField(widget=forms.TextInput())


class FlowSensorForm(TempSensorForm):
    """ Form for the airflow sensor. """

    alarm_active_flow = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class':'custom-control-input alarm_active',}))
    # delay = forms.CharField(widget=forms.TextInput())


class PressSensorForm(TempSensorForm):
    """ For of the pressure sensor, which has a negative room. """

    alarm_active_press = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class':'custom-control-input alarm_active',}))

    low_alarm_neg = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control btn-sm bg-danger text-white pressSensor wrap',}))
    low_warning_neg = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control btn-sm bg-warning text-white pressSensor wrap',}))
    high_warning_neg = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control btn-sm bg-warning text-white pressSensor wrap',}))
    high_alarm_neg = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control btn-sm bg-danger text-white pressSensor wrap',}))


class NetworkForm(forms.ModelForm):
    """ Form for the network modal with network name and password. """

    class Meta:
        model = Network
        fields = ('name', 'password',)


class FeaturesForm(forms.ModelForm):
    """ Form for the features modal which allows activating and deactivating 
    all sensor types. """

    class Meta:
        model = Features
        fields = (
            'temperature', 'humidity', 'pressure', 'airflow', 'analog', 'particles', 
        )


class SoundForm(forms.ModelForm):
    """ Form for the sound modal which  allows activating and deactivating the 
    alarm and touch buzzing. """

    class Meta:
        model = Sound
        fields = (
            'alarm', 'touch', 
        )
class CommForm(forms.ModelForm):
    """ Form for the Comm settings modal. """

    class Meta:
        model = Comm
        fields = (
            'bacnet_status', 'baudrate', 'mac_adress', 'object_instance',
        )
