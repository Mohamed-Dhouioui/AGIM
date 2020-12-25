import time

from unittest import mock

from .base import FunctionalTest

from main.models import Profile, PressSensorConfig, TempSensorConfig


# It would be better to mock the alarm, but the view is imported by the test
# server runner, similar to
# https://stackoverflow.com/questions/55602100/in-django-how-to-mock-an-object-method-called-by-views-py-during-its-import
# See also
# https://stackoverflow.com/questions/20481804/django-unit-tests-failing-when-run-with-other-test-cases?noredirect=1

class SiteAccessibilityTest(FunctionalTest):
    def test_site_access(self):
        self.selenium.get(self.live_server_url)
        assert 'Abatement Technologies' in self.selenium.title


class SensorTresholdTest(FunctionalTest):
    def test_user_can_alter_sensor_treshold(self):
        # Bob opens the main page and sees (simulated) sensor reads.
        self.selenium.get(self.live_server_url)
        time.sleep(10)
        # He wants to alter the treshold of the temp sensor and clicks its button.
        self.selenium.find_element_by_id('tempBtn').click()

        # He notes that a virtual keyboard pops up after he clicks into the input
        self.selenium.find_element_by_id('id_low_alarm').click()

        # He enters 18 as the new value
        self.enter_with_keyboard("18")

        # He sees that the value has changed to what he typed
        assert self.selenium.find_element_by_id('id_low_alarm').get_attribute('value') == "18"

        # Then, Bob clicks the update button. The modal closes and when Bob opens
        # it again, he sees the field for low_alarm has changed to the new value.
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(2)
        self.selenium.find_element_by_id('tempBtn').click()
        assert self.selenium.find_element_by_id('id_low_alarm').get_attribute('value') == "18 °C"

    def test_user_can_discard_altered_sensor_treshold(self):
        self.selenium.get(self.live_server_url)
        # He wants to alter the treshold of the temp sensor and clicks its button 
        # and then the input.
        self.selenium.find_element_by_id('tempBtn').click()
        # old_value = self.browser.find_element_by_id('id_low_alarm').get_attribute('value')
        # new_value = str(int(old_value.strip(' °C')) + 1)
        self.selenium.find_element_by_id('id_low_alarm').click()

        # He enters a different value
        self.enter_with_keyboard("10")

        # Then, Bob clicks the close button. The modal closes and when Bob opens
        # it again, he sees the field for low_alarm has not changed its value.
        close = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > button:nth-child(2)") 
        close.click()
        time.sleep(2)
        self.selenium.find_element_by_id('tempBtn').click()

        default = str(int(TempSensorConfig.low_alarm.field.default)) + ' °C'
        assert self.selenium.find_element_by_id('id_low_alarm').get_attribute('value') == default
    
    def test_warning_then_alarm_is_fired_when_high_treshold_is_surpassed(self): 
        self.selenium.get(self.live_server_url)
        time.sleep(5)
        btn_html = self.selenium.find_element_by_id('tempBtn').get_attribute('outerHTML')
        assert "border-color: rgb(68, 157, 68);" in btn_html
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == False

        # He wants to alter the treshold of the temp sensor and clicks its button 
        # and then the input.
        self.selenium.find_element_by_id('tempBtn').click()

        # He enters a high value for the warning input which
        # surpasses the static 24°C the dummy sensor reading returns
        self.selenium.find_element_by_id('id_high_warning').click()        
        self.enter_with_keyboard("22")

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # He notices that the temp sensor button border turns yellow and that  
        # the alarm button did not pop up
        btn_html = self.selenium.find_element_by_id('tempBtn').get_attribute('outerHTML')

        assert "border-color: yellow;" in btn_html
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == False

        # Bob then reopens the modal and enters a low value for high alarm
        self.selenium.find_element_by_id('tempBtn').click()
        self.selenium.find_element_by_id('id_high_alarm').click()        
        self.enter_with_keyboard("23")

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # He notices that the temp sensor button border turns red, the alarm 
        # button popped up and that a physical alarm was triggered
        btn_html = self.selenium.find_element_by_id('tempBtn').get_attribute('outerHTML')
        assert "border-color: red;" in btn_html
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == True

    def test_warning_then_alarm_is_fired_when_low_warning_treshold_is_surpassed(self):
        self.selenium.get(self.live_server_url)
        time.sleep(5)
        btn_html = self.selenium.find_element_by_id('tempBtn').get_attribute('outerHTML')
        assert "border-color: rgb(68, 157, 68);" in btn_html
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == False

        # He wants to alter the treshold of the temp sensor and clicks its button 
        # and then the input.
        self.selenium.find_element_by_id('tempBtn').click()

        # He enters a high value for the warning input which
        # surpasses the static 24°C the dummy sensor reading returns
        self.selenium.find_element_by_id('id_low_warning').click()        
        self.enter_with_keyboard("25")

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # He notices that the temp sensor button border turns yellow 
        btn_html = self.selenium.find_element_by_id('tempBtn').get_attribute('outerHTML')
        assert "border-color: yellow;" in btn_html

        # Bob then reopens the modal and enters a high value for low alarm
        self.selenium.find_element_by_id('tempBtn').click()
        self.selenium.find_element_by_id('id_low_alarm').click()        
        self.enter_with_keyboard("25")

        # He notices that the alarm is enabled for the temp sensor        
        assert self.selenium.find_element_by_css_selector('#id_alarm_active_temp').get_attribute('value') == 'on'

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # He notices that the temp sensor button border turns red, the alarm 
        # button popped up and that a physical alarm was triggered
        btn_html = self.selenium.find_element_by_id('tempBtn').get_attribute('outerHTML')
        assert "border-color: red;" in btn_html
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == True       

    def test_no_alarm_fired_when_alarm_is_disabled(self):
        # Bob wants to disable the alarm for the temperature sensor and verify
        # that no alarm fires, but the button layout still changed 
        self.selenium.get(self.live_server_url)
        time.sleep(5)
        btn_html = self.selenium.find_element_by_id('tempBtn').get_attribute('outerHTML')
        assert "border-color: rgb(68, 157, 68);" in btn_html
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == False

        # He wants to alter the treshold of the temp sensor and clicks its button 
        # and then the input
        self.selenium.find_element_by_id('tempBtn').click()
        time.sleep(2)
        assert self.selenium.find_element_by_id('id_alarm_active_temp').is_selected() == True
        self.selenium.execute_script("document.getElementById('id_alarm_active_temp').click();") 
        assert self.selenium.find_element_by_id('id_alarm_active_temp').is_selected() == False

        # He enters a high value for the warning and the alarm input which
        # surpasses the static 24°C the dummy sensor reading returns
        self.selenium.find_element_by_id('id_high_warning').click()        
        self.enter_with_keyboard("22")
        self.selenium.find_element_by_id('id_high_alarm').click()        
        self.enter_with_keyboard("23")

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # He notices that the temp sensor button border turns red, but no alarm is triggered
        btn_html = self.selenium.find_element_by_id('tempBtn').get_attribute('outerHTML')
        assert "border-color: red;" in btn_html
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == False      

    def test_unit_conversion(self):
        # Bob wants to test the temperature unit conversion. He opens
        # the temp sensor modal and clicks on the Fahrenheit button
        self.selenium.get(self.live_server_url)
        time.sleep(5)
        btn_html = self.selenium.find_element_by_id('tempBtn').get_attribute('outerHTML')

 
        self.selenium.find_element_by_id('tempBtn').click()
        self.selenium.find_element_by_id('tempFahrenheit').click()        

        # Bob confirms, the modal closes
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)
        assert self.selenium.find_element_by_id('temperature').get_attribute('innerHTML') == str(round((24 * 1.8) + 32.0)) + ' F'

    def test_alarm_is_fired_but_can_be_turned_off_by_readjusting_treshold(self):
        self.selenium.get(self.live_server_url)
        time.sleep(5)

        # Bob then opens the temperature modal and enters a high value for low alarm
        self.selenium.find_element_by_id('tempBtn').click()
        self.selenium.find_element_by_id('id_low_alarm').click()        
        self.enter_with_keyboard("25")

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # He notices that the alarm button popped up 
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == True

        # Now, Bob reopens the modal, enters a value below 24 for the low_alarm,
        # updates and sees that the alarm goes away
        self.selenium.find_element_by_id('tempBtn').click()
        self.selenium.find_element_by_id('id_low_alarm').click()        
        self.enter_with_keyboard("21")

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # He notices that the alarm button popped up 
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == False

    def test_switch_profile_changes_tresholds(self):
        self.selenium.get(self.live_server_url)
        time.sleep(5)

        # Bob notices that the current profile is Profile 1
        assert self.selenium.find_element_by_id('dropdownMenuLink').get_attribute('innerHTML') == "Profile 1"
        # Bob wants to see if switching the profile shows different tresholds indeed.
        # For this, he first changes the low_alarm treshold for the current profile
        self.selenium.find_element_by_id('tempBtn').click()
        self.selenium.find_element_by_id('id_low_alarm').click()        
        self.enter_with_keyboard("18")

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # Bob now goes to a different profile, opens the temp sensor modal
        # and sees that its value is the default, 18
        self.selenium.find_element_by_id('dropdownMenuLink').click()
        self.selenium.find_element_by_id('profile_link_3').click()
        time.sleep(2)

        self.selenium.find_element_by_id('tempBtn').click()
        assert self.selenium.find_element_by_id('id_low_alarm').get_attribute('value') == "19 °C" 

    def test_switch_room_changes_tresholds(self):
        self.selenium.get(self.live_server_url)
        time.sleep(5)

        # Bob notices that the current room is Room 1
        assert "display: block;" in self.selenium.find_element_by_id('menu_room_1').get_attribute('outerHTML')
        assert "display: none;" in self.selenium.find_element_by_id('menu_room_2').get_attribute('outerHTML')

        # Bob wants to see if switching the rooms shows different tresholds indeed.
        # For this, he first changes the low_alarm treshold for the current profile of the current room
        self.selenium.find_element_by_id('tempBtn').click()
        self.selenium.find_element_by_id('id_low_alarm').click()        
        self.enter_with_keyboard("18")

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # Bob now goes to room 2, opens the temp sensor modal
        # and sees that its value is the default, 18
        self.selenium.find_element_by_css_selector('#link_room_2 > li:nth-child(1) > a:nth-child(1)').click()
        time.sleep(2)

        self.selenium.find_element_by_id('tempBtn').click()
        assert self.selenium.find_element_by_id('id_low_alarm').get_attribute('value') == "19 °C" 

    def test_alarm_button_surpresses_alarm_but_reappears_for_other_sensor(self):
        # Bob wants to test the button to turn the alarm off
        self.selenium.get(self.live_server_url)
        time.sleep(5)

        # Bob then opens the modal and enters a high value for low alarm
        self.selenium.find_element_by_id('tempBtn').click()
        self.selenium.find_element_by_id('id_low_alarm').click()        
        self.enter_with_keyboard("25")

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#tempForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # He notices that the temp sensor button border turns red, the alarm 
        # button popped up and that a physical alarm was triggered
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == True

        # He then presses the alarm button; it goes away and does not come back
        self.selenium.find_element_by_id('alarmBtn').click()
        time.sleep(10)
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == False

        # Now, he opens the humidity sensor and changes the low alarm treshold
        # above 50 as delivered by the dummy sensor reading function
        # Bob then opens the modal and enters a high value for low alarm 
        self.selenium.find_element_by_id('humBtn').click()
        self.selenium.find_element_by_css_selector('.configure-hum modal-body > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)').click()        
        self.enter_with_keyboard("51")

        # He activates the sensor
        self.selenium.execute_script("document.getElementById('id_alarm_active_hum').click();")
        assert self.selenium.find_element_by_id('id_alarm_active_temp').is_selected() == True

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#humForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # He notices that the temp sensor button border turns red, the alarm 
        # button popped up and that a physical alarm was triggered
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == True


class PressSensorTest(FunctionalTest):
    def test_negative_room_warning_then_alarm_is_fired_when_low_warning_treshold_is_surpassed(self):

        profile = Profile.objects.get(room_index=1, profile_index=1)
        sensor = PressSensorConfig.objects.get(profile=profile)
        sensor.low_alarm_neg = 5
        sensor.low_warning_neg = 2
        sensor.high_warning_neg = 1
        sensor.high_alarm_neg = 1
        sensor.save()
        # Bob has a negative pressure room and wants to validate the sensor functionality
        # for it. He opens the pressure sensor modal and clicks the negative room button.
        self.selenium.get(self.live_server_url)
        time.sleep(5)

        # He clicks the button of the pressure sensor and then the button for the negative room.
        self.selenium.find_element_by_id('pressBtn').click()
        time.sleep(1)
        self.selenium.find_element_by_id('negBtn').click()
        time.sleep(1)

        # He notices low_warning has a negative value of -2 Pa
        assert self.selenium.find_element_by_id('id_low_warning_neg').get_attribute('value') == "- 2 Pa"

        # Bob confirms the new treshold values, the modal closes
        update = self.selenium.find_element_by_css_selector("#pressForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # He notices that the press sensor value display is negative and
        # that the button border turned yellow 
        assert self.selenium.find_element_by_id('pressure').get_attribute('innerHTML') == "-3 Pa"
        btn_html = self.selenium.find_element_by_id('pressBtn').get_attribute('outerHTML')
        assert "border-color: yellow;" in btn_html

        # Bob opens the pressure modal again and notices that the low_alarm field
        # became -2 Pa magically
        sensor.low_alarm_neg = 2
        sensor.save()
        self.selenium.find_element_by_id('pressBtn').click()
        time.sleep(1)
        self.selenium.find_element_by_id('negBtn').click()
        time.sleep(1)

        assert self.selenium.find_element_by_id('id_low_warning_neg').get_attribute('value') == "- 2 Pa"

        # Bob confirms, the modal closes
        update = self.selenium.find_element_by_css_selector("#pressForm > div:nth-child(2) > div:nth-child(3) > input:nth-child(1)") 
        update.click()
        time.sleep(5)

        # He notices that the press sensor button border turns red, the alarm 
        # button popped up and that a physical alarm was triggered
        btn_html = self.selenium.find_element_by_id('pressBtn').get_attribute('outerHTML')
        assert "border-color: red;" in btn_html
        assert self.selenium.find_element_by_id('alarmBtn').is_displayed() == True

