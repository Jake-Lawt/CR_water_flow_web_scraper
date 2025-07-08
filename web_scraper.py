from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time

options = Options()
for arg in ["--headless", "--no-sandbox", "--disable-dev-shm-usage"]:
    options.add_argument(arg)
options.binary_location = "/usr/bin/google-chrome"

driver = webdriver.Chrome(options=options)

driver.get('https://www.iid.com/water/water-supply')
time.sleep(5)
html_content = driver.page_source
driver.quit()

soup = BeautifulSoup(html_content, 'html.parser')
data_to_save = [
    [col.text.strip() for col in row.find_all(['td', 'th'])]
    for table in soup.find_all('table')
    for row in table.find_all('tr')
]

filename = datetime.now().strftime("water_supply_%Y_%m_%d_%H.csv")
with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(data_to_save)

print("Data saved to CSV")
