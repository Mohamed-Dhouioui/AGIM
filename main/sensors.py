#!/usr/bin/env python

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os, random, sys, time, csv
from struct import *
from time import sleep
filename = "calibration.csv"
f = open(filename, "w+")

# make debug mode/software testing run on a non-Raspbian Linux distro
try:
    import serial

    from smbus import SMBus

    import Adafruit_DHT
    from Adafruit_DHT import DHT22

    import busio
    import digitalio
    import board
    import adafruit_mcp3xxx.mcp3008 as MCP
    from adafruit_mcp3xxx.analog_in import AnalogIn

    # Map dht GPIO pins etc. for the two sets of sensors; DHT pins are in BCM numbering
    SENSOR_MAP = [{'dht': 17, 'am1000': MCP.P0, 'analog': MCP.P2, 'press': 0x29},
        {'dht': 17, 'am1000': MCP.P0, 'analog': MCP.P2, 'press': 0x29}]

    # globally defined smbus and multiplexer, required for repeated calls
    # (might not need to be a global anymore)
    bus = SMBus(1)    
    # plexer = Multiplex(bus)
except:
    Adafruit_DHT = None
    DHT22 = None


# DEPRECATED
# class Multiplex:
#     """ I2C multiplexer controller. First pressure sensor is channel 1, 
#     second channel 2. """
    
#     def __init__(self, bus, address=0x70):
#         self.bus = bus
#         self.address = address

#     def channel(self, channel=0):  # values 0-3 indictae the channel, anything else (eg -1) turns off all channels
#         """ Switch the I2C channel """  

#         if (channel==0): action = 0x04
#         elif (channel==1): action = 0x05
#         elif (channel==2): action = 0x06
#         elif (channel==3): action = 0x07
#         else: action = 0x00

#         self.bus.write_byte_data(self.address, 0x04, action)  #0x04 is the register for switching channels 


class DHT:
    def __init__(self, sensor=DHT22, pin=17):
        """ Initialize with the sensor type and the data pin (in BCM). """

        self.sensor, self.pin = sensor, pin

    def read(self):
        """ Return humidity and temperature. """

        return Adafruit_DHT.read_retry(self.sensor, self.pin)


# from https://github.com/Thomas-Tsai/pms3003-g3
# it'd be nice to prettify this
class Particles:
    def __init__(self, console="/dev/ttyS0", debug=False):
        """ Initialize the sensor. """

        self.console, self.debug = console, debug
        if self.debug: print("init")
        self.endian = sys.byteorder
    
    def conn_serial_port(self, device):
        """ Connect to a serial device. """

        if self.debug: print(device)
        self.serial = serial.Serial(device, baudrate=9600)
        if self.debug: print("conn ok")

    def check_keyword(self):
        """ Validate sensor functionality. """

        if self.debug: print("check_keyword")
        while True:
            token = self.serial.read()
            token_hex = token.hex()
            if self.debug: print(token_hex)
            if token_hex == '42':
                if self.debug: print("get 42")
                token2 = self.serial.read()
                token2_hex=token2.hex()
                if self.debug: print(token2_hex)
                if token2_hex == '4d':
                    if self.debug: print("get 4d")
                    return True
                elif token2_hex == '00': # fixme
                    if self.debug: print("get 00")
                    token3 = self.serial.read()
                    token3_hex=token3.hex()
                    if token3_hex == '4d':
                        if self.debug: print("get 4d")
                        return True
            
    def vertify_data(self, data):
        """ Verify the data returned by the sensor. """

        if self.debug: print(data)
        n = 2
        total = int('42',16) + int('4d',16)
        for i in range(0, len(data)-4, n):
            total = total + int(data[i:i+n],16)
        versum = int(data[40]+data[41]+data[42]+data[43], 16)

        if self.debug: print(total)
        if self.debug: print(versum)
        if total == versum: print("data correct")
    
    def read_data(self):
        """ Read the particle sensor data and close the connection. """

        data = self.serial.read(22)
        data_hex = data.hex()
        if self.debug: self.vertify_data(data_hex)
        pm1_cf = int(data_hex[4]+data_hex[5]+data_hex[6]+data_hex[7],16)
        pm25_cf = int(data_hex[8]+data_hex[9]+data_hex[10]+data_hex[11],16)
        pm10_cf = int(data_hex[12]+data_hex[13]+data_hex[14]+data_hex[15],16)
        pm1 = int(data_hex[16]+data_hex[17]+data_hex[18]+data_hex[19],16)
        pm25 = int(data_hex[20]+data_hex[21]+data_hex[22]+data_hex[23],16)
        pm10 = int(data_hex[24]+data_hex[25]+data_hex[26]+data_hex[27],16)
        if self.debug: print("pm1_cf: "+str(pm1_cf))
        if self.debug: print("pm25_cf: "+str(pm25_cf))
        if self.debug: print("pm10_cf: "+str(pm10_cf))
        if self.debug: print("pm1: "+str(pm1))
        if self.debug: print("pm25: "+str(pm25))
        if self.debug: print("pm10: "+str(pm10))
        data = [pm1_cf, pm10_cf, pm25_cf, pm1, pm10, pm25]
        self.serial.close()

        return data

    def read(self):
        """ Connect to the particles sensor at the given address and run
        read_data. """

        tty = self.console
        self.conn_serial_port(tty)
        if self.check_keyword() == True:
            self.data = self.read_data()
            if self.debug: print(self.data)
            return self.data


# Pressure sensor control commands
# ASC_DLHR default address.
# DEPRECATED
ASC_DLHR_I2CADDR = 0x29

# ASC_DLHR Commands
ASC_DLHR_SINGLE_READ_CMD = 0xAA
ASC_DLHR_AVG2_READ_CMD   = 0xAC
ASC_DLHR_AVG4_READ_CMD   = 0xAD
ASC_DLHR_AVG8_READ_CMD   = 0xAE
ASC_DLHR_AVG16_READ_CMD  = 0xAF

# ASC_DLHR Status bits
ASC_DLHR_STS_ZERO          = 0b10000000
ASC_DLHR_STS_PWRON         = 0b01000000
ASC_DLHR_STS_BUSY          = 0b00100000
ASC_DLHR_STS_MODE          = 0b00011000
ASC_DLHR_STS_EEPROM_CHKERR = 0b00000100
ASC_DLHR_STS_SNSCFG        = 0b00000010
ASC_DLHR_STS_ALUERR        = 0b00000001


class Pressure:
    def __init__(self, mode=ASC_DLHR_I2CADDR, address=ASC_DLHR_I2CADDR, i2c=None,
                 sensor_range=1.0, sensor_type=2, **kwargs):
        """ Initialize the pressure sensor. """

        # Check that mode is valid.
        # if mode != 0x29:
        #     raise ValueError('Unexpected address'.format(mode))
        self._mode, self.sensor_range, self.sensor_type = mode, sensor_range, sensor_type
        self.bus = i2c

    def write_cmd(self, cmd):
        """ Write a command to the pressure sensor. """

        self.bus.write_i2c_block_data(self._mode, cmd, [0x00, 0x00])
        time.sleep(0.01)

    def chk_busy(self):
        """ Check if the pressure sensor is busy right now. """

        Status = self.bus.read_byte(self._mode)
        
        if (Status & ASC_DLHR_STS_BUSY):
            print("\033[31;1m\r\nPower On status not set!\033[0;39m")
            return 1 # sensor is busy
        return 0     # sensor is ready
        
    def read(self):
        """ Read the pressure sensor. """

        self.write_cmd(ASC_DLHR_SINGLE_READ_CMD)

        outb = [0,0,0,0,0,0,0,0]
    
        time.sleep(0.04)
        self.retry_num = 5
        while self.retry_num > 0:
            if self.chk_busy():
                print("\033[31;1m\r\nSensor is busy!\033[0;39m")
                time.sleep(0.01)                       # Sleep for 100ms
            else:
                self.retry_num = 0
            self.retry_num = self.retry_num - 1

        outb = self.bus.read_i2c_block_data(self._mode, 0, 7)
        StatusByte = outb[0]

        time.sleep(0.01)
        
        # Check for correct status
        if (StatusByte & ASC_DLHR_STS_PWRON) == 0:
            print("\033[31;1m\r\nPower On status not set!\033[0;39m")
            quit()
        if (StatusByte & ASC_DLHR_STS_SNSCFG):
            print("\033[31;1m\r\nIncorrect sensor CFG!\033[0;39m")
            quit()
        if (StatusByte & ASC_DLHR_STS_EEPROM_CHKERR):
            print("\033[31;1m\r\nSensor EEPROM Checksum Failure!\033[0;39m")
            quit()
            
        # Ccnvert Temperature data to degrees C:
        Tmp = outb[4] << 8
        Tmp += outb[5]
        fTemp = float(Tmp)
        fTemp = (fTemp/65535.0) * 125.0 - 40.0
        
        # Convert Pressure to %Full Scale Span ( +/- 100%)
        Prs = (outb[1] <<16) + (outb[2]<<8) + (outb[3])
        iPrs = (outb[1] <<16) + (outb[2]<<8) + (outb[3])
        Prs -= 0x7FFFFF
        fPress = (float(Prs))/(float(0x800000))
        fPress *= 100.0

        fiPress = 1.25*((iPrs - (0.5*float(0x1000000) ) ) / float(0x1000000) ) * (self.sensor_range * self.sensor_type)
        with open('calibration.csv','a') as log:
            output = "{}\n".format(fiPress)
            log.write(output)    
        def read_cell(x, y):
            with open('calibration.csv', 'r') as f:
                reader = csv.reader(f)
                y_count = 0
                for n in reader:
                    if y_count == y:
                        cell = n[x]
                        return cell
                    y_count += 1 
        data1 = float(read_cell(0,0))
        pressure =(1.25*((iPrs - (0.5*float(0x1000000) ) ) / float(0x1000000) ) * 1) - data1        
        fiPress = pressure
        return fiPress


# DEPRECATED
# def set_I2C_channel(index):
#     """ Set I2C channel to index. """

#     global plexer

#     plexer.channel(index)


def read_all(sensor_set=1, DEBUG=False):
    """ Read all implemented sensors and return their values in a dictionary.
    If DEBUG=True, simulated values are returned instead. sensor_set is
    either 1 or 2, depending on which set of sensors needs to be read. """

    global bus, plexer    


    if DEBUG:          
        # static good state for tests
        temp = 24.0  # good state
        hum = 50.0  # good state
        part = "222"  # good state
        press = 10 
        flow = 1025  # good state
        analog = random.randint(0, 100)
    else:
        temp = random.randint(18, 20)
        hum = random.randint(30, 31)

        if hum == None or temp == None or hum > 99.0:
            hum, temp = "false", "false"
        else:
            hum, temp = round(hum, 2), round(temp, 2)

        # this will need a try except = "false" as well probably
        flow = round(read_AM1000(channel=SENSOR_MAP[sensor_set-1]['am1000']))
        #flow = 1025
        # ANALOG OFF FOR NOW
        # analog = read_analog(channel=SENSOR_MAP[sensor_set-1]['analog'])
        analog = 0
        # DIFFERENT SENSOR SETS NEED TO BE DEFINED FOR THESE!

        if sensor_set == 2:
            try: 
                part = "222"
                #part = Particles().read()  # how is 'part' to be interpreted anyway?
                #part = part[0] + part[1]
                #part = str(part[0]) + str(part[1]) + str(part[2])
            except:
                part = "false"  # reading failed, keep old value
            
            #part = str(2) + str(random.randint(0, 5)) + str(random.randint(0, 5))  # only good sensor states
        else:
            try:
                part = "222"
                #part = Particles().read()  # how is 'part' to be interpreted anyway?
                #part = part[0] + part[1]
               #part = str(part[0]) + str(part[1]) + str(part[2])
            except:
                part = "false"  # reading failed, keep old value

        # set_I2C_channel(sensor_set)
        address = SENSOR_MAP[sensor_set-1]['press']

        try:
            #press = 0.0
            press = round(Pressure(mode=address, address=address, i2c=bus).read(), 4)
            #print("good press",press)                        
        except Exception as e:
            print(e)
            press = 0.000123
        #   press = "false"
            print("busy")

    return {'temp': temp, "hum": hum, 'press': press, 'flow': flow, 
        'analog': analog, 'part': part} 

def read_press(sensor_set=1, DEBUG=False):
    global bus, plexer 
    address = SENSOR_MAP[sensor_set-1]['press']
    try:
        press = round(Pressure(mode=address, address=address, i2c=bus).read(), 4)
        print("good press",press) 
        #print("good press",press)                        
    except Exception as e:
            print(e)
            press = 0.000123
            print("busy")         
    return {'press': press}   

def read_analog(channel):
    """ Read the value of the analog sensor for the given channel. """

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel on pin 0
    return AnalogIn(mcp, channel).value  # Could be voltage instead


def read_AM1000(channel):
    """ Read the value of the airflow sensor for the given channel. """

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel and convert voltage to meters per second
    value = 3.0 * (AnalogIn(mcp, channel).voltage / 4.5)

    return value * 3600  # convert from m³/s to m³/h

def read_ACH(sensor_set=1, DEBUG=False):
    flow = round(read_AM1000(channel=SENSOR_MAP[sensor_set-1]['am1000']))
    return {'flow': flow}

if __name__ == "__main__":
    # Change to True to test simulated sensor reads
    print(read_ACH(1, False))
    print(read_ACH(2, False))
    # set_I2C_channel(1)
