from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time
import os

# Setup Chrome options
options = Options()
for arg in ["--headless", "--no-sandbox", "--disable-dev-shm-usage"]:
    options.add_argument(arg)
options.binary_location = "/usr/bin/google-chrome"

driver = webdriver.Chrome(options=options)

# Scrape
driver.get('https://www.iid.com/water/water-supply')
time.sleep(5)
html_content = driver.page_source
driver.quit()

# Parse HTML
soup = BeautifulSoup(html_content, 'html.parser')
tables = soup.find_all('table')
for table in tables:
    rows = table.find_all('tr')
    data_to_save = []
    for row in rows:
        cols = row.find_all(['td', 'th'])
        data_to_save.append([col.text.strip() for col in cols])

# Ensure data_directory exists
os.makedirs('data_directory', exist_ok=True)

# Create a timestamped filename inside data_directory
timestamp = datetime.now().strftime("%Y_%m_%d_%H")
filename = f"data_directory/water_supply_{timestamp}.csv"

# Save snapshot
current_dt = datetime.now()
formatted_datetime = current_dt.strftime("%Y_%m_%d_%H")
with open(f'water_supply_{formatted_datetime}.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data_to_save)

print(f"Data saved to {filename}")