
import time

from .base import FunctionalTest

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

from main.views import ALARM_PIN


class PhysicalAlarmTest(FunctionalTest):
    def test_warning_then_alarm_is_fired_when_high_treshold_is_surpassed(self):
        # Bob wants to see if the physical alarm is actually triggered.
        self.selenium.get(self.live_server_url)
        time.sleep(5)

        assert GPIO.input(ALARM_PIN) == 0

        # # He alters the treshold of the temp sensor and clicks its button 
        # # and then the input.
        self.selenium.find_element_by_id('tempBtn').click()
        self.selenium.find_element_by_id('id_high_alarm').click()        
        self.enter_with_keyboard("23")

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # # He notices that the temp sensor button border turns red, the alarm 
        # # button popped up and that a physical alarm was triggered
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == True
        assert GPIO.input(ALARM_PIN) == 1

    def test_alarm_fired_with_delay(self):
        # Bob wants to see an delayed alarm in action. He goes to the main page,
        # alters the alarm delay input to 10 seconds, sets the high alarm treshold below 24
        # and updates finally
        self.selenium.get(self.live_server_url)
        time.sleep(5)

        self.selenium.find_element_by_id('tempBtn').click()
        self.selenium.find_element_by_css_selector('.configure-temp modal-body > div:nth-child(7) > div:nth-child(2) > input:nth-child(1)').click() 
        self.enter_with_keyboard("10")  
        self.selenium.find_element_by_id('id_high_alarm').click()        
        self.enter_with_keyboard("23")

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()

        assert GPIO.input(ALARM_PIN) == 0

        time.sleep(15)  # needs some overhad to update the db etc.

        # Bob notices a physical alarm after the time delay
        assert GPIO.input(ALARM_PIN) == 1
