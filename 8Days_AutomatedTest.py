from applitools.eyes import Eyes
from applitools import logger
from applitools.logger import StdoutLogger

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import string
import random
# FileLogger does not work
from applitools.logger import FileLogger
logger.set_logger(FileLogger("C:\\Users\\Tea\\Desktop\\BCA\\8Days\\Automated\\eyes.log"))

logger.set_logger(StdoutLogger())

GENERAL_ELEMENTS = {
    'submit_btn': "co.vn.the8days:id/btnSubmit",
    'ok_btn': "co.vn.the8days:id/btnDialogOk",
    'close_btn': "co.vn.the8days:id/btnClose",
    'dialog_title': "co.vn.the8days:id/txtTitle"
}

SETTINGS_ELEMENTS = {
    'SettingsTab': "co.vn.the8days:id/tab_profile",
    'Notice': {'main': "co.vn.the8days:id/btnNotice",
               'in': "co.vn.the8days:id/ic_right",
               'back': "co.vn.the8days:id/btnBack"},

    'ChangePW': {'main': "co.vn.the8days:id/btnChangePassword",
                 'oldpw': 'co.vn.the8days:id/edtOldPassword',
                 'newpw': "co.vn.the8days:id/edtNewPassword",
                 'retype': "co.vn.the8days:id/edtConfirmPassword"},
    'MyAcct': "co.vn.the8days:id/btnMyAccount",
    'AppLanguage': "co.vn.the8days:id/btnAppLanguage",
    'ContactUs': 'co.vn.the8days:id/btnContactUs',
    'privacyPolicy': 'co.vn.the8days:id/btnPrivacyPolicy',
    'logout': "co.vn.the8days:id/btnLogOut"
}


def ran_email():
    ran_str = "".join(random.choice(string.ascii_letters + string.digits) for x in range(7))
    return (ran_str + "@fakemail.com")


class EightDays:
    def __init__(self, testname='8Days Test', language='English'):
        self.eyes = Eyes()
        self.eyes.api_key = 'IlUcgRAO105BlmoORdtUxbK8CUKg3KRSa8q4f3iACoY1I110'
        self.eyes.is_disabled = False
        self.testname = testname
        self.language = language

        desired_caps = {
            "platformName": 'Android',
            "platformVersion": '8.0.0',
            "deviceName": "Android Emulator",
            "automationName": "UiAutomator2",
            # "nativeWebScreenshot": "True",
            "app": 'C:/Users/Tea/Desktop/BCA/8Days/Automated/app-dev-debug.apk'
        }

        # need to start appium or this won't happen
        self.wd = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
        self.wd.implicitly_wait(10)  # wait for the page to load
        self.eyes.open(driver=self.wd, app_name='8days', test_name=testname)

    def select_language(self):
        if 'VN' in self.testname or self.language is 'Vietnamese':
            self.wait_locate("co.vn.the8days:id/radioVietnamese", click=True)
            self.language = 'Vietnamese'

        elif 'KR' in self.testname or self.language is 'Korean':
            self.wait_locate("co.vn.the8days:id/radioKorean", click=True)
            self.language = 'Korean'

        else:
            self.wait_locate("co.vn.the8days:id/radioEnglish", click=True)
            self.language = 'English'

        self.wait_locate("co.vn.the8days:id/btnNext", click=True)
        sleep(2)  # keyboard takes time to appear
        self.wd.hide_keyboard()
        self.eyes.check_window("Login page")

    def find_login_fields(self):
        self.userField = self.wd.find_element_by_id("co.vn.the8days:id/edtSignInEmail")
        self.pwField = self.wd.find_element_by_id("co.vn.the8days:id/edtSignInPassword")
        self.login_btn = self.wd.find_element_by_id("co.vn.the8days:id/btnSignIn")

    def basic_login(self):
        self.find_login_fields()

        self.userField.send_keys("keysilenc@gmail.com")
        self.pwField.click()
        self.delete_field(self.pwField)

        self.pwField.send_keys("golden1")
        self.login_btn.click()

    def tearDown(self):
        try:
            self.eyes.close()

        finally:
            self.wd.quit()
            self.eyes.abort_if_not_closed()

    '''general functions'''

    def delete_field(self, field):
        actions = TouchAction(self.wd)
        actions.long_press(field).release().perform()
        self.wd.press_keycode(67)

    def click_by_id(self, id):
        self.wd.find_element_by_id(id).click()

    def wait_locate(self, locater, click=False):
        if '//' in locater:
            WebDriverWait(self.wd, 10).until(EC.presence_of_element_located((By.XPATH, locater)))

            if click is True:
                try:
                    self.wd.find_element_by_xpath(locater).click()

                except (NoSuchElementException, StaleElementReferenceException) as e:
                    print(f"Unable to find {locater}")
                    raise

            else:
                return self.wd.find_element_by_xpath(locater)

        elif 'id' in locater:
            # this must come later because id is ALWAYS in the locater --> androID
            WebDriverWait(self.wd, 10).until(EC.presence_of_element_located((By.ID, locater)))
            if click is True:
                try:
                    self.wd.find_element_by_id(locater).click()

                except (NoSuchElementException, StaleElementReferenceException) as e:
                    print(f"Unable to find {locater}")
                    raise
            else:
                return self.wd.find_element_by_id(locater)

    def swipe_right_to_left(self):
        actions = TouchAction(self.wd)
        actions.press(x=998, y=998).move_to(x=180, y=989).release().perform()

    def user_guide(self):
        # print(f"Chosen company is {company}")
        # chosen_company = company
        self.wait_locate("co.vn.the8days:id/accCorporate", click=True)
        # self.wd.find_element_by_xpath(f"//android.widget.TextView[@text='{chosen_company}']").click()
        # using f"//android.widget.TextView[@text='{company']" didn't work,
        # neither did it work when f was right in front of '' like f'{}'
        # and this didn't work too ("//android.widget.TextView[@text='" + company + "']")

        for i in range(1, 4):
            self.eyes.check_window(f"user guide page {i}")
            self.swipe_right_to_left()
            if i == 3:
                TouchAction(self.wd).press(x=542, y=1090).release().perform()

        # For different screen sizes where the button might not be exactly at (542,1090)
        # y = 1000
        # while True:
        #     try:
        #         self.wd.find_element_by_xpath("co.vn.the8days:id/btnGenerateQRCode")
        #     except (StaleElementReferenceException, NoSuchElementException) as e:
        #         y -= 50
        #         TouchAction(self.wd).press(x=542, y=y).release().perform()
        #     else:
        #         self.eyes.check_window("Today Menu - Lunch")
        #         break


class EightDays_Login(EightDays):
    def __init__(self, testname='8Days', language='English'):
        super().__init__(testname='8Days', language='English')
        self.testname = testname
        self.language = language

    def wrong_user(self):
        self.find_login_fields()
        self.userField.click()
        self.userField.send_keys("thisemaildoesnotexist@gmail.com")
        self.pwField.click()
        self.pwField.send_keys("fakepassword1")

        self.login_btn.click()

        self.eyes.check_window("Non-existent user")
        self.wd.find_element_by_id("co.vn.the8days:id/btnDialogOk").click()

    def invalid_login_formats(self):
        self.find_login_fields()

        self.userField.click()
        self.delete_field(self.userField)
        self.pwField.click()
        self.eyes.check_window("login fields error messages")

    def wrong_pw(self):
        self.find_login_fields()

        self.userField.send_keys("keysilenc@gmail.com")
        self.pwField.send_keys("wrong1")
        self.login_btn.click()
        self.eyes.check_window("wrong pw for existing user")
        self.wd.find_element_by_id("co.vn.the8days:id/btnDialogOk").click()

    def login(self):
        self.find_login_fields()

        self.userField.send_keys("keysilenc@gmail.com")
        self.pwField.click()
        self.delete_field(self.pwField)

        self.pwField.send_keys("golden1")
        self.login_btn.click()
        self.eyes.check_window("select account")

    def just_login(self):
        self.select_language()
        self.login()
    ''' Using the App '''

    def today_menu(self):
        self.wd.find_element_by_xpath("//android.widget.ImageView[@index='1']").click()
        self.eyes.check_window("Select Canteen")
        self.wd.find_element_by_id("co.vn.the8days:id/btnCancel").click()

        lunch = self.wd.find_element_by_xpath("//android.widget.LinearLayout/android.widget.TextView[2]")
        lunch.click()
        self.eyes.check_window("Lunch")
        self.wd.find_element_by_xpath("//android.widget.TextView[@text='Dinner']").click()
        self.eyes.check_window("Dinner")

        self.wd.find_element_by_id("co.vn.the8days:id/btnGenerateQRCode").click()
        self.eyes.check_window("QR Code")

        self.wd.find_element_by_id("co.vn.the8days:id/segmentBalance").click()
        self.eyes.check_window("QR Code Balance")

        TouchAction(self.wd).tap(x=550, y=200).perform()
        self.eyes.check_window("Back to Today Menu")

    def weekly_menu(self):
        self.click_by_id("co.vn.the8days:id/tab_weeklyMenu")
        self.eyes.check_window("Weekly Menu")
        self.wd.find_element_by_id("co.vn.the8days:id/cafeteriaContainer").click()
        try:
            self.wd.find_element_by_id("co.vn.the8days:id/titleSelector")
        except NoSuchElementException:
            print("The Select Cafetarias option did not pop up upon clicking the canteen drop-down bar in the Weekly Menu page")
            pass
        self.wd.find_element_by_id("co.vn.the8days:id/btnCancel").click()

    def history(self):
        self.wd.find_element_by_xpath("co.vn.the8days:id/tab_data")
        self.screenshot("History")


class EightDays_SignUp(EightDays):
    def __init__(self, testname='8Days', language='English'):
        super().__init__(testname='8Days', language='English')
        self.testname = testname
        self.language = language
        self.select_language()

    def start(self):
        if 'ENG' in self.testname:
            self.wait_locate("co.vn.the8days:id/radioEnglish", click=True)

        elif 'VN' in self.testname:
            self.wait_locate("co.vn.the8days:id/radioVietnamese", click=True)

        elif 'KR' in self.testname:
            self.wait_locate("co.vn.the8days:id/radioKorean", click=True)

        self.wait_locate("co.vn.the8days:id/btnNext", click=True)

    def into_signup(self):
        try:
            self.wait_locate("co.vn.the8days:id/btnSignUp", click=True)
        except NoSuchElementException:
            self.wd.hide_keyboard()
        self.screenshot("Agree to privacy policy")
        self.wait_locate("co.vn.the8days:id/btnReadPrivacyPolicy", click=True)
        self.screenshot("privacy policy")
        self.wait_locate("co.vn.the8days:id/btnBack", click=True)
        self.wait_locate("co.vn.the8days:id/tglPrivacyPolicy", click=True)
        self.wait_locate("co.vn.the8days:id/btnNext", click=True)

        self.screenshot("Sign up - your information")

    def signup_by(self, contact, name, password, resendEmail=False, waitforTimeUp=False):
        if '@' in contact:
            email_field = self.wd.find_element_by_id("co.vn.the8days:id/edtEmailAddress")
            email_field.send_keys(contact)

        else:
            self.click_by_id("co.vn.the8days:id/segmentedPhone")
            self.wd.find_element_by_id("co.vn.the8days:id/edtPhoneNumber").send_keys(contact)

        name_field = self.wd.find_element_by_id("co.vn.the8days:id/edtName")
        name_field.send_keys(name)
        pw_field = self.wd.find_element_by_id("co.vn.the8days:id/edtYourPassword")
        pw_field.send_keys(password)
        self.wd.find_element_by_id("co.vn.the8days:id/edtRetypeYourPassword").send_keys(password)
        sleep(1)
        self.wd.find_element_by_id("co.vn.the8days:id/btnNext").click()
        self.wait_locate("co.vn.the8days:id/edtCode1")
        self.screenshot("Activate your account page")
        # for i in range(1, 6):
        #     field = self.wd.find_element_by_id(f"co.vn.the8days:id/edtCode{i}")
        #     field.click()
        #     field.send_keys(f"{i}")
        # submit btn remains grey if I do this
        self.click_by_id("co.vn.the8days:id/edtCode1")
        actions = ActionChains(self.wd)
        actions.send_keys('12345')
        actions.perform()

        self.wait_locate("co.vn.the8days:id/btnNext", click=True)
        self.wait_locate("co.vn.the8days:id/txtTitle")
        self.screenshot("Invalid code error message")
        self.click_by_id("co.vn.the8days:id/btnDialogOk")

        if resendEmail is True:
            self.click_by_id("co.vn.the8days:id/btnResend")

        if waitforTimeUp is True:
            sleep(300)  # sleep for 5 minutes
            self.screenshot("Time's up")

        self.click_by_id("co.vn.the8days:id/btnClose")


class ForgotPW(EightDays):
    FORGOT_PW = {
        'forgotPW': "co.vn.the8days:id/btnForgotPassword",
        'email_tab': "co.vn.the8days:id/segmentedEmail",
        'email_field': "co.vn.the8days:id/edtEmail",
        'phone_no_tab': "co.vn.the8days:id/segmentedPhone",
        'phoneno_field': "co.vn.the8days:id/edtPhoneNumber",
    }

    def __init__(self, testname='8Days', language='English'):
        super().__init__(testname='8Days', language='English')
        self.testname = testname
        self.language = language

        self.select_language()
        sleep(2)
        self.wd.hide_keyboard()
        self.click_by_id(ForgotPW.FORGOT_PW.get('forgotPW'))
        self.screenshot("Forgot Password Email Tab")

    def non_existent_user_forgot_via_email(self):
        email = ran_email()
        self.wd.find_element_by_id(ForgotPW.FORGOT_PW['email_field']).send_keys(email)
        self.wait_locate(GENERAL_ELEMENTS['submit_btn'], click=True)
        self.screenshot("Non-existent user - Error Message")
        self.click_by_id(GENERAL_ELEMENTS['ok_btn'])

    def non_existent_user_forgot_via_phone(self):
        phone_no = "".join(random.choice(string.digits) for x in range(8))
        self.click_by_id(ForgotPW.FORGOT_PW['phone_no_tab'])
        self.screenshot("Forgot Password Phone Number Tab")
        self.wd.find_element_by_id(ForgotPW.FORGOT_PW['phoneno_field']).send_keys(phone_no)
        self.wait_locate(GENERAL_ELEMENTS['submit_btn'], click=True)
        self.screenshot("Non-existent user - Error Message")
        self.wait_locate(GENERAL_ELEMENTS['ok_btn'], click=True)

    def existing_user_via_email(self, email):
        self.click_by_id(ForgotPW.FORGOT_PW['email_tab'])
        self.wd.find_element_by_id(ForgotPW.FORGOT_PW['email_field']).send_keys(email)
        self.click_by_id(GENERAL_ELEMENTS['ok_btn'])

    def existing_user_via_phone(self, number):
        self.click_by_id(ForgotPW.FORGOT_PW['phone_no_tab'])
        self.wd.find_element_by_id(ForgotPW.FORGOT_PW['phoneno_field']).send_keys(number)
        self.click_by_id(GENERAL_ELEMENTS['ok_btn'])


class changePW(EightDays):
    def __init__(self, testname='8Days', language='English'):
        super().__init__(testname='8Days', language='English')
        self.testname = testname
        self.language = language
        self.select_language()
        self.basic_login()
        self.user_guide()
        self.wait_locate("co.vn.the8days:id/tab_profile", click=True)

    def changePW_get_errors(self):
        self.wd.find_element_by_xpath(SETTINGS_ELEMENTS['SettingsTab']).click()
        self.wait_locate(SETTINGS_ELEMENTS['ChangePW']['main'], click=True)
        self.wd.find_element_by_id(SETTINGS_ELEMENTS['ChangePW']['oldpw']).send_keys("golden1")
        self.wd.find_element_by_id(SETTINGS_ELEMENTS['ChangePW']['newpw']).send_keys("golden12")
        self.wd.find_element_by_id(SETTINGS_ELEMENTS['ChangePW']['retype']).send_keys("golden12")
        self.click_by_id(SETTINGS_ELEMENTS['ChangePW']['retype'])
        self.wd.press_keycode(67)
        self.click_by_id(SETTINGS_ELEMENTS['ChangePW']['newpw'])
        self.wd.press_keycode(67)
        self.click_by_id(SETTINGS_ELEMENTS['ChangePW']['oldpw'])
        self.wd.press_keycode(67)
        self.wd.hide_keyboard()
        self.screenshot("ChangePW - Error messages")

    def changePW_wrongoldpw(self):
        self.wd.find_element_by_xpath(SETTINGS_ELEMENTS['SettingsTab']).click()
        self.wait_locate(SETTINGS_ELEMENTS['ChangePW']['main'], click=True)
        self.wd.find_element_by_id(SETTINGS_ELEMENTS['ChangePW']['oldpw']).send_keys("wrongpw1")
        self.wd.find_element_by_id(SETTINGS_ELEMENTS['ChangePW']['newpw']).send_keys("golden12")
        self.wd.find_element_by_id(SETTINGS_ELEMENTS['ChangePW']['retype']).send_keys("golden12")
        self.click_by_id(GENERAL_ELEMENTS['submit_btn'])
        self.screenshot("Wrong Password")
        self.click_by_id(GENERAL_ELEMENTS['ok_btn'])

    def changePW_success(self, oldpw=None, newpw=None):
        self.wait_locate(SETTINGS_ELEMENTS['SettingsTab'], click=True)
        self.wait_locate(SETTINGS_ELEMENTS['ChangePW']['main'], click=True)
        if oldpw is None:
            self.wd.find_element_by_id(SETTINGS_ELEMENTS['ChangePW']['oldpw']).send_keys("golden1")
        else:
            self.wd.find_element_by_id(SETTINGS_ELEMENTS['ChangePW']['oldpw']).send_keys(oldpw)

        if newpw is None:
            self.wd.find_element_by_id(SETTINGS_ELEMENTS['ChangePW']['newpw']).send_keys("golden12")
            self.wd.find_element_by_id(SETTINGS_ELEMENTS['ChangePW']['retype']).send_keys("golden12")
        else:
            self.wd.find_element_by_id(SETTINGS_ELEMENTS['ChangePW']['newpw']).send_keys(newpw)
            self.wd.find_element_by_id(SETTINGS_ELEMENTS['ChangePW']['retype']).send_keys(newpw)

        self.click_by_id(GENERAL_ELEMENTS['submit_btn'])
        self.screenshot("ChangePW Success")
        self.click_by_id(GENERAL_ELEMENTS['ok_btn'])


def loginTest():
    test = EightDays_Login("ENG 8Days Login")
    test.select_language()
    test.wrong_user()
    test.invalid_login_formats()
    test.wrong_pw()
    test.login()
    test.today_menu()


def signupTest():
    test2 = EightDays_SignUp("VN_8Days Sign Up")
    test2.select_language()
    test2.into_signup()
    test2.signup_by(ran_email(), "Testing", "somepw1", waitforTimeUp=False)


def forgotPWTest():
    test_forgot_pw = ForgotPW('KR_8Days Forgot PW')
    test_forgot_pw.non_existent_user_forgot_via_email()


def changePWTest():
    test_change_pw = changePW('8Days_ChangePW', language='Korean')
    test_change_pw.changePW_wrongoldpw()
    test_change_pw.changePW_get_errors()
    test_change_pw.changePW_success()  # (oldpw, newpw)


def main():
    loginTest()
    signupTest()
    forgotPWTest()
    changePWTest()


if __name__ == "__main__":
    main()
