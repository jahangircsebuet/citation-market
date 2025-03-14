from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')  # Necessary for some environments
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Initialize the WebDriver in headless mode
driver = webdriver.Chrome(options=chrome_options)

# Open the target webpage
driver.get('https://scholar.google.com/citations?user=v7hMP8kAAAAJ&hl=en')

import csv
import pandas as pd


# Initialize a list to store all row data
all_rows = []

# Find the table by ID
try:
    table = driver.find_element(By.ID, 'gsc_a_t')
    
    # Get all rows within the table
    rows = table.find_elements(By.TAG_NAME, 'tr')
    
    # Iterate over each row
    for row in rows:
        # Get all columns (td or th) within the row
        columns = row.find_elements(By.TAG_NAME, 'td')
        
        # Extract and store text from each column
        row_data = [col.text.strip() for col in columns]
        all_rows.append(row_data)  # Collect row data
    
except Exception as e:
    print(f'Table not found: {e}')

# Create a DataFrame from the collected row data
df = pd.DataFrame(all_rows, columns=['Title', 'Citation', 'Year'])  # Adjust column names as needed
print(df.head())

# Save the DataFrame to a CSV file
df.to_csv('df_papers.csv', index=False)

# Close the WebDriver
driver.quit()