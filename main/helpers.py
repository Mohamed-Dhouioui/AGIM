import os, subprocess

from stat import ST_MODE
from pwd import getpwuid


# Path to WPA_SUPPLICANT
WPA_SUPPlICANT = '/etc/wpa_supplicant/wpa_supplicant.conf'

# Template for writing WPA_SUPPLICANT
WPA_TEMPLATE = """network={
    ssid="%s"
    psk="%s"
    priority=1
}"""


def change_network(name, password):
    """ Change the network defined in wpa_supplicant. """

    wpa = WPA_TEMPLATE % (name, password) 
    replace_parameters(WPA_SUPPlICANT, wpa, 'network={\n', 5)
    subprocess.call(['sudo service networking restart'], shell=True)


# these might be a bit much just for wpa_supplicant
def write_access(func):
    """ Decorator which gives a function write access to system files. """

    def func_wrapper(path, *args):           
        if not os.path.isfile(path):  # create file if it doesn't exist
            subprocess.call(['touch ' + path], shell=True)   

        owner = getpwuid(os.stat(path).st_uid).pw_name
        perms = oct(os.stat(path)[ST_MODE])[-3:]
        subprocess.call(['sudo chgrp pi ' + path], shell=True)
        subprocess.call(['sudo chmod g=rw ' + path], shell=True)

        return_value = func(path, *args)

        subprocess.call(['sudo chmod ' + perms + ' ' + path], shell=True)
        subprocess.call(['sudo chgrp ' + owner + ' ' + path], shell=True)

        return return_value

    return func_wrapper


# DRAGON: THIS ASSUMES THERE IS A NEWLINE IN WPA_SUPPlICANT AFTER A FRESH INSTALL [PROBABLY]
@write_access
def replace_parameters(path, parameters, start_line, block_length):
    """ Open a system configuration file, find a line start_line, delete block_length
    lines and add in parameters. """

    with open(path, 'r') as f:
        data = f.readlines()

    # if no wlan0/network is defined, nothing is to delete
    try:
        index = data.index(start_line)
        del data[index: index+block_length]
    except:
        pass

    content = ''.join(data)
    content += parameters

    with open(path, 'w') as f:
        f.write(content)
