import time

from selenium.webdriver.firefox.webdriver import WebDriver

from pyvirtualdisplay import Display

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class FunctionalTest(StaticLiveServerTestCase):
    fixtures = ['data.json']
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.display = Display(visible=0)  # set this to 1 to show the tests
        cls.display.start()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)  

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        cls.display.stop()
        super().tearDownClass()

    def enter_with_keyboard(self, text):
        keyboard = self.selenium.find_element_by_css_selector('.ui-keyboard-preview')
        keyboard.clear()

        for key in text:
            keyboard.send_keys(key)
            time.sleep(0.5)

        accept = self.selenium.find_element_by_css_selector('div.ui-keyboard-keyset:nth-child(2) > button:nth-child(57)')
        accept.click()