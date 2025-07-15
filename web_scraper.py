from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

# Setup Chrome options
options = Options()
for arg in ["--headless", "--no-sandbox", "--disable-dev-shm-usage"]:
    options.add_argument(arg)
options.binary_location = "/usr/bin/google-chrome"

# Start driver
driver = webdriver.Chrome(options=options)

# Load page and wait for table
url = 'https://www.iid.com/water/water-supply'
driver.get(url)

# Wait until at least one <table> element appears (up to 20 seconds)
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )
except:
    print("Timed out waiting for table to load.")

# Capture HTML
html_content = driver.page_source
driver.quit()

# Save debug HTML for inspection (optional)
with open("debug_page.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Parse with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
tables = soup.find_all('table')
print(f"Found {len(tables)} tables.")

# Extract data
data_to_save = []
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all(['td', 'th'])
        data_to_save.append([col.text.strip() for col in cols])

print(f"Extracted {len(data_to_save)} rows.")

# Ensure directory exists
os.makedirs('data_directory', exist_ok=True)

# Timestamped filename
timestamp = datetime.now().strftime("%Y_%m_%d_%H")
filename = f"data_directory/water_supply_{timestamp}.csv"

# Save CSV
with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data_to_save)

print(f"Data saved to {filename}")
