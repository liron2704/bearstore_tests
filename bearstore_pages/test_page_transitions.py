from unittest import TestCase
from selenium import webdriver
from time import sleep

class TestPageTransitions(TestCase):
    def setUp(self):
        # Create a browser object (Open the browser)
        self.driver = webdriver.Chrome()
        # Go to the required URL
        self.driver.get("https://bearstore-testsite.smartbear.com/")
        # Maximize the window
        self.driver.maximize_window()
        # Define a timeout: In case an element is not found - wait 10 seconds
        self.driver.implicitly_wait(10)

    def test_one(self):
        pass


    def tearDown(self):
        sleep(2)
        self.driver.quit()