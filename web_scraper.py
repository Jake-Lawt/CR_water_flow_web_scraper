from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time

options = Options()
options.headless = True
options.binary_location = "/usr/bin/google-chrome"

driver = webdriver.Chrome(
    service=Service("./"),
    options=options
)

# Scrape
url = 'https://www.iid.com/water/water-supply'
driver.get(url)
time.sleep(5)

html_content = driver.page_source
driver.quit()

# Parse
soup = BeautifulSoup(html_content, 'html.parser')
tables = soup.find_all('table')

data_to_save = []
for table in tables:
    for row in table.find_all('tr'):
        cols = row.find_all(['td', 'th'])
        data_to_save.append([col.text.strip() for col in cols])

# Save
filename = datetime.now().strftime("water_supply_%Y_%m_%d_%H.csv")
with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data_to_save)

print("Data saved to CSV")