import csv
import time
import random
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
from fetch_author_papers import fetch_author_papers
from url_with_days_info import extract_cited_by_urls
from fetch_days_info import fetch_days_info

name = "jahangir"
url = 'https://scholar.google.com/citations?user=v7hMP8kAAAAJ&hl=en'
papers = fetch_author_papers(url=url, author_name=name)
print(f"Author: {name} and #papers: {len(papers)}")

# Read the CSV file into a DataFrame
df = pd.read_csv("jahangir_papers.csv")
cited_by_urls_with_days = extract_cited_by_urls(df.values, "jahangir")
fetch_days_info(cited_by_urls_with_days, "jahangir")


# Generate a random delay between 10 and 30 seconds
time.sleep(random.uniform(10, 30))
name = "sai"
url = 'https://scholar.google.com/citations?user=VjEGZJoAAAAJ&hl=en'
papers = fetch_author_papers(url=url, author_name=name)
print(f"Author: {name} and #papers: {len(papers)}")

# Read the CSV file into a DataFrame
df = pd.read_csv("sai_papers.csv")
cited_by_urls_with_days = extract_cited_by_urls(df.values, "sai")
fetch_days_info(cited_by_urls_with_days, "sai")

# Generate a random delay between 10 and 30 seconds
time.sleep(random.uniform(10, 30))
name = "ismail"
url = 'https://scholar.google.com/citations?user=FexryyIAAAAJ&hl=en'
papers = fetch_author_papers(url=url, author_name=name)
print(f"Author: {name} and #papers: {len(papers)}")

# Read the CSV file into a DataFrame
df = pd.read_csv("ismail_papers.csv")
cited_by_urls_with_days = extract_cited_by_urls(df.values, "ismail")
fetch_days_info(cited_by_urls_with_days, "ismail")

# Generate a random delay between 10 and 30 seconds
time.sleep(random.uniform(10, 30))
name = "abdullah"
url = 'https://scholar.google.com/citations?user=zQKHA64AAAAJ&hl=en'
papers = fetch_author_papers(url=url, author_name=name)
print(f"Author: {name} and #papers: {len(papers)}")

# Read the CSV file into a DataFrame
df = pd.read_csv("abdullah_papers.csv")
cited_by_urls_with_days = extract_cited_by_urls(df.values, "abdullah")
fetch_days_info(cited_by_urls_with_days, "abdullah")






# def is_next_page_available(driver):
#     """
#     Check if the 'Next' button is available on the current page.
#     """
#     try:
#         # Wait for the "Next" button to appear (if it exists)
#         next_button = WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located((By.LINK_TEXT, "Next"))
#         )
#         # Check if the button is enabled and clickable
#         if next_button.is_enabled():
#             return True
#     except Exception:
#         pass
#     return False


# from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# # Base URL (url1)
# url1 = 'https://scholar.google.com/scholar?hl=en&as_sdt=5%2C44&cites=10315031793445629859&scipsc=&q=&scisbd=1'

# # Function to create paginated URLs
# def create_paginated_url(base_url, start_value):
#     # Parse the URL into components
#     parsed_url = urlparse(base_url)
    
#     # Parse the query parameters into a dictionary
#     query_params = parse_qs(parsed_url.query)
    
#     # Add or update the 'start' parameter
#     query_params['start'] = [str(start_value)]
    
#     # Reconstruct the query string
#     new_query = urlencode(query_params, doseq=True)
    
#     # Reconstruct the full URL
#     new_url = urlunparse((
#         parsed_url.scheme,
#         parsed_url.netloc,
#         parsed_url.path,
#         parsed_url.params,
#         new_query,
#         parsed_url.fragment
#     ))
    
#     return new_url

# # Create url2 and url3
# url2 = create_paginated_url(url1, 10)
# url3 = create_paginated_url(url1, 20)

