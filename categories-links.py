import requests
from bs4 import BeautifulSoup

# URL of the forum
base_url = "https://forum.arbitrum.foundation/"

# Fetch the page
response = requests.get(base_url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all categories within the table
    categories = soup.select('table.category-list a')

    # Extract and print category names along with their links
    category_info = [(category.text.strip(), base_url.rstrip('/') + category['href']) for category in categories]

    for name, link in category_info:
        print(f"Category: {name}, Link: {link}")
else:
    print("Failed to retrieve the page")
