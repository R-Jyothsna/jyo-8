import json
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
service = Service('C:/Users/rjyot/Desktop/python/selenium/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

def sanitize_filename(title):
    # Remove invalid characters and truncate to a safe length
    sanitized = re.sub(r'[<>:"/\\|?*]', '', title)
    return sanitized[:255]  # Limit filename length to avoid too long names

def scrape_page(url):
    driver.get(url)
    time.sleep(5)  # Allow some time for the page to load

    try:
        comments = []
        comment_elements = driver.find_elements(By.CLASS_NAME, 'cooked')
        for comment_element in comment_elements:
            comment_text = comment_element.text
            if comment_text:
                comments.append(comment_text)

    except Exception as e:
        print(f"Error: {e}")
        comments = []

    return comments

def process_link(link_data):
    title = link_data['Title']
    url = link_data['Link']
    category_name = link_data['Category']
    all_comments = []
    page_number = 0  # Start from page 0

    while True:
        page_url = f"{url}?page={page_number}"
        print(f"Fetching page {page_number} for link '{title}'...")

        comments = scrape_page(page_url)
        if not comments:  # Stop if there are no comments on this page
            print(f"No more comments found on page {page_number} for link '{title}'. Stopping.")
            break
        all_comments.extend(comments)
        page_number += 1

    # Use the first comment as the description
    if all_comments:
        description = all_comments[0]
        other_comments = all_comments[1:]
    else:
        description = "Description not found"
        other_comments = []

    # Ensure description does not appear in comments
    other_comments = [comment for comment in other_comments if comment != description]

    # Save the results to a JSON file
    sanitized_title = sanitize_filename(title)
    json_filename = f'{sanitized_title}.json'
    
    output_data = {
        'Category': category_name,
        'Title': title,
        'Description': description,
        'Comments': other_comments
    }

    with open(json_filename, 'w') as f:
        json.dump(output_data, f, indent=4)
    
    print(f"Processing completed for link '{title}' and data saved to {json_filename}")

def main():
    # Load link data from the single JSON file
    with open('all_links.json', 'r') as f:
        links = json.load(f)

    for link_data in links:
        process_link(link_data)

    driver.quit()

if __name__ == "__main__":
    main()
