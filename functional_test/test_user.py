"""Functional tests of AI-gram  a social network for artificial intelligent"""
# Py unit report
from pyunitreport import HTMLTestRunner
# Tests
import unittest
# Browser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class LoginTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(executable_path=r'/Users/johan/Dev-courses/Django-course/platzigram/functional_test/chromedriver')
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(15)
        cls.driver.get('http://127.0.0.1:8000/users/login/')

    def test_login(self):

        search_field = self.driver.find_element_by_id('username')
        search_field.clear()
        search_field.send_keys('me123')
        passwd = self.driver.find_element_by_id('passwd')
        passwd.clear()
        passwd.send_keys('12345')
        self.driver.implicitly_wait(40)
        passwd.submit()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as variable:
            return False
        return True


if __name__ == "__main__":
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reports', report_name='AI-gram_login_report'))