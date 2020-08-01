# Test
from unittest import TestLoader, TestSuite
from pyunitreport import HTMLTestRunner
# Local
from test_basic import RunServerTest
from test_user import LoginTest

basic_test = TestLoader().loadTestsFromTestCase(LoginTest)
user_test = TestLoader().loadTestsFromTestCase(RunServerTest)

suite_test = TestSuite([basic_test, user_test])

kwargs = {
    "output": 'AI-gram-report'
}

runner = HTMLTestRunner(**kwargs)
runner.run(suite_test)