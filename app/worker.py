from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re
from database_file import *
import html2text
import aiohttp
import asyncio

queue.empty()


visited_urls = get_unique_urls()

def split_list(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i:i + chunk_size]


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            text = await response.text()
            return text, url
    except Exception as e:
        print(str(e))



def scrape_and_enqueue(urls, batch_size=10):
    async def scrape_url_async(session, url):
        async with session.get(url) as response:
            content = await response.text()
            insert_row(url, html2text.html2text(content))
            visited_urls.add(url)
            print("Visited: ", len(visited_urls))

            child_urls = extract_child_urls(url, content)

            for i in range(0, len(child_urls), batch_size):
                batch = child_urls[i:i + batch_size]
                queue.enqueue(scrape_and_enqueue, batch, batch_size)

    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [scrape_url_async(session, url) for url in urls]
            await asyncio.gather(*tasks)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

def extract_child_urls(url, content):
    url_list = []
    soup = BeautifulSoup(content, 'html.parser')
    for element in soup.find_all(['a']):
        try:
            joined_url = urljoin(url, element['href'])
            if (joined_url not in visited_urls) and (joined_url not in url_list):
                url_list.append(joined_url)
                print("Joined url: ", joined_url)
        except Exception as ex:
            pass
    return url_list

"""
def background_task(url):
    if url in visited_urls:
        return

    print("\nScraping: ", str(url))
    print("List of URLs: ", len(visited_urls))
    visited_urls.add(url)

    response = requests.get(url)
    insert_row(url, html2text.html2text(response.text))
    soup = BeautifulSoup(response.content, 'html.parser')

    for element in soup.find_all(['a']):
        try:
            child_url = urljoin(url, element['href'])
            job = queue.enqueue(background_task, child_url)
        except Exception as ex:
            pass

    visited_urls.add(url)
"""

