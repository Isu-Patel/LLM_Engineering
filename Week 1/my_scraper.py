from bs4 import BeautifulSoup
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

SOUP = None
URL = None
PAGE_TITLE = None

def fetch_website_contents(url):
    global SOUP, URL, PAGE_TITLE
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        SOUP = BeautifulSoup(response.text, 'html.parser')
        URL = url
        PAGE_TITLE = SOUP.title.string if SOUP.title else "No title"
        print(f"Fetched: {PAGE_TITLE[:50]}...")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        SOUP = None

def fetch_text_contents(url):
    global SOUP
    fetch_website_contents(url)
    if SOUP:
        for script in SOUP(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        text = SOUP.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        return PAGE_TITLE + "\n" + text[:2000] + "..."
    return None

def fetch_website_links(url):
    fetch_website_contents(url)
    if SOUP:
        links = [a_tag['href'] for a_tag in SOUP.find_all('a', href=True)]
        return links
    return []
