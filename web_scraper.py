from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time

options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)

# Target URL
url = 'https://www.iid.com/water/water-supply'
driver.get(url)
time.sleep(5)

html_content = driver.page_source
driver.quit()

soup = BeautifulSoup(html_content, 'html.parser')

# Extract table content
tables = soup.find_all('table')
for table in tables:
    rows = table.find_all('tr')
    data_to_save = []
    for row in rows:
        cols = row.find_all(['td', 'th'])
        data_to_save.append([col.text.strip() for col in cols])

# Save to CSV
current_dt = datetime.now()
formatted_datetime = current_dt.strftime("%Y_%m_%d_%H")
with open(f'water_supply_{formatted_datetime}.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data_to_save)

print("Data saved to CSV.")