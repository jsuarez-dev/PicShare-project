# Test
from unittest import TestLoader, TestSuite
from pyunitreport import HTMLTestRunner
# Local 
from functional_test import *
# Utilites
import os

PATH_DRIVER = './chromedriver'

os.set

basic_test = TestLoader().loadTestsFromTestCase(RunServerTest)
user_sign = TestLoader().loadTestsFromTestCase(SignUpTest)
user_login = TestLoader().loadTestsFromTestCase(LoginTest)

suite_test = TestSuite([basic_test, user_sign, user_login])

kwargs = {
    "output": 'AI-gram-report'
}

runner = HTMLTestRunner(**kwargs)
runner.run(suite_test)
