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


PATH = "E:\webdrivers\chromedriver.exe"
PATH2 = "E:\webdrivers\chromedriver2.exe"

driverForSearching = webdriver.Chrome(PATH)
driverForLightSpeed = webdriver.Chrome(PATH)

driverForSearching.maximize_window()
site2 = 'https://us.lightspeedapp.com/?name=item.views.quick_add&form_name=view&id=null&tab=details'
driverForLightSpeed.get(site2)


def getMSRPFromString(MSRP):
    # get number from string
    MSRP = re.search('[0-9.]+', MSRP).group()
    return MSRP


def getBrand(brand):
    # the first word in description is the brand. delete everything after that
    sep = ','
    brand = brand.split(sep)[0]
    return brand


def findUPC():
    try:
        upc = WebDriverWait(driverForSearching, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='UPC']/following-sibling::div"))
        )
        upcvalue = upc.get_attribute("innerText")

    except:
        print("error with finding upc")
        upcvalue = 0
    finally:
        return upcvalue


def findEAN():
    try:
        ean = WebDriverWait(driverForSearching, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='EAN']/following-sibling::div"))
        )
        eanvalue = ean.get_attribute("innerText")
    except:
        print("error with finding  ean")
        eanvalue = '0'
    finally:
        return eanvalue


def findDescription():
    try:
        description = WebDriverWait(driverForSearching, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "variantDescription"))
        )
        descriptionvalue = description.get_attribute("innerText")
    except:
        print("error with finding  description")
        descriptionvalue = ''
    finally:
        return descriptionvalue


def findMSRP():
    try:
        MSRP = WebDriverWait(driverForSearching, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "priceSmall"))
        )
        MSRPvalue = MSRP.get_attribute("innerText")

    except:
        print("error with finding  MSRP")
        MSRPvalue = '0'
    finally:
        return MSRPvalue


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


def getInputFromUser():
    item_number = input("input the item number (including the dash): ")
    getInfoFromInternet(item_number)


def getInfoFromInternet(item_number):
    site = 'https://www.hlc.bike/ca/Catalog/Item/' + item_number
    driverForSearching.get(site)

    upc = findUPC()
    ean = findEAN()
    description = findDescription()
    msrp = findMSRP()
    image = findAndDownloadImage()
    vendor = 'HLC'
    brand = getBrand(description)

    inputDataOnLightspeed(upc, ean, description, item_number, msrp, vendor, brand)


def inputDataOnLightspeed(upc, ean, description, item_number, msrp, vendor, brand):
    upcInput = WebDriverWait(driverForLightSpeed, 10).until(
        EC.presence_of_element_located((By.ID, "view_upc"))
    )
    eanInput = WebDriverWait(driverForLightSpeed, 10).until(
        EC.presence_of_element_located((By.ID, "view_ean"))
    )
    descriptionInput = WebDriverWait(driverForLightSpeed, 10).until(
        EC.presence_of_element_located((By.ID, "view_description"))
    )
    man_SKUInput = WebDriverWait(driverForLightSpeed, 10).until(
        EC.presence_of_element_located((By.ID, "view_man_sku"))
    )
    msrpInput = WebDriverWait(driverForLightSpeed, 10).until(
        EC.presence_of_element_located((By.ID, "view_price_default"))
    )
    vendorInput = WebDriverWait(driverForLightSpeed, 10).until(
        EC.presence_of_element_located((By.ID, "view_vendor_id"))
    )
    brandInput = WebDriverWait(driverForLightSpeed, 10).until(
        EC.presence_of_element_located((By.ID, "view_manufacturer_id"))
    )

    upcInput.send_keys(upc)
    eanInput.send_keys(ean)
    descriptionInput.send_keys(description)
    man_SKUInput.send_keys(item_number)

    msrpInput.clear()
    msrpInput.send_keys(msrp)

    vendorInput.send_keys(vendor)
    vendorInput.send_keys(Keys.RETURN)

    brandInput.send_keys(brand)
    brandInput.send_keys(Keys.RETURN)


def main():
    getInputFromUser()


main()
