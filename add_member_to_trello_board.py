from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException

# =========== REQUIRED INFO ==============
trelloboard = " " # put your trelloboard link here
email = " " # your email
password = " " # your password

CHROMEDRIVER_PATH = r"" # path to chromedriver.exe

name1 = ""
name2 = ""
# =========================================

driver = webdriver.Chrome(CHROMEDRIVER_PATH)
driver.get(trelloboard)

login = driver.find_element_by_css_selector(".js-login")
login.click()

username = driver.find_element_by_id("user")
username.send_keys(email)

password = driver.find_element_by_id("password")
password.send_keys(password)

login = driver.find_element_by_id("login")
login.click()

# load the page
sleep(2)

'''You will need to change the labels of the xpath to suit your needs, though the general format should be the same'''
def androidMembers():
    # finding the list of interest and the cards under it
    androidCards = driver.find_elements_by_xpath("//textarea[@aria-label='Android']//parent::div//following-sibling::div[contains(@class,'list-cards')]/child::a")

    print("found cards")

    for i in range(len(androidCards)):
        androidCards[i].click()

        members = driver.find_element_by_xpath("//div[@class='window-sidebar']//a[contains(@class,'button-link')]")
        members.click()

        # find the member you want to add to the card
        name1 = driver.find_element_by_xpath("//a[contains(@title,name1)]")
        check = driver.find_element_by_xpath("//span[contains(@name,name2)]//following-sibling::span[contains(@class,'icon-check')]")

        try:
            check = driver.find_element_by_xpath("//span[contains(@name,name2)]//following-sibling::span[contains(@class,'icon-check')]")
        except NoSuchElementException:
            print("name not ticked yet. Click!")
            name1.click()

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

        name1 = driver.find_element_by_xpath("//a[contains(@title,name1)]")
        name2 = driver.find_element_by_xpath("//a[contains(@title,name2)]")

        try:
            check = driver.find_element_by_xpath("//a[contains(@title,name1)]//parent::li[contains(@class,'active')]")
        except NoSuchElementException:
            print("name not ticked yet. Click!")
            name.click()

        try:
            check = driver.find_element_by_xpath("//a[contains(@title,name1)]//parent::li[contains(@class,'active')]")

        except NoSuchElementException:
            print("name not ticked yet. Click!")
            nghia.click()

        close = driver.find_element_by_xpath("//a[contains(@class,'icon-lg icon-close dialog-close-button')]")
        close.click()


# run the functions for the lists you want to add members to
IOSMembers()
sleep(2)
driver.quit()
