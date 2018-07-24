from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(r"C:\Users\Tea\Desktop\BCA\AutomatedTesting\Selenium\chromedriver.exe")
driver.get("<your trello board>")

login = driver.find_element_by_css_selector(".js-login")
login.click()

username = driver.find_element_by_id("user")
username.send_keys("<youremail>")

password = driver.find_element_by_id("password")
password.send_keys("<yourpassword>")

login = driver.find_element_by_id("login")
login.click()

# load the page
sleep(2)


def androidMembers():
    androidCards = driver.find_elements_by_xpath("//textarea[@aria-label='Android']//parent::div//following-sibling::div[contains(@class,'list-cards')]/child::a")

    print("found cards")

    for i in range(len(androidCards)):
        androidCards[i].click()

        members = driver.find_element_by_xpath("//div[@class='window-sidebar']//a[contains(@class,'button-link')]")
        members.click()

        khoa = driver.find_element_by_xpath("//a[contains(@title,'<name>')]")
        check = driver.find_element_by_xpath("//span[contains(@name,'khoa59')]//following-sibling::span[contains(@class,'icon-check')]")
        if check.value_of_css_property('display') == 'None':
            khoa.click()
            close = driver.find_element_by_xpath("//a[contains(@class,'icon-lg icon-close dialog-close-button')]")
            close.click()

        else:
            close = driver.find_element_by_xpath("//a[contains(@class,'icon-lg icon-close dialog-close-button')]")
            close.click()


def IOSMembers():
    IOS_cards = driver.find_elements_by_xpath("//textarea[@aria-label='IOS']//parent::div//following-sibling::div[contains(@class,'list-cards')]/child::a")

    print("found IOS cards")

    for i in range(len(IOS_cards)):
        IOS_cards[i].click()

        members = driver.find_element_by_xpath("//div[@class='window-sidebar']//a[contains(@class,'button-link')]")
        members.click()

        name1 = driver.find_element_by_xpath("//a[contains(@title,'name')]")
        name2 = driver.find_element_by_xpath("//a[contains(@title,'name2')]")

        try:
            check = driver.find_element_by_xpath("//a[contains(@title,'name')]//parent::li[contains(@class,'active')]")
        except NoSuchElementException:
            print("name not ticked yet. Click!")
            name.click()

        try:
            check = driver.find_element_by_xpath("//a[contains(@title,'name')]//parent::li[contains(@class,'active')]")

        except NoSuchElementException:
            print("name not ticked yet. Click!")
            nghia.click()

        close = driver.find_element_by_xpath("//a[contains(@class,'icon-lg icon-close dialog-close-button')]")
        close.click()


# run the functions for the lists you want to add members to
IOSMembers()
sleep(2)
driver.quit()
