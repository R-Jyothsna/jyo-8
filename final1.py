import requests
from bs4 import BeautifulSoup
import json

def get_category_links(base_url):
    response = requests.get(base_url)
    if response.status_code != 200:
        print("Failed to retrieve the base page")
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')
    categories = soup.select('table.category-list a')

    category_info = {category.text.strip(): base_url.rstrip('/') + category['href'] for category in categories}
    return category_info

def scrape_category(url, category_name, start_page=0):
    proposals = []
    page_number = start_page
    
    while True:
        page_url = f"{url}?page={page_number}"
        print(f"Fetching page {page_number} for category '{category_name}'...")

        response = requests.get(page_url)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number} for category '{category_name}'")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        proposal_elements = soup.find_all('a', class_='title raw-link raw-topic-link')
        
        if not proposal_elements:
            print(f"No proposals found on page {page_number} for category '{category_name}'")
            break

        for element in proposal_elements:
            title = element.get_text(strip=True)
            link = element.get('href')
            proposals.append({'Category': category_name, 'Title': title, 'Link': link})

        page_number += 1

    return proposals

def main():
    base_url = "https://forum.arbitrum.foundation/"
    categories = get_category_links(base_url)
    all_proposals = []

    for category_name, url in categories.items():
        proposals = scrape_category(url, category_name)
        all_proposals.extend(proposals)

    # Save all proposals to a single JSON file
    with open('all_links.json', 'w') as f:
        json.dump(all_proposals, f, indent=4)
    print('Scraping completed and all data saved to all_links.json')

if __name__ == "__main__":
    main()
