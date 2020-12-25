import imp
import sys
import os
import ConfigParser

from dlhr import *
sensorhw = imp.load_source('dlhr', 'dlhr.py')
sensorasc = sensorhw.ASC_DLHR(mode=ASC_DLHR_I2CADDR)
while True:
        sensorasc.write_cmd(ASC_DLHR_SINGLE_READ_CMD)
        sensorasc.read_sensor()
    