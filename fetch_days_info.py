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
from bs4 import BeautifulSoup  # Import BeautifulSoup for formatting

def fetch_days_info(urls, author_name):
    for url_info in urls:
        # Unpack the list into variables
        title, url, citation, year, cited_by_url, paper_id, cited_by_url_with_days_info = url_info
        
        # Print the paper ID for debugging
        print("Paper ID:", paper_id)
        
        # Call the fetch function with the required parameters
        fetch(url=url, author_name=author_name, paper_id=paper_id)


def fetch(url, author_name, paper_id):
    # get driver object 
    driver = get_driver()

    # Generate a random delay between 10 and 30 seconds
    time.sleep(random.uniform(10, 30))

    # load the page 
    driver.get(url=url)

    # Fetch all elements with the class name 'gs_ri'
    papers = driver.find_elements(By.CLASS_NAME, 'gs_ri')

    # Get the count of elements
    elements_count = len(papers)

    print(f"Number of elements with class 'gs_ri': {elements_count}")

    # # Print the HTML of each element in a formatted way
    # for index, paper in enumerate(papers, start=1):
    #     html_content = paper.get_attribute('outerHTML')
    #     soup = BeautifulSoup(html_content, 'html.parser')  # Parse the HTML
    #     print(f"Element {index}:\n{soup.prettify()}\n")  # Print formatted HTML

    # List to store paper information
    paper_data = []

    # Iterate through each paper and extract the required information
    for index, paper in enumerate(papers, start=1):
        try:
            # Extract the paper title
            title_element = paper.find_element(By.CLASS_NAME, 'gs_rt')
            title = title_element.text

            # Extract the author list
            author_element = paper.find_element(By.CLASS_NAME, 'gs_a')
            authors = author_element.text

            # Extract the value of the element with class name 'gs_age'
            try:
                age_element = paper.find_element(By.CLASS_NAME, 'gs_age')
                age = age_element.text
            except:
                age = "No age information available"

            # Extract the value of the element with class name 'gs_a'
            gs_a_value = author_element.text

            # Print the extracted information
            print(f"Paper {index}:")
            print(f"Title: {title}")
            print(f"Authors: {authors}")
            print(f"Age: {age}")
            print(f"gs_a Value: {gs_a_value}")
            print("-" * 50)

            # Append the extracted information to the list
            paper_data.append({
                "Title": title,
                "Authors": authors,
                "Age": age,
                "gs_a Value": gs_a_value
            })

        except Exception as e:
            print(f"Error processing paper {index}: {e}")
    
    
    if driver is not None:
        # Close the WebDriver
        driver.quit()

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(paper_data)

    # Print the DataFrame
    print(df)

    # Optionally, save the DataFrame to a CSV file
    df.to_csv(f"{author_name}_{paper_id}_days.csv", index=False)


if __name__ == "__main__":
    name = "jahangir"
    url = 'https://scholar.google.com/scholar?hl=en&as_sdt=5,44&sciodt=0,44&cites=13810402491279919646&scipsc=&q=&scisbd=1'
    fetch_days_info(url=url, author_name=name)

    
