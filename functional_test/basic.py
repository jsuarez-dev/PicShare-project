"""Functional tests of AI-gram  a social network for artificial intelligent"""
# Py unit report
from pyunitreport import HTMLTestRunner
# Tests
import unittest
# Browser
from selenium import webdriver


class RunServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(
            executable_path=r'functional_test/chromedriver'
        )
        cls.driver.implicitly_wait(15)

    def test_running(self):
        self.driver.get('http://127.0.0.1:8000/')
        self.assertIn('AI-gram', self.driver.title)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
