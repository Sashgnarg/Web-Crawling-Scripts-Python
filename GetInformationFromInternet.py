import re
import shutil

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# THIS SCRIPT WILL SEARCH FOR PARTS FROM THE MANUFATURER "HLC" WHEN GIVEN AN ITEM NUMBER, THEN GATHER INFORMATION
# ABOUT THAT PRODUCT AND DOWNLOAD THE PRODUCT IMAGE, AND FINALLY IT WILL INPUT THAT DATA INTO LIGHTSPEED ECOMMERCE

#CONSTANTS
PRESS_RETURN = 0
DONT_PRESS_RETURN = 1

PATH = "E:/webdrivers/chromedriver.exe"

driverForSearching = webdriver.Chrome(PATH)
driverForLightSpeed = webdriver.Chrome(PATH)
driverForSearching.maximize_window()
site1 = 'https://www.hlc.bike/ca/login.aspx'
site2 = 'https://us.lightspeedapp.com/?name=item.views.quick_add&form_name=view&id=null&tab=details'
driverForSearching.get(site1)
driverForLightSpeed.get(site2)



def findAndDownloadImage():
    try:
        image = WebDriverWait(driverForSearching, 10).until(
            EC.presence_of_element_located((By.ID, "mainImage"))
        )
    except:
        print("image could not be downloaded")
        return ''

    image_url = image.get_attribute('src')
    filename = image_url.split("/")[-1]
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream=True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived')

    return filename

class Attribute:
    def __init__(self, attribute_name, attribute_value_default):
        #attribute_name = upc,ean etc,
        self.attribute_name = attribute_name
        self.attribute_value_default = attribute_value_default
        self.attribute_value = attribute_value_default


    def findValue(self, CSS_selector_type, CSS_selector):
        try:
            element_location_in_html = WebDriverWait(driverForSearching, 10).until(
                EC.presence_of_element_located((CSS_selector_type, CSS_selector))
            )
            self.attribute_value = element_location_in_html.get_attribute("innerText")

        except:
            print("error with finding " + self.attribute_name)
            self.attribute_value = self.attribute_value_default


    def inputValueOnLightspeed(self, CSS_selector_type, CSS_selector, return_value):
        value_input = WebDriverWait(driverForLightSpeed, 10).until(
            EC.presence_of_element_located((By.ID, CSS_selector))
        )
        if(return_value == PRESS_RETURN):
            value_input.clear()
            value_input.send_keys(self.attribute_value)
            value_input.send_keys(Keys.RETURN)
        else:
            value_input.clear()
            value_input.send_keys(self.attribute_value)


    def filterPriceFromString(self):
        # get number from string
        try:
            self.attribute_value = re.search('[0-9.]+', self.attribute_value).group()
        except:
            return 0
        return self.attribute_value

    def filterBrand(self, value):
        # the first word in description is the brand. delete everything after that
        sep = ','
        self.attribute_value = value.split(sep)[0]


def getItemNumberFromUser():
    item_number = input("enter -1 to exit\ninput the item number (including the dash): ")
    return item_number




def main():
    while True:
        item_number = getItemNumberFromUser()
        if(item_number == '-1'):
            driverForSearching.quit()
            driverForLightSpeed.quit()
            return
        site = 'https://www.hlc.bike/ca/Catalog/Item/' + item_number
        driverForSearching.get(site)

        UPC = Attribute('UPC', 0)
        EAN = Attribute('EAN', 0)
        description = Attribute('description', '')
        defaultPrice = Attribute('defaultPrice', 0)
        msrp = Attribute('msrp', 0)
        vendor = Attribute('vendor', 'HLC')
        brand = Attribute('brand', '')
        man_sku = Attribute('man_sku', item_number)

        UPC.findValue(By.XPATH, "//div[text()='UPC']/following-sibling::div")
        EAN.findValue(By.XPATH, "//div[text()='EAN']/following-sibling::div")
        description.findValue(By.CLASS_NAME, "variantDescription")
        defaultPrice.findValue(By.ID, "detailVariantPrice")
        defaultPrice.attribute_value = defaultPrice.filterPriceFromString()
        msrp.findValue(By.CLASS_NAME, "priceSmall")
        msrp.attribute_value = msrp.filterPriceFromString()
        vendor.attribute_value = 'HLC'
        brand.filterBrand(description.attribute_value)
        findAndDownloadImage()

        UPC.inputValueOnLightspeed(By.ID, "view_upc", DONT_PRESS_RETURN)
        EAN.inputValueOnLightspeed(By.ID, "view_ean", DONT_PRESS_RETURN)
        description.inputValueOnLightspeed(By.ID, "view_description", DONT_PRESS_RETURN)
        man_sku.inputValueOnLightspeed(By.ID, "view_man_sku", DONT_PRESS_RETURN)
        defaultPrice.inputValueOnLightspeed(By.ID, "view_default_cost", DONT_PRESS_RETURN)
        vendor.inputValueOnLightspeed(By.ID, "view_vendor_id", PRESS_RETURN)
        brand.inputValueOnLightspeed(By.ID, "view_manufacturer_id",PRESS_RETURN)
        msrp.inputValueOnLightspeed(By.ID, "view_price_default", DONT_PRESS_RETURN)



main()
