from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re
from database_file import *
import html2text


class WebScraper:
    def __init__(self):
        self.visited_urls = get_unique_urls()

    def scrape_data(self, url):
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        response = requests.get(url)
        insert_row(url, html2text.html2text(response.text))
        soup = BeautifulSoup(response.content, 'html.parser')

        for element in soup.find_all(['a']):
            try:
                child_url = urljoin(url, element['href'])
                job = queue.enqueue(background_task, child_url)
            except Exception as ex:
                pass
        return


def background_task(url):
    print("\nScraping: ", str(url))
    print("List of URLs: ", len(scraper.visited_urls))

    scraper.scrape_data(url)
    scraper.visited_urls.add(url)


scraper = WebScraper()