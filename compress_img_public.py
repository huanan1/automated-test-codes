'''
This code drags all images in a specified folder to Tinyjpg. Note that this will only work when the images in the file is <= 20, due to the tinyJPG.com's limit
'''
import pyautogui as pag
from selenium import webdriver
from time import sleep
import os
import logging

# Define this 3 variables to run the code
path_to_chromedriver = r""  # eg. C:\Users\Tea\Desktop\chromedriver.exe"
path_to_file_with_images = r""  # eg. C:/Users/Tea/Desktop/1ToCompress/
path_to_default_download_location = r""  # eg. C:/Users/Tea/Downloads/

files = os.listdir(path_to_file_with_images)
print(files)

driver = webdriver.Chrome(path_to_chromedriver)

driver.get("https://tinyjpg.com/")
assert "TinyJPG" in driver.title


droplocation = driver.find_element_by_class_name("icon")
droplocation.click()

sleep(2)
pag.typewrite(path_to_file_with_images)
pag.press('enter')

sleep(2)

window = pag.click(476, 310)
pag.hotkey('ctrl', 'a')

sleep(2)

pag.click(1768, 1701)

for i in range(5):
    try:
        assert len(files) == len(driver.find_elements_by_css_selector("div .progress.success"))
    except AssertionError:
        sleep(3)
    else:
        break


downloads = driver.find_elements_by_css_selector(".upload .upload a")
print(downloads)

for download in downloads:
    download.click()

sleep(2)

for file in files:
    try:
        os.remove(path_to_file_with_images + file)
        os.rename(path_to_default_download_location + file, path_to_file_with_images + file)
        os.remove(path_to_default_download_location + file)
        # I can write it like this when I'm writing the path directly instead of using a variable
        # os.rename(f"C:/Users/Tea/Downloads/{file}", f"C:/Users/Tea/Desktop/BCA/TOI/1ToCompress/{file}")

    except FileNotFoundError:
        print(logging.exception(f"{file} Not Found"))

driver.quit()
