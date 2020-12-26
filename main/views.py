import datetime, glob, json, math, shutil, subprocess, time, serial, sys, requests , random
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseServerError
from django.contrib import auth, messages
from django.core.exceptions import FieldDoesNotExist
from threading import Thread
from main.models import Measurement, Configuration, Sound, Network, \
    Features, Display, Comm, Password, TempSensorConfig, HumSensorConfig,\
    FlowSensorConfig, PartSensorConfig, PressSensorConfig, Profile

from main.forms import ProfileForm, TempSensorForm, HumSensorForm, PartSensorForm,\
    SoundForm, FlowSensorForm, PressSensorForm, NetworkForm, FeaturesForm, \
    ClockForm, DisplayForm, CommForm,  ResetPasswordForm, AchSetupForm, AchCalibrationForm

from main.sensors import read_all
from main.sensors import read_press, read_ACH

from main.helpers import change_network

from main.constants import *

from unittest import mock


# Set this to True to use simulated sensor data, False for real sensor reads
DEBUG = False

# buzzer pin
ALARM_PIN = 27
#Var to checn h2o or Pa
inH2O = False 
# make debug mode/software testing run on a non-Raspbian Linux distro
try:
    import RPi.GPIO as GPIO

     # Prolly already has been set by an import
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(ALARM_PIN, GPIO.OUT)
except:
    GPIO = mock.Mock
    GPIO.LOW, GPIO.HIGH = None, None
    GPIO.output = mock.Mock


# Map sensor name to sensor model (needs to remain here to prevent circular import)
SENSOR_MAPPING = {'temp': TempSensorConfig, 'hum': HumSensorConfig, 
    'press': PressSensorConfig, 'flow': FlowSensorConfig, 'part': PartSensorConfig}

def Speed0(request):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    ser.write(b'm0*')
    data = "Speed0"  
    print("Speed0")
    return redirect("/")
    #return render(request, '/', {'data': data})
def Speed1(request):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    ser.write(b'm1*')
    data = "Speed1"
    print("Spee1")
    return redirect("/")
def Speed2(request):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    ser.write(b'm2*')
    data = "Speed2"  
    return redirect("/")
    #return render(request, '/', {'data': data})
def Speed3(request):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    ser.write(b'm3*')
    data = "Speed3"
    return redirect("/")
def Speed4(request):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    ser.write(b'm4*')
    data = "Speed4"
    return redirect("/")
def Speed5(request):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    ser.write(b'm5*')
    data = "Speed5"
    return redirect("/")
def datastring(request):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    ser.write(b'hc800Reading*')
    data = ser.readline().decode("ascii")
    return JsonResponse({'data': data})
    #return render(request, '/', {'data': data})
def uvOn(request):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    ser.write(b'uv1*')
    data = "uvOn"  
    return redirect("/")
def uvOff(request):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    ser.write(b'uv0*')
    data = "uvOff"  
    return redirect("/")
def hepaLifeReset(request):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    ser.write(b'hepaLifeReset*')
    data = ser.readline().decode("ascii") 
    return JsonResponse({'data': data})


def store_data(request):
    """ Store the database on an USB stick. """

    source_path = '/home/pi/AGIM/db.sqlite3'
    target_path = glob.glob('/media/pi/*')[0] + '/db.sqlite3'
    shutil.copyfile(source_path, target_path)

    return HttpResponse()


# can this be fused with change_display_type?
# Could be done with setattr(config, 'log_interval', int(request.POST['log_interval']))
# and request.META['HTTP_REFERER'], but try to remove as many get requests with redirects as possible
def change_log_interval(request):
    """ Update the data logging interval. """

    config = Configuration.objects.get()
    config.log_interval = int(request.POST['log_interval'])
    config.save()

    return redirect("/main/view_data")


def change_display_type(request):
    """ Change the data display type for a single room or both. """

    config = Configuration.objects.get()
    config.display_type = int(request.POST['display_type'])
    config.save()

    return redirect("/main/view_data")


def erase_data(request):
    """ Erase all measurements.  """

    Measurement.objects.all().delete()
    return redirect("/main/view_data")


def set_press_average(request):
    reads = []
    config = Configuration.objects.get()
   
    for i in range(25):
        data = read_press(config.active_profile.room_index, DEBUG)['press']
        #data = read_all(config.active_profile.room_index, DEBUG)['press']
        print('before reads',data)
        #if data != None:
        if data != 0.000123:
            reads.append(data)
            print('good reads',data)
    #if inH2O == False:
     #   average = sum(reads) * 249 /len(reads)
    #    print('avg inside', average)   
    average = sum(reads) /len(reads)


    # This is a hacked solution that should be improved
    profiles = Profile.objects.filter(room_index=config.active_profile.room_index)

    for profile in profiles:       
        sensor = PressSensorConfig.objects.get(profile=profile)
        if  (sensor.in_h2o is True):        
            sensor.average = average
            sensor.save()
        if  (sensor.in_h2o is False):      
            sensor.average = average * 248.84
            sensor.save()        

    return JsonResponse({})


def calculate_duct(sensor):
    if sensor.square:
        return round(sensor.width*sensor.height, 2)

    return round(math.pow((sensor.diameter/2), 2) * math.pi, 2)


def set_flow_average(request):
    reads = []
    config = Configuration.objects.get()
    
    for i in range(200):        
        data = read_ACH(config.active_profile.room_index, DEBUG)['flow']
        print('Ach data',data);
        if data != None:
            reads.append(data)

    average = sum(reads)/len(reads)
    print('Ach average',average);
    # This is a hacked solution that should be improved
    profiles = Profile.objects.filter(room_index=config.active_profile.room_index)

    for profile in profiles:
        sensor = FlowSensorConfig.objects.get(profile=profile)
        sensor.average = average
        sensor.save()

    return JsonResponse({})


# ideally, one function to return all data, reads + configuration, which accepts a parameter
# to decide if the data will be logged
def get_sensors(request):
    """ Return configuration of all sensors and their current reads. """

    config = Configuration.objects.get()
    try:
        data = read_all(config.active_profile.room_index, DEBUG)
        press_sensor = PressSensorConfig.objects.get(profile=config.active_profile)
        if  (press_sensor.in_h2o is True):
            data['press'] = round(float(data['press'])  - float(press_sensor.average), 2)
        else:    
            data['press'] = round(float(data['press']) * float(248.84) - float(press_sensor.average), 2)
        
        print('data.sensor',data['press'])
        flow_sensor = FlowSensorConfig.objects.get(profile=config.active_profile)
        data['flow'] = calculate_airflow(config.active_profile, data['flow'], flow_sensor.metric)
        return JsonResponse(gather_all_data(data, config))
    except:
        return JsonResponse()


def gather_all_data(data, config):
    result = {}

    for name, sensor in SENSOR_MAPPING.items():
        current_sensor = sensor.objects.get(profile=config.active_profile)
        result[name] = {'value': data[name], **gather_sensor_data(name, current_sensor)}

    result['analog'] = {'value': data['analog']}

    return result


def gather_sensor_data(name, sensor):
    """ Gather all sensor configuration in a dict. """

    result = {'low_alarm': sensor.low_alarm,
              'low_warning': sensor.low_warning,
              'high_alarm': sensor.high_alarm,
              'high_warning': sensor.high_warning,
              'active': "true" if sensor.alarm_active else "false",
              'delay': sensor.delay}

    if name == 'flow':
        result['metric'] = "true" if sensor.metric else "false"

    if name == 'temp':
        result['celsius'] = "true" if sensor.celsius else "false"

    if name == 'press':
        result['negative'] = "true" if sensor.negative_room else "false"
        result['in_h2o'] = "true" if sensor.in_h2o else "false" 
        result['low_alarm_neg'] = sensor.low_alarm_neg
        result['low_warning_neg'] = sensor.low_warning_neg
        result['high_warning_neg'] = sensor.high_warning_neg
        result['high_alarm_neg'] = sensor.high_alarm_neg       

    return result


def update_sensor(request):
    """ Update a sensors configuration depending on type. Sanitize input, set 
    active state and delay, configure unit for airflow sensor, update also 
    negative room configuration for the pressure sensor. """

    config = Configuration.objects.get()
    sensor = SENSOR_MAPPING[request.POST.get('sensor_type')].objects.get(
        profile=config.active_profile)

    # this can be compressed into a single line
    # Automatic casting of variable type is not so good
    sensor.low_alarm = sanitize(request.POST.get('low_alarm'))
    sensor.low_warning = sanitize(request.POST.get('low_warning'))
    sensor.high_warning = sanitize(request.POST.get('high_warning'))
    sensor.high_alarm = sanitize(request.POST.get('high_alarm'))

    set_special_sensor_attributes(request, sensor)

    sensor.save()

    return HttpResponse(json.dumps({}), content_type="application/json")


def set_special_sensor_attributes(request, sensor):
    """ Set the sensor attributes alarm_active, delay, metric for flow
    and call a function to set the pressure sensor attributes. """

    sensor.alarm_active = request.POST.get('alarm_active') == "true"
    # print('\n\nblablal')
    # print(sensor.alarm_active)
    sensor.delay = request.POST.get('delay')

    if request.POST['sensor_type'] == "flow":
        sensor.metric = request.POST.get('metric') == "true"

    if request.POST['sensor_type'] == "temp":
        sensor.celsius = request.POST.get('celsius') == "true"

    if request.POST['sensor_type'] == "press":
        set_press_attributes(request, sensor)


def set_press_attributes(request, sensor):
    """ Set the specific pressure sensor attributes. """

    sensor.in_h2o = request.POST.get('in_h2o') == "true"
    sensor.negative_room = request.POST.get('negative_room') == "true"

    sensor.low_alarm_neg = sanitize(request.POST['low_alarm_neg'])
    sensor.low_warning_neg = sanitize(request.POST['low_warning_neg'])
    sensor.high_alarm_neg = sanitize(request.POST['high_alarm_neg'])
    sensor.high_warning_neg = sanitize(request.POST['high_warning_neg'])    


def sanitize(value):
    """ Remove all units from value. """

    to_remove = ['Pa', '-', '°C', '%', 'in H2O', 'F']

    for unit in to_remove:
        value = value.replace(unit, '')

    return value.strip()


def get_network_json(request):
    """ Return network configuration as JSON. """

    if request.method == 'GET':
        network = get_object_or_404(Network)

        return JsonResponse({'name': network.name, 'password': network.password,})

    raise Http404


def get_achsetup_json(request):
    """ Return ach setup as JSON. """

    if request.method == 'GET':
        config = Configuration.objects.get()
        sensor = FlowSensorConfig.objects.get(profile=config.active_profile)

        return JsonResponse({'volume': sensor.volume, 'square': sensor.square,
            'diameter': sensor.diameter, 'width': sensor.width, 'height': sensor.height,})

    raise Http404


# BUG: this should use the average of 10 live sensor values!
# but it's better to implement that after changing sensors.py to 
# be able to read just a specific sensor
def get_achcalibration_json(request):
    """ Return ach calibration as JSON. """

    if request.method == 'GET':
        config = Configuration.objects.get()
        sensor = FlowSensorConfig.objects.get(profile=config.active_profile)

        return JsonResponse({'k_factor': sensor.k_factor, 'average': sensor.average,
            "duct": calculate_duct(sensor), 'is_metric': sensor.metric})

    raise Http404


def calculate_airflow(profile, sensor_read, is_metric):
    sensor = FlowSensorConfig.objects.get(profile=profile)
    try:
        if is_metric:
            result = ((sensor_read - sensor.average) * 0.013634 * calculate_duct(sensor) / 1000000
                * sensor.k_factor * 60) / sensor.volume
            print(result)
            return round(result, 2)
        else:
            result = ((sensor_read - sensor.average) * 0.013634 * calculate_duct(sensor) * 82 / 100000000
                * sensor.k_factor * 60) / sensor.volume * 35.3147
            return round(result, 2)            
    except Exception as e:  # probably sensor.volume was 0
        print("\n\nException raised in calculate airflow, prolly volume is 0!!!\n\n")
        return 0


# could be fused to toggle_alarm with a GET parameter
def alarm_on(request):
    """ Turn on the alarm pin. """

    if Sound.objects.get().alarm:
        print("alarm on")
        GPIO.output(ALARM_PIN, GPIO.HIGH)
    return HttpResponse()


def alarm_off(request):
    """ Turn off the alarm pin. """

    print("alarm off")
    GPIO.output(ALARM_PIN, GPIO.LOW)
    return HttpResponse()


def touch_alarm(request):
    """ Touch alarm for one second if it is activated. """

    # only fire touch alarm if the alarm is not already on
    if Sound.objects.get().touch and GPIO.input(ALARM_PIN) == GPIO.LOW:
        print("\nTouch alarm\n")
        GPIO.output(ALARM_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(ALARM_PIN, GPIO.LOW)
    return HttpResponse()


def get_display_json(request):
    """ Return display configuration as JSON. """

    if request.method == 'GET':
        display = get_object_or_404(Display)

        return JsonResponse({
            'screen_sleep': display.screen_sleep,
            'off_time': display.off_time,
            'lock_time': display.lock_time,
            })

    raise Http404


def update_display(request):
    """ Update the display configuration via its form. If a screen blank time
    was set, configure that. """

    form = DisplayForm(request.POST, 
        instance=get_object_or_404(Display))
    if form.is_valid():
        form.save()
        messages.success(request, 'Display updated')
    else:
        messages.error(request, 'Error updating Display')

    off_time = 'off'
    if form['screen_sleep'].value():       
        off_time = form['off_time'].value()

    subprocess.call(["DISPLAY=:0 xset s " + off_time], shell=True)

    return HttpResponse(json.dumps({}), content_type="application/json")


def update_achsetup(request):
    # maybe move all of these into function get_current_sensor(SensorType)
    config = Configuration.objects.get()
    
    # this is a hacked solution which should be improved
    profiles = Profile.objects.filter(room_index=config.active_profile.room_index)
    for profile in profiles:
        sensor = FlowSensorConfig.objects.get(profile=profile)

        sensor.volume = request.POST.get('volume')
        sensor.square = request.POST.get('round') == 'false'
        sensor.diameter = request.POST.get('diameter')
        sensor.width = request.POST.get('width')
        sensor.height = request.POST.get('height')
        sensor.save()

    return HttpResponse(json.dumps({}), content_type="application/json")


def update_achcalibration(request):
    # maybe move all of these into function get_current_sensor(SensorType)
    config = Configuration.objects.get()
    
    # this is a hacked solution which should be improved
    profiles = Profile.objects.filter(room_index=config.active_profile.room_index)
    for profile in profiles:
        sensor = FlowSensorConfig.objects.get(profile=profile)

        sensor.k_factor = request.POST.get('k_factor')
        sensor.save()

    return HttpResponse(json.dumps({}), content_type="application/json")


def set_clock(request):
    """ Set the system date, then the hardware clock with the datetime string 
    from the request. """

    date_time_obj = datetime.datetime.strptime(request.POST['now'], '%Y-%m-%d %H:%M %p')
    date_str = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')

    command = 'sudo hwclock --set --date="' + date_str + '"'

    try:
        subprocess.call([command], shell=True)
        subprocess.call(['sudo hwclock -s'], shell=True)
    except:
        print("\n\n No hardware clock installed, can't set it!\n\n")

    return HttpResponse(json.dumps({}), content_type="application/json")


# Should use a form as well
def update_network(request):
    """ Update network configuration. """

    # Could use form validation as well
    config = Configuration.objects.get()
    config.network.name = request.POST.get('name')
    config.network.password = request.POST.get('password')
    config.network.save()

    change_network(config.network.name, config.network.password)

    return HttpResponse(json.dumps({}), content_type="application/json")


def get_profile_json(request, room, profile):
    """ Return room configuration as JSON for a given room and profile index. """

    if request.method == 'GET':
        profile = get_object_or_404(Profile, room_index=room, profile_index=profile)
        return JsonResponse({
            'title': profile.title,
            'color': profile.color,
        })
    raise Http404


def toggle_room(request, room):
    """ Update config after room switch and return profile information JSON. """

    profile = Profile.objects.get(room_index=room, is_active=True)
    config = Configuration.objects.get()
    config.active_profile = profile
    config.save()

    return profile_data_as_json(profile)


# could be partially fused with toggle_room
def toggle_profile(request, profile_index):
    """ Update config after profile switch and return profile information JSON. """

    config = Configuration.objects.get()

    old_profile = config.active_profile
    new_profile = Profile.objects.get(room_index=old_profile.room_index, 
        profile_index=profile_index)
    old_profile.is_active = False
    new_profile.is_active = True
    old_profile.save()
    new_profile.save()
    
    config.active_profile = new_profile
    config.save()

    return profile_data_as_json(new_profile)


def profile_data_as_json(profile):
    return JsonResponse({
        'title': profile.title,
        'color': profile.color,
        'profile_index': profile.profile_index,
        'room_index': profile.room_index})


def update_profile(request):
    """ Update the current profile with a POST request. """

    room_index = request.POST.get('room_index')
    profile_index = request.POST.get('profile_index')

    form = ProfileForm(request.POST, 
        instance=get_object_or_404(Profile, 
            room_index=room_index, profile_index=profile_index))

    if form.is_valid():
        form.save()

    config = Configuration.objects.get()
    profile = Profile.objects.get(room_index=room_index, profile_index=profile_index)
    config.active_profile = profile
    config.save()

    return HttpResponse(json.dumps({}), content_type="application/json")


def set_password_state(request):
    """ Set password activation state. """

    pwd_model = Password.objects.get()
    pwd_model.active = request.POST['state'] == "true"
    pwd_model.save()

    return JsonResponse({})


def get_features_json(request):
    """ Return feature activation as JSON response. """
    global features_menu
    features = Features.objects.get()
    print("\n\n===================================================>\n")
    features_menu = {}
    features_menu['temperature'] = features.temperature
    features_menu['humidity'] = features.humidity
    features_menu['pressure'] = features.pressure
    features_menu['airflow'] = features.airflow
    features_menu['analog'] = features.analog
    features_menu['particles'] = features.particles
    print(features_menu)
    print("\n===================================================>\n\n")
    return JsonResponse({
        'temp': features.temperature,
        'hum': features.humidity,
        'press': features.pressure,
        'flow': features.airflow,
        'analog': features.analog,
        'part': features.particles,})


# this function should be generalized for all update functions
def update_features(request):
    """ Validate and store feature activation form. """

    form = FeaturesForm(request.POST, 
        instance=get_object_or_404(Features))
    if form.is_valid():
        form.save()
        for i in form.cleaned_data.keys():
            features_menu[i]= form.cleaned_data.get(i)
            print(features_menu[i])
    return HttpResponse(json.dumps({}), content_type="application/json")


def log_sensor(room):
    """ Log data for a sensor set for the given room. """

    data = read_all(room, DEBUG)
    features = Features.objects.get()

    part = data['part'] if (data['part'] != 'false' and features.particles) else None
    temp = data['temp'] if (data['temp'] != 'false' and features.temperature) else None
    hum = data['hum'] if (data['hum'] != 'false' and features.humidity) else None
 
    config = Configuration.objects.get()
    press_sensor = PressSensorConfig.objects.get(profile=config.active_profile)

    press = None
    if data['press'] != 'false' and features.pressure: 
        press = round(data['press'] - press_sensor.average, 2)

    flow = None
    if data['flow'] != 'false' and features.airflow:
        flow = calculate_airflow(config.active_profile, data['flow'], False)

    # features modal misses analog so far
    analog = data['analog'] if features.analog else None
    print("Measurment",temp, hum,press,flow,analog,part,room)
    Measurement(temperature=temp, humidity=hum, 
        pressure=press, airflow=flow, analog=analog, 
        particles=part, room=room)



# this should be combined with gathering sensor data for display; a parameter should
# be passed to decide if the data should be logged
def log_sensors(request):
    """ Read all sensors and store their measurements. """

    log_sensor(1)
    log_sensor(2)

    return HttpResponse()


def update_sound(request):
    """ Validate and store sound configuration form. """

    form = SoundForm(request.POST, 
        instance=get_object_or_404(Sound))
    if form.is_valid():
        form.save()
        messages.success(request, 'Sound updated')
    else:
        messages.error(request, 'Error updating sound')

    return HttpResponse(json.dumps({}), content_type="application/json")


def get_sound_json(request):
    """ Return feature activation as JSON response. """

    sound = Sound.objects.get()

    return JsonResponse({
        'alarm': sound.alarm,
        'touch': sound.touch,})


def verify_password(request):
    """ Return a json success if the request has the correct password and a 
    json error else. """

    config = Configuration.objects.get()

    if config.password.password != request.POST['password']:
        return HttpResponseServerError(json.dumps({'error': 'An error occured'}))

    return JsonResponse({"success": 'true'})


def reset_password(request):
    """ Set password if the old password was entered correctly and the
    new password was entered twice correctly. """

    config = Configuration.objects.get()

    if request.POST['old_password'] == config.password.password:
        if request.POST['new_password'] == request.POST['confirm_password']:
            config.password.password = request.POST['new_password']
            config.password.save()
            config.save()

    return redirect("/main/view_password")

def get_comm_json(request):
    try:
        """ Return comm configuration as JSON. """
        print('\n\n=============================================>\n\n')
        if request.method == 'GET':
            comm = get_object_or_404(Comm)
        print('======================================================>')
        return JsonResponse({
            'bacnet_status': comm.bacnet_status,
            'baudrate': comm.baudrate,
            'mac_adress': comm.mac_adress,
            'object_instance': comm.object_instance
            })
    except:
        print('===================>ERROR<=========================')


def update_comm(request):
    """ Update the display configuration via its form. If a screen blank time
    was set, configure that. """
    try:
        form = CommForm(request.POST, 
            instance=get_object_or_404())
        print('==================================================================>')
        if form.is_valid():
            form.save()
            messages.success(request, 'Comm updated')
        else:
            messages.error(request, 'Error updating Comm')
        return HttpResponse(json.dumps({}), content_type="application/json")
    except Exception as e:
        print('=================================================================>\n')
        print(e)
        print('\n\n=============================================================>\n\n')


def view_main(request):
    """ Main view. Sets the screen lock time if necessary. Passes all necessary forms 
    to the main template. """

    config = Configuration.objects.get()

    alarm_off(None)  # turn off any running alarm on page load    

    lock_time = 0
    if config.password.active:
        # if the screen is blank, it needs to be locked on wakeup anyway,
        # therefore lock_time can't be higher than off_time
        lock_time = min(config.display.off_time, config.display.lock_time)

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M %p')
    clock_form = ClockForm(initial={'now': now})

    return render(request, 'frame.html', {'config': config, 'profile_form': ProfileForm, 
        'temp_sensor_form': TempSensorForm, 'view_type': 'main', 'network_form': NetworkForm,
        "log_seconds": INTERVAL_MAP[config.log_interval], "features_form": FeaturesForm,
        'clock_form': clock_form, 'display_form': DisplayForm, 'comm_form' : CommForm,
        'lock_time': lock_time, 'hum_sensor_form': HumSensorForm, 'flow_sensor_form': FlowSensorForm, 
        'press_sensor_form': PressSensorForm, 'part_sensor_form': PartSensorForm, 
        'sound_form': SoundForm, "achsetup_form": AchSetupForm, "achcalibration_form": AchCalibrationForm})


def view_data(request):
    """ View for the data display page. Sensor data for only one room or both is
    passed for display. """

    config = Configuration.objects.get()

    if config.display_type == 0:
        measurements = Measurement.objects.filter(room=1)
    elif config.display_type == 1:
        measurements = Measurement.objects.filter(room=2)
    else:
        measurements = Measurement.objects.all()

    return render(request, 'frame.html', {'measurements': 
        measurements, 'view_type': 'data', 'config': config, 
        'log_intervals': LOG_INTERVALS, "log_seconds": INTERVAL_MAP[config.log_interval],    
        'display_types': DISPLAY_TYPES}) 


def view_password(request):
    """ View for the password reset and activation page. """

    config = Configuration.objects.get()
    return render(request, 'frame.html', {'view_type': 'password', 
        'config': config, 'reset_password_form': ResetPasswordForm,})     
