# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 16:26:02 2018

@author: Cheng Huan An

This is an example script of the automation of a payment form. Focus is on using Selenium locaters and KEYS (different ways to carry out a task -- say selecting an item from a list) and incorporating logging into your script.

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
# only used when I'm using certain EC; else I don't find it faster

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select
# normally used for <select> items but can't be used here somehow.
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import random
import logging
import time
import datetime


formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

logger = setup_logger('info_level_logger','formsINFO.log')
logger2 = setup_logger('debug_level_logger','formsDEBUG.log',level=logging.DEBUG)
# logging.basicConfig(filename='formsINFO.log', level=logging.INFO, format='%(%(levelname)s:%(message)s')

# the following takes 47 seconds to run, assuming immediate reaction when clicking submit.

# set-up
start = time.time()
now = datetime.datetime.now()
s = now.strftime("%d %B %Y, %H:%M:%S")
logger.info("Test ran on: {} at{}".format(s.split(',')[0], s.split(',')[1]))
driver = webdriver.Chrome(r"C:\Users\Tea\Desktop\BCA\AutomatedTesting\Selenium\chromedriver.exe")

# set window size to only take up half the screen
# driver.set_window_size(750,800)
# driver.set_window_position(0,0)
try:
    counter += 1
except NameError:
    counter = 1
logger2.debug('Counter: {}'.format(counter))

if counter == 1:
    driver.get("http://www.trailsofindochina.com/trailsv2/payment/")

elif counter == 2:
    driver.get("https://backends.studioboconganh.com/trails/v2/payment/")
    counter = 0

else:
    counter = 0

# Login page
elem = driver.find_elements_by_class_name("required")

"""
User login information
"""
user = 'go'
password = 'payment'
bookingcode = 'test'

try:
    elem[0].send_keys(user)
    elem[1].send_keys(password)
    elem[2].send_keys(bookingcode)

except NoSuchElementException:
    assert counter <= 2, 'global variable counter not counting right. counter is {}'.format(counter)

logger.info('Found login page elements')
checkbox = driver.find_element_by_tag_name("label")
checkbox.click()
login = driver.find_element_by_id("submit_pay")
login.click()

# Online Payment Form
WebDriverWait(driver, 10).until(EC.title_contains("OnePAY"))

form_elem1 = driver.find_elements_by_class_name("required")
# invoice, name, address, city, state, postal code
assert ('Invoice_number_' + bookingcode) in driver.page_source, "invoice"

form_elem2 = driver.find_elements_by_class_name("ui-selectmenu-status")
# cardtype, expiry mth, expiry year, country, payment, total amt

cardtype = form_elem2[0]
cardtype.click()

num = random.randint(1, 2)  # either 1 or 2
driver.implicitly_wait(1)
actions = ActionChains(driver)

for _ in range(num):
    actions.send_keys(Keys.ARROW_DOWN)
    actions.send_keys(Keys.ENTER)
    actions.perform()

chosen_card = cardtype.text
logger.info("The chosen card is: {}".format(chosen_card))

"""
User Card Information
"""
cardname = 'Cookie'
card_num = {'Visa': '4000000000000002',
            'MasterCard': '5313581000123430'}
expiry_mth = 'May'
expiry_year = '2021'
security_code = '123'

name = driver.find_element_by_name("requestDTO.vpc_NameCard")
name.send_keys(cardname)

form_elem3 = driver.find_elements_by_class_name("input-text")
cardnum = form_elem3[0]

if chosen_card == 'Visa':
    cardnum.send_keys(card_num.get('Visa'))

elif chosen_card == 'MasterCard':
    cardnum.send_keys(card_num.get('MasterCard'))

else:
    print("{}: no card for this yet".format(chosen_card))
    logger.info("{}: no card for this yet".format(chosen_card))
    cardtype.click()
    actions.send_keys(Keys.ARROW_UP)
    actions.send_keys(Keys.ENTER)
    actions.perform()

expirymth = driver.find_element_by_xpath(
    "//a[starts-with(@id,'expiryMonth_button')]")
expirymth.click()
driver.find_element_by_xpath("//a[text()=" + "'" + expiry_mth + "'" + "]").click()

expiry_yr = driver.find_element_by_xpath(
    "//a[starts-with(@id,'expiryYear_button')]")
expiry_yr.click()
driver.find_element_by_xpath("//a[text()=" + expiry_year + "]").click()

cvv = driver.find_element_by_name("requestDTO.vpc_CardSecurityCode")
cvv.send_keys(security_code)

Address = {'Street': '617  Briarwood Drive',
           'City': 'Atlanta',
           'State': 'Georgia',
           'Zip': '30328'}

address = driver.find_element_by_name("requestDTO.AVS_Street01")
address.send_keys(Address.get('Street'))

city = driver.find_element_by_name("requestDTO.AVS_City")
city.send_keys(Address.get('City'))

state = driver.find_element_by_name("requestDTO.AVS_StateProv")
state.send_keys(Address.get('State'))

postal_code = driver.find_element_by_name("requestDTO.AVS_PostCode")
postal_code.send_keys(Address.get('Zip'))

country = driver.find_element_by_xpath("//a[starts-with(@id,'avsCountry_button')]")
country.click()
choose_country = driver.find_element_by_xpath(("//a[text()='Georgia']")).click()

payment = driver.find_element_by_xpath("//a[starts-with(@id,'paymentDescription')]")
payment.click()
driver.find_element_by_xpath(("//a[contains(text(),'Deposit')]")).click()

currency = driver.find_element_by_xpath("//a[starts-with(@id,'currencyCode_button_')]")
currency.click()
driver.find_element_by_xpath("//a[contains(text(),'USD')]").click()

amt = driver.find_element_by_id('inAmount')
ran_num = str(random.randint(1, 10000))
amt.send_keys(ran_num)

driver.find_element_by_id("btcheck").click()
driver.find_element_by_id("submit_pay").click()

# driver.implicitly_wait(30) #this one doesn't actually work here somehow, just jumps to the error almost immediately, I think it might be because they see a fully-loaded page so they stop waiting.
time.sleep(20)
# trick to use selenium and manual mode together

try:
    assert ('receipt') in driver.title, 'receipt page not reached'
    logger.info("receipt page reached")
except AssertionError:
    assert ('error payment') in driver.title, 'neither receipt nor error payment page'
    logger2.error("error payment page reached instead of receipt page")

end = time.time()
total = end - start
logger.info("Total time taken (to confirmation page): {:3f}s".format(total))
logger.info("\n")
