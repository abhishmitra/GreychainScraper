import asyncio
import aiohttp
import psycopg2
from database_file import *
import html2text
from bs4 import BeautifulSoup


def extract_child_urls(base_url, html_content):
    valid_urls = []

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract all anchor tags from the HTML
    anchor_tags = soup.find_all('a', href=True)

    for anchor in anchor_tags:
        url = anchor['href']
        # Join the URL with the base_url to handle relative URLs
        absolute_url = urljoin(base_url, url)
        # Use a regular expression to check if the URL is valid
        if re.match(r'^https?://', absolute_url):
            valid_urls.append(absolute_url)

    return valid_urls

async def scrape_url_async(session, url):
    try:
        async with session.get(url, timeout = 5) as response:
            content = await response.text()

            text = html2text.html2text(content)
            child_urls = extract_child_urls(url, content)

            update_database_with_content(url, text)

            child_urls = [(url, None) for url in child_urls if url not in visited_urls]
            insert_urls_with_content(child_urls)

            visited_urls.add(url)
    except Exception as ex:
        pass

async def process_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_url_async(session, url) for url in urls]
        await asyncio.gather(*tasks)

async def worker():
    while True:
        try:
            print("\nVisited URLs: ", len(visited_urls))
            print("Empty rows: ", count_empty_rows() )

            rows = fetch_empty_text_rows(limit = 400)
            if not rows:
                await asyncio.sleep(1)
                continue

            await process_urls(rows)
        except Exception as e:
            import traceback
            print("Error: ", e)
            await asyncio.sleep(1)

if __name__ == '__main__':
    import time

    print("Background worker started")
    time.sleep(15)

    delete_all_rows()

    visited_urls = get_unique_urls()
    asyncio.run(worker())
