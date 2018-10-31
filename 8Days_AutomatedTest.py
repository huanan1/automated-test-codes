from applitools.eyes import Eyes
from applitools import logger
from applitools.logger import StdoutLogger

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import sys
import string
import random
# FileLogger does not work
# from applitools.logger import FileLogger
# logger.set_logger(FileLogger("eyes.log"))

logger.set_logger(StdoutLogger())
sys.stdout = open('file.txt', 'w')


class EightDays:
    def __init__(self, testname):
        self.eyes = Eyes()
        self.eyes.api_key = 'IlUcgRAO105BlmoORdtUxbK8CUKg3KRSa8q4f3iACoY1I110'

        desired_caps = {
            "platformName": 'Android',
            "platformVersion": '8.0.0',
            "deviceName": "Android Emulator",
            "automationName": "UiAutomator2",
            # "nativeWebScreenshot": "True",
            "app": 'C:/Users/Tea/Desktop/BCA/8Days/Automated/mobile.apk'
        }

        # need to start appium or this won't happen
        self.wd = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
        # 127.0.0.1 is your localhost and 4723 is the port
        # http://localhost:4723/wd/hub
        self.wd.implicitly_wait(10)  # wait for the page to load
        self.eyes.open(driver=self.wd, app_name='8days', test_name=testname)
        # The string passed to checkWindow() is typically a descriptive name that identifies the checkpoint.

    def select_language(self):
        self.wd.find_element_by_id("kr.co.the8days.dev:id/radioEnglish").click()
        self.wd.find_element_by_id("kr.co.the8days.dev:id/btnNext").click()

        sleep(2)
        self.wd.hide_keyboard()

    def find_login_fields(self):
        self.userField = self.wd.find_element_by_id("kr.co.the8days.dev:id/edtSignInEmail")
        self.pwField = self.wd.find_element_by_id("kr.co.the8days.dev:id/edtSignInPassword")
        self.login_btn = self.wd.find_element_by_id("kr.co.the8days.dev:id/btnSignIn")

    def basic_login(self):
        self.find_login_fields()

        self.userField.send_keys("keysilenc@gmail.com")
        self.pwField.click()
        self.delete_field(self.pwField)

        self.pwField.send_keys("golden1")
        self.login_btn.click()

    '''general functions'''

    def delete_field(self, field):
        actions = TouchAction(self.wd)
        actions.long_press(field).release().perform()
        self.wd.press_keycode(67)

    def screenshot(self, name):
        self.eyes.check_window(name)

    def click_by_id(self, id):
        self.wd.find_element_by_id(id).click()


class EightDays_Login(EightDays):
    def __init__(self, testname):
        super().__init__(testname)

    def start(self):
        self.eyes.check_window('Language Selection')

        self.wd.find_element_by_id("kr.co.the8days.dev:id/radioEnglish").click()
        self.eyes.check_window("Selected Language")

        self.wd.find_element_by_id("kr.co.the8days.dev:id/btnNext").click()
        self.wd.implicitly_wait(10)
        sleep(2)
        self.wd.hide_keyboard()
        self.eyes.check_window("Login page")

    def wrong_user(self):

        super().find_login_fields()
        self.userField.click()
        self.userField.send_keys("thisemaildoesnotexist@gmail.com")
        self.pwField.click()
        self.pwField.send_keys("fakepassword1")

        self.login_btn.click()

        self.eyes.check_window("Non-existent user")
        self.wd.find_element_by_id("kr.co.the8days.dev:id/btnDialogOk").click()

    def invalid_login_formats(self):
        self.find_login_fields()

        self.userField.click()
        self.delete_field(self.userField)
        self.pwField.click()
        self.delete_field(self.pwField)

        self.wd.implicitly_wait(5)
        self.eyes.check_window("login fields error messages")

    def wrong_pw(self):
        self.find_login_fields()

        self.userField.send_keys("keysilenc@gmail.com")
        self.pwField.send_keys("wrong1")
        self.login_btn.click()
        self.eyes.check_window("wrong pw for existing user")
        self.wd.find_element_by_id("kr.co.the8days.dev:id/btnDialogOk").click()

    def login(self):
        self.find_login_fields()

        self.userField.send_keys("keysilenc@gmail.com")
        self.pwField.click()
        self.delete_field(self.pwField)

        self.pwField.send_keys("golden1")
        self.login_btn.click()
        self.eyes.check_window("select account")

    def test_logins(self):
        self.start()
        self.wrong_user()
        self.invalid_login_formats()
        self.wrong_pw()
        self.login()

    def just_login(self):
        self.start()
        self.login()
    ''' Using the App '''

    def swipe_right_to_left(self):
        actions = TouchAction(self.wd)
        actions.press(x=998, y=998).move_to(x=180, y=989).release().perform()

    def user_guide(self):
        LG_display = self.wd.find_element_by_xpath("//android.widget.TextView[@text='LG Display']")
        LG_display.click()

        for i in range(1, 4):
            self.eyes.check_window(f"user guide page {i}")
            self.swipe_right_to_left()
            if i == 3:
                TouchAction(self.wd).press(x=542, y=1090).release().perform()

        y = 1000
        while True:
            try:
                self.wd.find_element_by_xpath("//android.widget.TextView[@text= 'Today Menu']")
            except (StaleElementReferenceException, NoSuchElementException) as e:
                y -= 50
                TouchAction(self.wd).press(x=542, y=y).release().perform()
            else:
                self.eyes.check_window("Today Menu - Breakfast")
                break

    def today_menu(self):
        self.wd.find_element_by_xpath("//android.widget.ImageView[@index='1']").click()
        self.eyes.check_window("Select Canteen")
        self.wd.find_element_by_id("kr.co.the8days.dev:id/btnCancel").click()

        lunch = self.wd.find_element_by_xpath("//android.widget.TextView[@text='Lunch']")
        lunch.click()
        self.eyes.check_window("Lunch")
        self.wd.find_element_by_xpath("//android.widget.TextView[@text='Dinner']").click()
        self.eyes.check_window("Dinner")

        self.wd.find_element_by_id("kr.co.the8days.dev:id/btnGenerateQRCode").click()
        self.eyes.check_window("QR Code")

        self.wd.find_element_by_id("kr.co.the8days.dev:id/segmentBalance").click()
        self.eyes.check_window("QR Code Balance")

        TouchAction(self.wd).tap(x=550, y=200).perform()
        self.eyes.check_window("Back to Today Menu")

    def weekly_menu(self):
        self.wd.find_element_by_xpath("//android.widget.TextView[@text = 'Weekly Menu']").click()
        self.eyes.check_window("Weekly Menu")
        self.wd.find_element_by_id("kr.co.the8days.dev:id/cafeteriaContainer").click()
        try:
            self.wd.find_element_by_id("kr.co.the8days.dev:id/titleSelector")
        except NoSuchElementException:
            print("The Select Cafetarias option did not pop up upon clicking the canteen drop-down bar in the Weekly Menu page")
            pass
        self.wd.find_element_by_id("kr.co.the8days.dev:id/btnCancel").click()

    def history(self):
        self.wd.find_element_by_xpath("//android.widget.TextView[@text = 'History']")
        self.screenshot("History")

    def into_app(self):
        self.user_guide()

    def tearDown(self):
        try:
            self.eyes.close()

        finally:
            self.wd.quit()
            self.eyes.abort_if_not_closed()


class EightDays_SignUp(EightDays):
    def __init__(self, testname):
        super().__init__(testname)

    def start(self):
        while True:
            try:
                self.wd.find_element_by_id("kr.co.the8days.dev:id/radioEnglish").click()
                self.wd.find_element_by_id("kr.co.the8days.dev:id/btnNext").click()
            except NoSuchElementException:
                sleep(2)
            else:
                break

    def into_signup(self):
        sleep(2)
        self.wd.hide_keyboard()
        self.click_by_id("kr.co.the8days.dev:id/btnSignUp")
        self.screenshot("Agree to privacy policy")
        self.click_by_id("kr.co.the8days.dev:id/btnReadPrivacyPolicy")
        self.screenshot("privacy policy")
        self.click_by_id("kr.co.the8days.dev:id/btnBack")
        self.click_by_id("kr.co.the8days.dev:id/tglPrivacyPolicy")
        try:
            self.click_by_id("kr.co.the8days.dev:id/btnNext")

        except WebDriverException:
            print("Next button not ready for clicking yet")
            sleep(1)
            self.click_by_id("kr.co.the8days.dev:id/btnNext")

        self.screenshot("Sign up - your information")

    def signup_by_email(self, email, name, password):
        email_field = self.wd.find_element_by_id("kr.co.the8days.dev:id/edtEmailAddress")
        email_field.send_keys(email)
        name_field = self.wd.find_element_by_id("kr.co.the8days.dev:id/edtName")
        name_field.send_keys(name)
        pw_field = self.wd.find_element_by_id("kr.co.the8days.dev:id/edtYourPassword")
        pw_field.send_keys(password)
        self.wd.find_element_by_id("kr.co.the8days.dev:id/edtRetypeYourPassword").send_keys(password)
        sleep(1)
        self.wd.find_element_by_id("kr.co.the8days.dev:id/btnNext").click()
        self.wd.implicitly_wait(1)
        self.screenshot("Activate your account page")
        sleep(1)
        self.click_by_id("kr.co.the8days.dev:id/edtCode1").send_keys("1")
        ActionChains(self.wd).send_keys("2345").perform()
        self.screenshot("Invalid code error message")
        # sleep(300)  # sleep for 5 minutes
        # self.screenshot("Time's up")
        self.click_by_id("kr.co.the8days.dev:id/btnClose")


test = EightDays_Login("8Days Login")
test.just_login()
test.into_app()
test.today_menu()

test2 = EightDays_SignUp("8Days Sign Up")
test2.start()
test2.into_signup()
test2.signup_by_email("fakeemail@email.com", "Testing", "somepw1")
