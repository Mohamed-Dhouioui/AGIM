#!/bin/sh
sleep 10
cd /home/pi/Desktop/AGIM
python3 manage.py runserver 0.0.0.0:8000 &

sudo /usr/bin/chromium-browser --no-sandbox --no-first-run --window-size=1920,1080 --noerrdialogs --start-fullscreen --start-maximized --disable-notifications --disable-infobars --kiosk --incognito http://localhost:8000
