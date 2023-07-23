from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re
from database import queue, insert_row
import html2text

data = {}



class SearchEngine:
    def __init__(self, data):
        self.data = data

    def search_text(self, search_text):
        results = []
        for page, content in self.data.items():
            if re.search(search_text, content, re.IGNORECASE):
                results.append(page)
        return results



class WebScraper:
    def __init__(self):
        self.visited_urls = set()

    def scrape_data(self, url):
        if url in self.visited_urls:
            return []

        self.visited_urls.add(url)
        response = requests.get(url)
        insert_row(url, html2text.html2text(response.text))
        soup = BeautifulSoup(response.content, 'html.parser')

        for element in soup.find_all(['a']):
            child_url = urljoin(url, element['href'])
            job = queue.enqueue(background_task, child_url)


def background_task(url):
    print("Scraping: ", str(url))
    scraper = WebScraper()
    scraper.scrape_data(url)