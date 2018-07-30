from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException

# REQUIRED INFO
trelloboard = ""  # your trelloboard link
email = ""  # your email
pw = ""  # your password


class addMembers():
    def __init__(self, lst_name, members=None, labels=None):
        driver = webdriver.Chrome("/path/to/chromedriver/if/not/in/PATH")
        self.driver = driver
        driver.get(trelloboard)
        login = driver.find_element_by_css_selector(".js-login")
        login.click()

        username = driver.find_element_by_id("user")
        username.send_keys(email)

        password = driver.find_element_by_id("password")
        password.send_keys(pw)

        login = driver.find_element_by_id("login")
        login.click()

        # load the page
        sleep(2)

        self.members = members
        self.labels = labels
        self.lst_name = lst_name

        if self.members is not None:
            self.add_Members(self.members)

        if self.labels is not None:
            self.add_Labels(self.labels)

    def add_Members(self, members):
        lst = self.driver.find_elements_by_xpath(f"//textarea[@aria-label='{self.lst_name}']//parent::div//following-sibling::div[contains(@class,'list-cards')]/child::a")

        for i in range(len(lst)):
            lst[i].click()  # open each card

            members = self.driver.find_element_by_xpath("//div[@class='window-sidebar']//a[contains(@class,'button-link')]")
            members.click()

            for x in self.members:
                x = self.driver.find_element_by_xpath(f"//a[contains(@title,'{x}')]")
                try:
                    self.driver.find_element_by_xpath(f"//span[contains(@name,'{x}')]//following-sibling::span[contains(@class,'icon-check')]")
                except NoSuchElementException:
                    print(f"{x} not clicked yet. Click!")
                    x.click()
                    sleep(1)
                    close = self.driver.find_element_by_xpath("//a[contains(@class,'icon-lg icon-close dialog-close-button')]")
                    close.click()

                else:
                    close = self.driver.find_element_by_xpath("//a[contains(@class,'icon-lg icon-close dialog-close-button')]")
                    close.click()

        def add_Labels(self, labels):
            pass

        sleep(5)
        self.driver.quit()


addMembers('Bugs/Improve ToDo List', ['name1', 'name2'])
