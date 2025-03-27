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


def get_driver():
    # Set up headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')  # Necessary for some environments
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Initialize the WebDriver in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    return driver

def fetch_author_papers(url, author_name):
    # Initialize a list to store all row data
    all_rows = []
    driver = get_driver()
    driver.get(url)
    try:
        # Find the table by ID
        # 'gsc_a_t' is the selector for the table which contains all the papers 
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
                row_data.append(paper_title)
                row_data.append(paper_url)
                # print("row_data: ", row_data)

                # Extract and append the rest of the columns (e.g., citations, year)
                for col in columns[1:]:
                    # print("col.text.strip(): ", col.text.strip())
                    row_data.append(col.text.strip())

                # row_data.append(paper_title)
                # row_data.append(paper_url)
                
            all_rows.append(row_data)  # Collect row data
        
    except Exception as e:
        print(f'Table not found: {e}')
        return all_rows

    if len(all_rows) > 0: 
        # Create a DataFrame from the collected row data
        df = pd.DataFrame(all_rows, columns=['Title', 'URL', 'Citation', 'Year'])  # Adjust column names as needed

        df = df.dropna()

        # Save the DataFrame to a CSV file
        df.to_csv(f'{author_name}_papers.csv', index=False)

    # Close the WebDriver
    driver.quit()

    return all_rows

if __name__ == "__main__":

    # test cases 
    name = "jahangir"
    url = 'https://scholar.google.com/citations?user=v7hMP8kAAAAJ&hl=en'
    papers = fetch_author_papers(url=url, author_name=name)
    print(f"Author: {name} and #papers: {len(papers)}")
    print(papers)

    name = "sai"
    url = 'https://scholar.google.com/citations?user=VjEGZJoAAAAJ&hl=en'
    papers = fetch_author_papers(url=url, author_name=name)
    print(f"Author: {name} and #papers: {len(papers)}")
    print(papers)

    name = "ismail"
    url = 'https://scholar.google.com/citations?user=FexryyIAAAAJ&hl=en'
    papers = fetch_author_papers(url=url, author_name=name)
    print(f"Author: {name} and #papers: {len(papers)}")
    print(papers)

    name = "abdullah"
    url = 'https://scholar.google.com/citations?user=zQKHA64AAAAJ&hl=en'
    papers = fetch_author_papers(url=url, author_name=name)
    print(f"Author: {name} and #papers: {len(papers)}")
    print(papers)