import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup


################SCRAPPING DATA FROM ZILLOW USING BEAUTIFULSOUP #############
zillow_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
    "accept-language": "en-US,en;q=0.9"
}
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLScl51WsC3Ch1AqA9TfNkqmBRm-BJyGTTGzlVac9IOeuMyDUiQ/viewform?usp=sf_link"
zillow_address= "https://www.zillow.com/homes/for_rent/3-_beds/1.5-_baths/?searchQueryState=%7B%22mapBounds%22%3A%7B%22west%22%3A-122.83981199196992%2C%22east%22%3A-121.6189562790793%2C%22south%22%3A47.30989806317245%2C%22north%22%3A47.852728815933894%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22mp%22%3A%7B%22min%22%3A2400%2C%22max%22%3A2800%7D%2C%22beds%22%3A%7B%22min%22%3A3%7D%2C%22sort%22%3A%7B%22value%22%3A%22priorityscore%22%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22price%22%3A%7B%22min%22%3A552787%2C%22max%22%3A644919%7D%2C%22baths%22%3A%7B%22min%22%3A1.5%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%5D%2C%22customRegionId%22%3A%226f21b62f0aX1-CR18llfliduic8u_ydimm%22%2C%22pagination%22%3A%7B%7D%7D"
SLEEP_TIMER= 1
zillow_response = requests.get(url=zillow_address, headers=zillow_headers).text
soup = BeautifulSoup(zillow_response, "html.parser")
# print(soup.prettify())
address_text_list = soup.find_all(class_="list-card-addr")
# for address in address_text_list:
#     print(address.text)

price_list = soup.find_all(class_="list-card-price")
# for price in price_list:
#     print(price.text)

address_link_list = soup.find_all(class_="list-card-img")
# for address_link in address_link_list:
#     try:
#         print(address_link['href'])
#     except KeyError:
#         print("No link found")

# print(address_text_list)
# print(price_list)
# print(address_link_list)


######### ADD DATA THRU SELENIUM INTO GOOGLE FORMS ############
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
for num in range(0, len(address_text_list)):
    #chrome_driver_path = Service("C:\SeleniumDrivers\chromedriver.exe") # local driver
    chrome_driver_path = Service("/usr/local/bin/chromedriver") # circleci driver.
    driver = webdriver.Chrome(service=chrome_driver_path, chrome_options=options) #

    driver.get(google_form_url)
    time.sleep(SLEEP_TIMER)
    form_address_element = driver.find_element(By.CSS_SELECTOR, value='#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(1) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input')
    try:
        enter_address = form_address_element.send_keys(address_text_list[num].text)
    except KeyError:
        enter_address = form_address_element.send_keys("No Address Found")
    time.sleep(SLEEP_TIMER)
    form_price_element = driver.find_element(By.CSS_SELECTOR, value='#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(2) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input')
    try:
        enter_price = form_price_element.send_keys(price_list[num].text)
    except KeyError:
        enter_price = form_price_element.send_keys("No Price Found")
    time.sleep(SLEEP_TIMER)
    form_link_element = driver.find_element(By.CSS_SELECTOR,'#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(3) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input')
    try:
        enter_link = form_link_element.send_keys(address_link_list[num]['href'])
    except KeyError:
        enter_link = form_link_element.send_keys("No Link Found")
    time.sleep(SLEEP_TIMER)
    submit_form = driver.find_element(By.CLASS_NAME, value="l4V7wb").click()
    time.sleep(SLEEP_TIMER)
    driver.close()

print("Google Form Writing Complete")