import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')  # Necessary for some environments
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Initialize the WebDriver in headless mode
driver = webdriver.Chrome(options=chrome_options)

# Open the target webpage

# name = "jahangir"
# driver.get('https://scholar.google.com/citations?user=v7hMP8kAAAAJ&hl=en')

# name = "sai"
# driver.get('https://scholar.google.com/citations?user=VjEGZJoAAAAJ&hl=en')

# name = "ismail"
# driver.get('https://scholar.google.com/citations?user=FexryyIAAAAJ&hl=en')

name = "abdullah"
driver.get('https://scholar.google.com/citations?user=zQKHA64AAAAJ&hl=en')


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
        
        # Initialize row data list
        row_data = []

        # Extract paper title and URL from the first column
        if columns:
            title_col = columns[0]
            anchor = title_col.find_element(By.TAG_NAME, 'a')
            paper_title = anchor.text.strip()
            paper_url = anchor.get_attribute('href')

            # print("paper_url: ", paper_url)
            row_data.append(paper_url)

            # Extract and append the rest of the columns (e.g., citations, year)
            for col in columns[1:]:
                row_data.append(col.text.strip())

            # row_data.append(paper_title)
            # row_data.append(paper_url)
            
        all_rows.append(row_data)  # Collect row data
    
except Exception as e:
    print(f'Table not found: {e}')

# Create a DataFrame from the collected row data
df = pd.DataFrame(all_rows, columns=['Title', 'Citation', 'Year'])  # Adjust column names as needed
# print(df.head())

# print("#papers: ", len(df))

# Save the DataFrame to a CSV file
df.to_csv(f'{name}_papers.csv', index=False)

# Close the WebDriver
driver.quit()

# print("all_rows")
# print(all_rows)

def is_next_page_available(driver):
    """
    Check if the 'Next' button is available on the current page.
    """
    try:
        # Wait for the "Next" button to appear (if it exists)
        next_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Next"))
        )
        # Check if the button is enabled and clickable
        if next_button.is_enabled():
            return True
    except Exception:
        pass
    return False


from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Base URL (url1)
url1 = 'https://scholar.google.com/scholar?hl=en&as_sdt=5%2C44&cites=10315031793445629859&scipsc=&q=&scisbd=1'

# Function to create paginated URLs
def create_paginated_url(base_url, start_value):
    # Parse the URL into components
    parsed_url = urlparse(base_url)
    
    # Parse the query parameters into a dictionary
    query_params = parse_qs(parsed_url.query)
    
    # Add or update the 'start' parameter
    query_params['start'] = [str(start_value)]
    
    # Reconstruct the query string
    new_query = urlencode(query_params, doseq=True)
    
    # Reconstruct the full URL
    new_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query,
        parsed_url.fragment
    ))
    
    return new_url

# Create url2 and url3
url2 = create_paginated_url(url1, 10)
url3 = create_paginated_url(url1, 20)

# build cited by url 
def build_cited_by_url(paper_id):
    base_url = "https://scholar.google.com/scholar"
    params = {
        "hl": "en",
        "as_sdt": "5,44",
        "cites": paper_id,
        "scipsc": "",
        "q": "",
        "scisbd": "1"
    }

    from urllib.parse import urlencode

    full_url = f"{base_url}?{urlencode(params)}"
    return full_url

paper_id = "9579430514940149198"
url = build_cited_by_url(paper_id)
print(url)

def extract_cited_by_urls(data):
    print("entering into extract_cited_by_urls")
    # Set up headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')  # Necessary for some environments
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Initialize the WebDriver in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    all_cited_by_urls_with_days_info = []
    
    for row in data:
        print(len(row), row[0] if len(row) > 0 else None)
        paper_url = row[0] if len(row) > 0 else None
        
        # print("Re-initialize the driver here")
        # Re-initialize the driver here
        # Set up headless mode
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')  # Necessary for some environments
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Initialize the WebDriver in headless mode
        driver = webdriver.Chrome(options=chrome_options)
        
        if paper_url is not None:
            # Load the paper URL in the browser
            driver.get(paper_url)

            try:
                # Wait for the "Cited by" link to appear
                cited_by_anchor = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Cited by"))
                )

                # Extract the link
                cited_by_url = cited_by_anchor.get_attribute('href')
                # print("Cited by URL:", cited_by_url)

                # Extract the paper_id from the cited_by_url
                parsed_url = urlparse(cited_by_url)
                query_params = parse_qs(parsed_url.query)
                paper_id = query_params.get('cites', [None])[0]  # Get the 'cites' parameter value
                # print("Extracted Paper ID:", paper_id)

                cited_by_url_with_days_info = build_cited_by_url(paper_id)

                all_cited_by_urls_with_days_info.append(cited_by_url_with_days_info)

            except Exception as e:
                print("Cited by link not found for:", paper_title)
                print("e: ", e)
                cited_by_url = None
        
        # Close the WebDriver
        driver.quit()

    # print("returning from extract_cited_by_urls")
    # print("all_cited_by_urls_with_days_info")
    # print(all_cited_by_urls_with_days_info)

    return all_cited_by_urls_with_days_info

cited_by_urls_with_days = extract_cited_by_urls(all_rows)

for url in cited_by_urls_with_days:
    print("url: ", url)