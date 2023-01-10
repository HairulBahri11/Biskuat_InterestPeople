from asyncio import streams
from email.mime import image
from multiprocessing.sharedctypes import Value
import shutil
from urllib import request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import requests

# another import
import os
import wget as wget

def ambil_foto(keyword):
    driver = webdriver.Chrome('D:/Mata Kuliah/semester 5/Biskuat_InterestPeople/static/driver/chromedriver.exe')
    #driver = webdriver.Chrome() if your chromedriver.exe inside root

    driver.set_window_size(480, 1080)
    driver.get("http://www.instagram.com")

    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username.clear()
    username.send_keys("@rulyton")
    password.clear()
    password.send_keys("4januari")
    Login_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    # handling popup message
    not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

    searchbox = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    searchbox.clear()

    searchbox.send_keys(keyword)
    time.sleep(5)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(5)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(5)

    driver.execute_script("window.scrollTo(0, 4000);")

    images = driver.find_element(By.XPATH, '//article[@class="x1iyjqo2"]').find_elements(By.XPATH, '//img[@class="x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3"]')
    images = [image.get_attribute('src') for image in images]
    images = images[:-2] #slicing-off IG logo and Profile picture

    path = 'static/' 
    path = os.path.join(path, keyword[0:])
    os.makedirs(path,exist_ok=True)


    counter = 0
    for images2 in images:
        save_as = os.path.join(path, keyword[0:] + str(counter) + '.jpeg')
        wget.download(images2, save_as)
        
        if counter == 20:
            break
        counter += 1