import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

GOOGLE_FORM = "https://forms.gle/Q2crx3cY1GseKaXE8"
SPREADSHEET = "https://docs.google.com/spreadsheets/d/1cn1mVvn9vMPRysBS_7OFDzEEswCrP4BWK1JIWXFLmn4/edit?resourcekey#gid=820040227"
ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.69219435644531%2C%22east%22%3A-122.17446364355469%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7,or;q=0.6"
}

response = requests.get(ZILLOW_URL, headers=headers)
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")

all_link_elements = soup.select(".property-card-data a")

all_link = []
for link in all_link_elements:
    href = link["href"]
    if "http" not in href:
        all_link.append(f"https://www.zillow.com{href}")
    else:
        all_link.append(href)

# print(all_link)

all_price_elements = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr")
all_price1 = [i.getText().split("+")[0] for i in all_price_elements]
all_price = [i.split("/")[0] for i in all_price1]
# print(all_price)

all_address_elements = soup.select(".StyledPropertyCardDataWrapper-c11n-8-84-3__sc-1omp4c3-0.bKpguY.property-card-data  a  address")
all_address = [i.getText().split("|")[-1] for i in all_address_elements]
# print(all_address)

driver = webdriver.Chrome()

for i in range(len(all_link)):
    driver.get(GOOGLE_FORM)
    driver.maximize_window()
    sleep(3)

    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(all_address[i])
    sleep(2)

    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(all_price[i])
    sleep(2)

    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(all_link[i])
    sleep(2)

    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
    sleep(5)

driver.get(SPREADSHEET)
sleep(30)
driver.quit()
