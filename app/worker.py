from bs4 import BeautifulSoup
from database_file import *
import html2text
import aiohttp
import asyncio

visited_urls = get_unique_urls()

def scrape_and_enqueue(urls, batch_size=100):
    async def scrape_url_async(session, url):
        try:
            async with session.get(url, timeout = 10) as response:
                content = await response.text()
                insert_row(url, html2text.html2text(content))
                visited_urls.add(url)

                child_urls = extract_child_urls(url, content)
                print("\nVisited: ", len(visited_urls))
                print("Child URLs: ", len(child_urls))
                print("Queue Length: ", len(queue.jobs))

                for i in range(0, len(child_urls), batch_size):
                    batch = child_urls[i:i + batch_size]
                    queue.enqueue(scrape_and_enqueue, batch, batch_size)

        except Exception as ex:
            print("Exception: ", str(ex))
            pass

    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [scrape_url_async(session, url) for url in urls if url not in visited_urls]
            await asyncio.gather(*tasks)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

def extract_child_urls(url, content):
    url_list = []
    soup = BeautifulSoup(content, 'html.parser')
    for element in soup.find_all(['a']):
        try:
            joined_url = urljoin(url, element['href'])
            if (joined_url not in url_list):
                url_list.append(joined_url)
        except Exception as ex:
            pass
    return url_list
