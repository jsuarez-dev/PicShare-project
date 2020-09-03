"""Functional tests of AI-gram  a social network for artificial intelligent"""
# Py unit report
from pyunitreport import HTMLTestRunner
# Tests
import unittest
# Browser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
# Utils
import time
import pyautogui


class SignUpTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(executable_path=r'/Users/johan/Dev-courses/Django-course/platzigram/functional_test/chromedriver')
        cls.driver.implicitly_wait(15)
        cls.driver.get('http://127.0.0.1:8000/')

    def test_sign_up(self):
        """Sign up in the platform"""
        # Check the redirection
        self.assertEqual(self.driver.current_url, 'http://127.0.0.1:8000/users/login/?next=/')
        # move to sign up url
        sign_up_link = self.driver.find_element_by_link_text('Sign Up')
        sign_up_link.click()
        # fill up fields
        username_field = self.driver.find_element_by_name('username')
        username_field.clear()
        username_field.send_keys('me123')

        password = self.driver.find_element_by_name('email')
        password.clear()
        password.send_keys('me@gmail.com')

        password = self.driver.find_element_by_name('password')
        password.clear()
        password.send_keys('12345')

        password_confirmation = self.driver.find_element_by_name('password_confirmation')
        password_confirmation.clear()
        password_confirmation.send_keys('12345')

        birthday = self.driver.find_element_by_name('birthday')
        birthday.clear()
        birthday.send_keys('10/10/1980')

        first_name = self.driver.find_element_by_name('first_name')
        first_name.clear()
        first_name.send_keys('me')

        last_name = self.driver.find_element_by_name('last_name')
        last_name.clear()
        last_name.send_keys('last')
        # send
        summit = self.driver.find_element_by_xpath('//*[@id="auth-container"]/form/div[7]/div[1]/button')
        summit.click()

        try:
            title = self.driver.find_element_by_class_name('alert')
            self.assertEqual('Username is already use', title.text)
        except NoSuchElementException:
            time.sleep(5)
            title = self.driver.find_element_by_xpath('//*[@id="auth-container"]/div/h3')
            self.assertEqual("We've sent you an confirmation email", title.text)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


class LoginTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(executable_path=r'/Users/johan/Dev-courses/Django-course/platzigram/functional_test/chromedriver')
        cls.driver.implicitly_wait(15)
        cls.driver.get('http://127.0.0.1:8000/')

    def test_login(self):
        username = 'yo123'
        first_name = 'yo'
        last_name = 'me'
        # Check the redirection
        self.assertEqual(self.driver.current_url, 'http://127.0.0.1:8000/users/login/?next=/')
        # Fill up login form
        username_field = self.driver.find_element_by_name('username')
        username_field.clear()
        username_field.send_keys(username)

        password = self.driver.find_element_by_name('password')
        password.clear()
        password.send_keys('12345')
        password.submit()

        self.driver.implicitly_wait(3)

        try:
            title = self.driver.find_element_by_xpath('//*[@id="profile-box"]/form/div[1]/div/h5')
            self.assertEqual(title.text, '@{} | {} {}'.format(username, first_name, last_name))
            # Fill up profile form
            picture = self.driver.find_element_by_xpath('//*[@id="picture_id"]')
            picture.clear()
            picture.send_keys("/Users/johan/Dev-courses/Django-course/platzigram/img_test/profile/img_test.001.png")

            website = self.driver.find_element_by_name('website')
            website.clear()
            website.send_keys('yo123.com')

            biography = self.driver.find_element_by_name('biography')
            biography.clear()
            biography.send_keys("""
                Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the 
                industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and 
                scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap 
                into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the 
                release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing 
                """)

            phone_number = self.driver.find_element_by_name('phone_number')
            phone_number.clear()
            phone_number.send_keys('+61400100100')

            summit_btn = self.driver.find_element_by_xpath('//*[@id="profile-box"]/form/button')
            summit_btn.click()
            time.sleep(5)
            self.driver.implicitly_wait(3)
            self.assertEqual(self.driver.current_url, 'http://127.0.0.1:8000/users/{}/'.format(username))

        except NoSuchElementException:
            self.driver.implicitly_wait(3)
            self.assertEqual(self.driver.current_url, 'http://127.0.0.1:8000/')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reports', report_name='AI-gram_login_report'))