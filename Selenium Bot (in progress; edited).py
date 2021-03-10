import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def availabilityCheck():
    r = requests.get('https://yourwebsite.com/products.json')
    products = json.loads((r.text))['products']

    for product in products:
        print(product['title'])
        productName = product['title']
        print(products[0]['handle'])
        if productName == 'Your Product Name':
            productURL = 'https://yourwebsite.com/products/'+ product['handle']
            return productURL

    return False

driver = webdriver.Chrome(executable_path=r'C:\Users\your_user\chromedriver.exe')
driver.get('https://yourwebsite/producturl/')

# Clicking ATC button and checkout
driver.find_element_by_xpath('//button[@class="product-form--atc-button "]').click()
driver.find_element_by_xpath('//button[@name="checkout "]').click()

# User Login
driver.find_element_by_xpath('//input[@name="customer[email]"]').send_keys('youremail@gmail.com')
driver.find_element_by_xpath('//input[@name="customer[password]"]').send_keys('yourpassword')
time.sleep(1)
driver.find_element_by_xpath('//button[@class="button-primary form-action--submit"]').click()

# Shipping Info
driver.find_element_by_xpath('//input[@placeholder="First name"]').send_keys('Your FName')
driver.find_element_by_xpath('//input[@placeholder="Last name"]').send_keys('Your LName')
driver.find_element_by_xpath('//input[@placeholder="Address"]').send_keys('Your Address')
driver.find_element_by_xpath('//input[@placeholder="City"]').send_keys('Your City')
time.sleep(0.5)
driver.find_element_by_xpath('//input[@autocomplete="shipping address-level1"]').send_keys('Your State Abbr.')
driver.find_element_by_xpath('//input[@placeholder="ZIP code"]').send_keys('Your Zipcode')
time.sleep(1)
driver.find_element_by_xpath('//button[@name="button"]').click()

# To automatically click enter, add '+ u'\ue007' after the key

# Continue to Payment Button click
driver.find_element_by_xpath('//button[@id="continue_button"]').click()

# Entering Payment Info
# driver.switch_to.frame('card-fields-iframe')
# wait = WebDriverWait(driver,10)
# wait.until(EC.frame_to_be_available_and_switch_to_it(By.ID,"card-fields-number"))

# Properly switches to frame and returns frame but how to input card number...?
WebDriverWait(driver, 2).until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME,"card-fields-iframe")))

# Work from here on...




