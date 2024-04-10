import requests
from bs4 import BeautifulSoup

def scrape_obituaries(url, mode='all_at_once', current_page=1):
    """Scrape obituaries from the given URL, supporting 'page_by_page' and 'all_at_once' modes."""
    all_names = []
    try:
        if mode == 'page_by_page':
            # Construct the URL for the current page if paginated
            page_url = f"{url}?page={current_page}"
            names = fetch_names_from_page(page_url)
            all_names.extend(names)
        elif mode == 'all_at_once':
            page = current_page
            while True:
                page_url = f"{url}?page={page}"
                names = fetch_names_from_page(page_url)
                if not names:  # Assuming an empty list means no more data
                    break
                all_names.extend(names)
                page += 1
    except Exception as e:
        print(f"An error occurred: {e}")
    return all_names

def fetch_names_from_page(url):
    """Fetch names from a single page URL."""
    names = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Example: Find all <h2> tags with class 'obit-title'
        obit_titles = soup.find_all('h2', class_='obit-title')
        for title in obit_titles:
            names.append(title.text.strip())
    else:
        print(f"Failed to fetch data from {url}")
    return names
