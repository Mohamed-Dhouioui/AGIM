# AGIM

## Installation

### System setup

Download the latest Raspbian Buster from https://www.raspberrypi.org/downloads/ and burn it onto an sd card.
Create a file named 'ssh' in /boot, unmount the sd card, put it into the RPi, connect the RPi and
the host with an ethernet cable, then boot the RPi. Find the RPis IP address with an IP scanner (e.g. Angry IP Scanner)
and log into the RPi with

    ssh pi@IP

and the password 'raspberry'.
Enter in the terminal

    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install xvfb -y

Download the repository

    cd /home/pi
    git clone https://github.com/mbadr-ca/AGIM.git

Install rmate [ONLY FOR MY SETUP!]

    HOST:
    [ssh-keygen]
    ssh-copy-id pi@RPI_IP
    ssh-add
    RPI:
    sudo wget -O /usr/local/bin/rsub https://raw.github.com/aurora/rmate/master/rmate
    sudo chmod a+x /usr/local/bin/rsub

If libraries can't be installed with certificate issues, set the system date with

    sudo date -s "Tue Oct 22 11:49:11 UTC 2019"

Install apt packages

    sudo apt-get install python3-dev sqlite3 x11-xserver-utils xutils -y

Install requirements

    sudo pip3 install -r requirements.txt

Install Firefox and Geckodriver

    sudo apt-get install firefox-esr -y
    wget https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-arm7hf.tar.gz
    tar xf geckodriver-v0.21.0-arm7hf.tar.gz
    sudo chmod a+x geckodriver
    sudo mv geckodriver /usr/bin/
    rm geckodriver-v0.21.0-arm7hf.tar.gz

Install DHT22

    sudo python3 -m pip install --upgrade pip setuptools wheel
    sudo pip3 install Adafruit_DHT

Install ADC driver for AM1000

    sudo pip3 install adafruit-circuitpython-mcp3xxx


### Configuration

Disable screen sleep
    sudo nano /etc/lightdm/lightdm.conf

    Add this line

    xserver-command=X -s 0 dpms


//This didn't work >    DISPLAY=:0 xset s off

Enable I2C

    sudo raspi-config
    Goto Interfaces, I2C, select YES

Disable automatic time update:

    timedatectl set-ntp 0

[TODO]
//Force NTPD to update date/time 
sudo timedatectl set-ntp True //To get the right time
sudo timedatectl set-ntp False // to disable it and be able to sync time with the hwclock

RTC DS1307 setup:
    I guess address is 0x68
//Update timezone for Django server 
GO to agim/settings.py
    https://pimylifeup.com/raspberry-pi-rtc/

Add to /boot/config.txt

    dtoverlay=i2c-rtc,ds1307

    sudo apt-get -y remove fake-hwclock
    sudo update-rc.d -f fake-hwclock remove

    sudo nano /lib/udev/hwclock-set

Configure git

    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"
    
## Config File
    sudo nano /boot/config.txt
    dtoverlay=uart1, txd1_pin14, rxd1_pin=15
    gpio=14, 15=a5
    gpio=36, 37=a2
    gpio=16, 17=a2
    

### Autostart

Create an Desktop entry 

    /home/pi/.config/autostart/autoAGIM.desktop

and fill it with

    [Desktop Entry]
    Type=Application
    Exec=/home/pi/AGIM/start.sh
    Hidden=false
    X-GNOME-Autostart-enabled=true
    Name[en_US]=AutoAGIM
    Name=AutoAGIM
    Comment=Start AGIM when GNOME starts

### Initialize database

    python3 manage.py loaddata main/fixtures/data.json

## Pin map
(BOARD numbering)

7 DHT set1
13 DHT set2


## Sensors

Dht22 Adafruit

PM2.5 Air Quality Sensor Adafruit

AM1000 Series MEMS

    https://www.servoflo.com/mass-flow-sensors/siargo-mass-flow-sensors/1300-am1000

dlhr-f50d

    https://www.allsensors.com/products/dlhr-f50d
    I2C 0x29


General analog sensor (?)
    
RTC DS1307 


## Usage

Run testserver:

    cd agim
    python3 manage.py runserver 0.0.0.0:8000

Access the page in the browser of a connected machine. Browse to:

    RPI_IP:8000

Repopulate database (WARNING: this deletes all measurements!)

    python3 manage.py loaddata main/fixtures/data.json


## Non-Raspbian Linux Setup

If you want to run AGIM on a non-Raspbian Linux distro for improved performance,
you only need to perform these steps:

    cd ~
    git clone https://github.com/mbadr-ca/AGIM.git
    sudo apt-get install python3-dev sqlite3 x11-xserver-utils xutils xvfb -y
    cd ~/AGIM
    sudo pip3 install -r requirements.txt

Then, install the Geckodriver which fits your system.

## Software tests

Install the right selenium driver from here

    https://github.com/mozilla/geckodriver/releases/tag/v0.26.0

Like

    wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
    tar xf geckodriver-v0.26.0-linux64.tar.gz
    rm geckodriver-v0.19.1-arm7hf.tar.gz
    sudo chmod a+x geckodriver
    sudo mv geckodriver /usr/local/bin/


### Run the unit tests
Test server does not need to run.

    python3 manage.py test main/tests/

### Run the functional tests

    python3 manage.py test main.functional_tests.test_sensors

### Test the physical alarm (RPi only)

    python3 manage.py test main.functional_tests.test_physical_alarm

### Coverage 
Define files that should be ommited in .coveragerc

    coverage run --source='.' manage.py test main
    sudo coverage html

Open /htmlcov/index.html in browser to see the results.
