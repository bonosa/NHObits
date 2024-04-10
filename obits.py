import requests
from bs4 import BeautifulSoup

def scrape_obituaries(url, mode='all_at_once', current_page=1, max_pages=3):
    """Scrape obituaries from the given URL, supporting 'page_by_page' and 'all_at_once' modes,
    with a limit on the number of pages to fetch."""
    all_names = []
    page_count = 0  # Initialize a counter to track the number of pages fetched
    
    try:
        page = current_page
        while page_count < max_pages:  # Limit the number of pages to fetch
            page_url = f"{url}?page={page}"
            print(f"Fetching data from: {page_url}")  # Debugging print
            response = requests.get(page_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                obit_titles = soup.find_all('h2', class_='obit-title')
                page_names = [title.text.strip() for title in obit_titles]
                
                print(f"Names fetched from page {page}: {page_names}")  # Debug print for names
                
                if not page_names:
                    break  # Stop if no names are found on the page
                all_names.extend(page_names)
                page_count += 1  # Increment the page counter
                
                if mode == 'page_by_page':
                    break  # Stop after fetching one page in 'page_by_page' mode
                page += 1  # Prepare to fetch the next page
            else:
                print(f"Failed to fetch data from {page_url}, Status Code: {response.status_code}")
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return all_names