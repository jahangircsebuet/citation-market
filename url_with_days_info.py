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
from driver import get_driver
from utils import build_cited_by_url_with_days_info
from fetch_author_papers import fetch_author_papers


def extract_cited_by_urls(data, author_name):
    print("entering into extract_cited_by_urls")
    new_data = []

    for row in data:
        print(len(row), row[1] if len(row) > 0 else None)
        paper_url = row[1] if len(row) > 0 else None
        new_row = []
        new_row.extend(row)
        
        if paper_url is not None:
            driver = None
            try:
                # get the driver 
                driver = get_driver()

                # Generate a random delay between 10 and 30 seconds
                time.sleep(random.uniform(10, 30))

                # Load the paper URL in the browser
                driver.get(paper_url)

                # Wait for the "Cited by" link to appear
                cited_by_anchor = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Cited by"))
                )

                # Extract the link
                cited_by_url = cited_by_anchor.get_attribute('href')
                # print("Cited by URL:", cited_by_url)

                # cited by url where there is no days info 
                new_row.append(cited_by_url)

                # Extract the paper_id from the cited_by_url
                parsed_url = urlparse(cited_by_url)
                query_params = parse_qs(parsed_url.query)
                paper_id = query_params.get('cites', [None])[0]  # Get the 'cites' parameter value
                # print("Extracted Paper ID:", paper_id)
                new_row.append(paper_id)

                # we need the page where there is days info, this is the url where there will be days info 
                cited_by_url_with_days_info = build_cited_by_url_with_days_info(paper_id)
                new_row.append(cited_by_url_with_days_info)

                # store each row to create dataframe later 
                new_data.append(new_row)

            except Exception as e:
                print("Cited by link not found for:", paper_url)
                print("e: ", e)
                cited_by_url = None
        
            if driver is not None:
                # Close the WebDriver
                driver.quit()

    if len(new_data) > 0: 
        # Create a DataFrame from the collected row data
        df = pd.DataFrame(new_data, columns=['Title', 'URL', 'Citation', 'Year', 'CitedByURL', 'PaperID', 'CitedByURLWithDaysInfo'])  # Adjust column names as needed

        df = df.dropna()

        # Save the DataFrame to a CSV file
        df.to_csv(f'{author_name}_papers.csv', index=False)

    return new_data

if __name__ == "__main__":
    # Read the CSV file into a DataFrame
    df = pd.read_csv("jahangir_papers.csv")

    cited_by_urls_with_days = extract_cited_by_urls(df.values, "jahangir")
    
    if len(cited_by_urls_with_days) > 0:
        print("Extracted Cited By URLs with Days Info Successfully!")

    print("#papers: ", len(df.values))
    print("#cited by URLs: ", len(cited_by_urls_with_days))